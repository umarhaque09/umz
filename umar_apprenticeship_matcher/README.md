# Pathfinder — Apprenticeship & Career Matcher

A Python portfolio application that helps students explore technology career pathways. Enter academic results, interests, skill confidence and a preferred location to get ranked, explained recommendations.

**Portfolio demonstration:** all 12 employers and opportunities are fictional. The dataset is not a vacancy feed. Entry thresholds are illustrative, and scores are not hiring probabilities.

## Features

- Interactive Streamlit profile and results interface
- Weighted scoring with four visible components
- UCAS and GCSE Maths checks, separate from the compatibility score
- Skills-gap suggestions tied to the selected pathway
- London, Greater London, Manchester, Birmingham and any-location preferences
- Comparison table, CSV export and Matplotlib breakdown chart
- Input validation, empty-state handling and automated tests

## Run locally

Use Python 3.12. Download and extract the project, then open a terminal inside the folder containing `app.py`.

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install and start:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in your terminal. Keep the terminal running while using the app. Stop it with Ctrl+C.

## Algorithm

Each component is between 0 and 1:

| Component | Weight | Rule |
|---|---:|---|
| Academic | 35% | Average of UCAS/minimum UCAS and Maths/minimum Maths, each capped at 1; a zero UCAS minimum is automatically met |
| Interest | 30% | 1 for an exact pathway match, otherwise 0 |
| Skills | 20% | Average of relevant self-ratings divided by 5; no requested skills gives 1 |
| Location | 15% | 1 for exact match or Any, 0.8 between London and Greater London, otherwise 0 |

`score = 100 × (0.35A + 0.30I + 0.20S + 0.15L)`

Example: 112 UCAS points, Maths grade 6, Data interest, London, and all relevant skills at 5 produces 100 for Demo Analytics. Lowering Maths to 4 reduces that score to 94.2 and marks the sample thresholds as not met. This shows why a compatibility score must not replace an entry check.

Weights are design choices, not statistically learned values. Ties use company and role names for stable ordering. Scores are rounded to one decimal place.

## Project layout

- `app.py`: interface, chart and CSV export
- `matcher.py`: validation, scoring and skills recommendations
- `data/apprenticeships.csv`: fictional demonstration dataset
- `tests/`: scoring boundaries, invalid data and interactive app checks
- `.github/workflows/tests.yml`: test workflow for GitHub
- `INTERVIEW_CHEATSHEET.md`: learning and demonstration guide
- `GITHUB_SETUP.md`: repository publishing instructions

## Test

```bash
python -m unittest discover -s tests -v
```

Nine tests cover perfect matching, Maths impact, UCAS boundaries, location handling, relevant skills, malformed inputs, missing columns, empty data and interactive filtering. Tested on Python 3.12 with the dependency versions in `requirements.txt`.

## Limitations and next improvements

This is a rule-based recommender, not machine learning. Self-ratings are subjective; academic ratios are a simple approximation. It does not check qualification equivalence, required subjects, residency or other real recruitment conditions. Geography is categorical rather than a commuting-distance calculation. No accounts or application tracking are included.

Useful next steps: collect feedback from students, test alternative weights, expand skills, and add verified vacancy data with source URLs and checked dates. Live data should keep verified employer requirements separate from illustrative examples.

## Privacy and development

The app does not save profile inputs to disk or a database. Downloads are generated in the session. Do not commit CVs, contact details, credentials or real student profiles. Streamlit usage-stat collection is disabled in the configuration.

This version was developed with AI assistance. Review the source, run the experiments in the interview guide, and describe your own contribution accurately when presenting it.
