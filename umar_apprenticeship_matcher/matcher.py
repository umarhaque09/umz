"""Explainable, rule-based matching. Scores are not hiring probabilities."""
import math
import pandas as pd

INTERESTS = ['Data', 'Software', 'Cybersecurity', 'Technology Management']
SKILLS = {'python': 'Practise Python functions, lists and dictionaries; build a small script.',
          'data': 'Clean a CSV with Pandas and explain one chart from the results.',
          'communication': 'Prepare a STAR example about teamwork and practise a two-minute project demo.'}
WEIGHTS = {'academic': .35, 'interest': .30, 'skills': .20, 'location_fit': .15}
REQUIRED = ['company', 'role', 'pathway', 'location', 'minimum_ucas', 'minimum_maths',
            'python_useful', 'data_useful', 'communication_useful']
RESULT_COLUMNS = REQUIRED + ['match_score', 'entry_check', 'match_reasons'] + list(WEIGHTS)

def _number(value, label, low, high):
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise ValueError(f'{label} must be a number.') from None
    if not math.isfinite(number) or not low <= number <= high or not number.is_integer():
        raise ValueError(f'{label} must be a whole number from {low} to {high}.')
    return int(number)

def validate_data(df):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError('Missing dataset columns: ' + ', '.join(sorted(missing)))
    clean = df[REQUIRED].copy()
    for col in ['company', 'role', 'pathway', 'location']:
        if clean[col].isna().any() or clean[col].astype(str).str.strip().eq('').any():
            raise ValueError(f'{col} cannot be blank.')
        clean[col] = clean[col].astype(str).str.strip()
    if not clean['pathway'].isin(INTERESTS).all():
        raise ValueError('Unknown pathway in dataset.')
    for col, low, high in [('minimum_ucas', 0, 300), ('minimum_maths', 1, 9)] + [(s+'_useful', 0, 1) for s in SKILLS]:
        clean[col] = clean[col].map(lambda v: _number(v, col, low, high))
    return clean

def validate_profile(profile):
    p = dict(profile)
    for key, low, high in [('ucas_points', 0, 300), ('maths_grade', 1, 9)] + [(s+'_skill', 0, 5) for s in SKILLS]:
        p[key] = _number(p.get(key), key, low, high)
    if p.get('interest') not in INTERESTS:
        raise ValueError('Select a recognised interest.')
    if p.get('preferred_location') not in ['London', 'Greater London', 'Manchester', 'Birmingham', 'Any']:
        raise ValueError('Select a recognised location.')
    return p

def _location_score(location, preference):
    if preference == 'Any' or location == preference:
        return 1.0
    if {location, preference} == {'London', 'Greater London'}:
        return .8
    return 0.0

def score_opportunities(df, profile):
    df, p = validate_data(df), validate_profile(profile)
    rows = []
    for _, role in df.iterrows():
        ucas = min(p['ucas_points'] / role['minimum_ucas'], 1) if role['minimum_ucas'] else 1
        maths = min(p['maths_grade'] / role['minimum_maths'], 1)
        relevant = [p[s+'_skill']/5 for s in SKILLS if role[s+'_useful']]
        components = {'academic': (ucas+maths)/2,
                      'interest': float(role['pathway'] == p['interest']),
                      'skills': sum(relevant)/len(relevant) if relevant else 1.,
                      'location_fit': _location_score(role['location'], p['preferred_location'])}
        meets = p['ucas_points'] >= role['minimum_ucas'] and p['maths_grade'] >= role['minimum_maths']
        reasons = [f"Sample academic thresholds: {role['minimum_ucas']} UCAS points and Maths grade {role['minimum_maths']}.",
                   'Both sample thresholds met.' if meets else 'One or more sample academic thresholds not yet met.',
                   'Matches your selected interest.' if components['interest'] else 'A different pathway from your selected interest.']
        if p['preferred_location'] == 'Any':
            reasons.append('You selected any location.')
        else:
            reasons.append(f"Location: {role['location']} (preference: {p['preferred_location']}).")
        rows.append({**role.to_dict(), **{k: round(v*100, 1) for k,v in components.items()},
                     'match_score': round(sum(components[k]*w for k,w in WEIGHTS.items())*100, 1),
                     'entry_check': 'Meets sample thresholds' if meets else 'Below sample thresholds',
                     'match_reasons': reasons})
    return pd.DataFrame(rows, columns=RESULT_COLUMNS).sort_values(
        ['match_score', 'company', 'role'], ascending=[False, True, True], kind='stable').reset_index(drop=True)

def recommend_skills(role, profile):
    return [tip for skill, tip in SKILLS.items() if role[skill+'_useful'] and profile[skill+'_skill'] < 3]
