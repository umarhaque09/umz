import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_profile_and_empty_state(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'12')
        app.slider[0].set_value(0)
        app.checkbox[0].check().run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'0')
        self.assertEqual(len(app.warning),1)
        app.checkbox[0].uncheck().run()
        self.assertEqual(app.metric[0].value,'12')
        self.assertEqual(len(app.exception),0)
