# Understand your project

## What it does

Pathfinder compares a student's academics, interests, self-rated skills and location with fictional technology pathways. It ranks the options and explains the score, entry thresholds and priority skills to develop.

## Walk through the code

1. `app.py` reads the CSV into a Pandas DataFrame and collects sidebar inputs.
2. `score_opportunities` validates the dataset and profile.
3. Each row receives four component scores; a weighted sum gives the final score.
4. A separate check compares both academic thresholds directly.
5. Results are sorted and returned to the interface.
6. `recommend_skills` suggests practice for relevant skills rated below 3/5.

## Try these before an interview

- Set 112 points, Maths 6, Data, London and all skills to 5: Demo Analytics scores 100.
- Lower Maths to 4. Explain why the score falls and the entry check changes.
- Change your preferred location to Any. Explain why distant pathways improve.
- Set UCAS points to 0 and turn on the threshold filter. Show the empty-state message.
- Select a software role and lower only your data-analysis skill: explain why an irrelevant skill does not count.
- Download the results and open the CSV.
- Run the tests and read one test's assertions.

## Questions you should be ready for

**Why weighted scoring?** It is transparent and works without a labelled training dataset. The weights reflect design decisions, not research findings.

**Why Python and Pandas?** Python keeps the logic readable; Pandas handles structured CSV data and result tables.

**Why separate entry checks?** A person could have strong interests and skills while missing an academic requirement. A high score must not imply eligibility.

**What was improved from the starter?** Maths now affects scoring and entry checks; sample companies are consistently fictional; input validation, empty states, component explanations, export and tests were added.

**What are the limitations?** Fictional data, subjective skill ratings, hand-picked weights and simplified geography. It does not predict recruitment outcomes.

**What would you improve next?** User feedback, more skills, verified live data and sensitivity testing of the weights.

## Describe your contribution honestly

This build was produced with AI assistance. Do not claim to have independently written or tested things you have not personally worked through. After running and reviewing it, explain which parts you understand, what you changed and how you checked your changes. Avoid memorising a claim of expertise; demonstrate the app and explain a real example.
