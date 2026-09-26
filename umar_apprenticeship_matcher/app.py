"""Streamlit presentation layer; matching logic lives in matcher.py."""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matcher import INTERESTS, WEIGHTS, score_opportunities, recommend_skills

st.set_page_config(page_title='Pathfinder | Career Matcher', page_icon='🧭', layout='wide')
st.caption('PATHFINDER / YOUR NEXT STEP')
st.title('Find a direction that fits you.')
st.write('Explore technology pathways using your academics, interests, skills and location.')
st.info('Portfolio demo · All 12 employers and opportunities are fictional. Scores describe fit, not your chance of getting a job.')

with st.sidebar:
    st.header('Build your profile')
    ucas = st.slider('Estimated UCAS points', 0, 224, 112, step=4)
    maths = st.selectbox('GCSE Maths grade', list(range(1,10)), index=4)
    interest = st.selectbox('Main interest', INTERESTS)
    location = st.selectbox('Preferred location', ['London', 'Greater London', 'Manchester', 'Birmingham', 'Any'])
    st.subheader('Your confidence')
    st.caption('0 = new to this · 5 = very confident')
    python = st.slider('Python', 0, 5, 2)
    data = st.slider('Data analysis', 0, 5, 2)
    communication = st.slider('Communication', 0, 5, 4)
    only_meets = st.checkbox('Only show sample thresholds met')
    st.caption('Profiles are used in this session. This app does not write them to a database.')

profile = dict(ucas_points=ucas, maths_grade=maths, interest=interest, preferred_location=location,
               python_skill=python, data_skill=data, communication_skill=communication)
try:
    opportunities = pd.read_csv(Path(__file__).parent / 'data' / 'apprenticeships.csv')
    results = score_opportunities(opportunities, profile)
except (ValueError, OSError) as exc:
    st.error(f'Could not load matches: {exc}')
    st.stop()
if only_meets:
    results = results[results.entry_check == 'Meets sample thresholds'].reset_index(drop=True)

left, centre, right = st.columns(3)
left.metric('Pathways to explore', len(results))
centre.metric('Sample thresholds met', int((results.entry_check == 'Meets sample thresholds').sum()))
right.metric('Top fit score', f'{results.iloc[0].match_score:.1f}/100' if len(results) else '—')
if results.empty:
    st.warning('No results meet both sample thresholds. Turn off the filter to explore pathways and their requirements.')
    st.stop()

matches, plan, method = st.tabs(['Your matches', 'Skills action plan', 'How matching works'])
with matches:
    st.subheader('Your strongest matches')
    for rank, (_, role) in enumerate(results.head(3).iterrows(), 1):
        with st.container(border=True):
            a,b = st.columns([4,1])
            a.markdown(f"**{rank}. {role['role']}**")
            a.caption(f"{role['company']} · {role['location']} · {role['entry_check']}")
            b.metric('Fit', f"{role['match_score']:.1f}")
            st.progress(float(role['match_score'])/100)
    with st.expander('Compare all pathways', expanded=True):
        cols = ['company','role','location','minimum_ucas','minimum_maths','entry_check','match_score']
        st.dataframe(results[cols], hide_index=True, width='stretch')
        export = results.drop(columns=['match_reasons']).copy()
        st.download_button('Download this comparison (CSV)', export.to_csv(index=False), 'career_matches.csv', 'text/csv')
    selected = st.selectbox('Explore a match', range(len(results)),
                            format_func=lambda i: f"{results.iloc[i]['company']} — {results.iloc[i]['role']}")
    role = results.iloc[selected]
    for reason in role.match_reasons:
        st.write('• '+reason)
    fig, ax = plt.subplots(figsize=(8,2.5))
    fig.patch.set_facecolor('#f5f7fb')
    ax.set_facecolor('#f5f7fb')
    ax.barh(list(WEIGHTS)[::-1], [role[k] for k in list(WEIGHTS)[::-1]], color='#0d9488')
    ax.set_xlim(0,100)
    ax.set_xlabel('Component fit (0–100, before weighting)')
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
with plan:
    st.subheader(f"Next steps for {role['role']}")
    gaps = recommend_skills(role, profile)
    if gaps:
        for i, tip in enumerate(gaps,1):
            st.write(f'{i}. {tip}')
    else:
        st.success('No priority gaps at the self-rating threshold. Demonstrate your skills with a working project and evidence.')
    if ucas < role.minimum_ucas:
        st.write(f'Academic gap: {role.minimum_ucas-ucas} estimated UCAS points below this sample threshold.')
    if maths < role.minimum_maths:
        st.write(f'Maths gap: sample grade {role.minimum_maths}; your selected grade is {maths}.')
    st.caption('Suggested skills are development ideas, not certified assessments or employer requirements.')
with method:
    st.subheader('A score you can explain')
    st.write('Academic fit contributes 35%, interest 30%, skills 20% and location 15%.')
    st.write('Academic fit averages your UCAS and Maths ratios, each capped at 100%. Interest is an exact pathway match. Skills average your relevant confidence ratings. Location receives 100% for an exact match or Any, 80% between London and Greater London, and 0% otherwise.')
    st.code('score = 100 × (0.35 × academic + 0.30 × interest\n               + 0.20 × skills + 0.15 × location)')
    st.write('Entry checks stay separate from the score: a strong fit can still fall below sample academic thresholds. Actual employers may also specify subjects, qualifications and other conditions.')
    st.caption('This is a rule-based recommender. It does not use machine learning or predict recruitment outcomes.')
