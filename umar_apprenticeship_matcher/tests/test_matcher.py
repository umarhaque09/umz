import unittest
from pathlib import Path
import pandas as pd
from matcher import score_opportunities, recommend_skills

class MatchingTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(Path(__file__).resolve().parents[1]/'data/apprenticeships.csv')
        self.p = dict(ucas_points=112, maths_grade=6, interest='Data', preferred_location='London', python_skill=5, data_skill=5, communication_skill=5)
    def test_perfect_match(self):
        r = score_opportunities(self.df, self.p)
        self.assertEqual(r.iloc[0].match_score, 100)
        self.assertEqual(r.iloc[0].company, 'Demo Analytics')
        self.assertTrue(r.match_score.between(0,100).all())
    def test_maths_changes_score_and_threshold_check(self):
        a = score_opportunities(self.df.iloc[:1], self.p).iloc[0]
        b = score_opportunities(self.df.iloc[:1], {**self.p,'maths_grade':4}).iloc[0]
        self.assertLess(b.match_score,a.match_score)
        self.assertEqual(b.entry_check,'Below sample thresholds')
    def test_threshold_boundary(self):
        for points, expected in [(111,'Below'),(112,'Meets')]:
            r = score_opportunities(self.df.iloc[:1], {**self.p,'ucas_points':points})
            self.assertTrue(r.iloc[0].entry_check.startswith(expected))
    def test_any_location(self):
        r = score_opportunities(self.df, {**self.p,'preferred_location':'Any'})
        self.assertTrue((r.location == 'London').any())
        self.assertTrue((r.location_fit == 100).all())
        self.assertTrue(all('You selected any location.' in reasons for reasons in r.match_reasons))
    def test_skills_only_relevant(self):
        role = self.df[self.df.company=='Demo Digital'].iloc[0]
        self.assertEqual(recommend_skills(role, {**self.p,'data_skill':0}),[])
        self.assertEqual(len(recommend_skills(role,{**self.p,'python_skill':0})),1)
    def test_invalid_inputs(self):
        for key,value in [('maths_grade',0),('python_skill',6),('ucas_points',float('nan'))]:
            with self.assertRaises(ValueError):
                score_opportunities(self.df,{**self.p,key:value})
    def test_invalid_data(self):
        with self.assertRaises(ValueError):
            score_opportunities(self.df.drop(columns=['minimum_maths']), self.p)
    def test_empty_data(self):
        self.assertTrue(score_opportunities(self.df.iloc[:0],self.p).empty)

if __name__ == '__main__':
    unittest.main()
