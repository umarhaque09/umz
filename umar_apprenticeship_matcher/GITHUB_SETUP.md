# Publish the project on GitHub

The package is ready to become a repository. Do not upload the ZIP itself as the source code; extract it and use the files inside `umar_apprenticeship_matcher`.

Suggested name: `apprenticeship-career-matcher`

Suggested description: `Explainable Python career-pathway matcher with Streamlit, academic checks, skills-gap recommendations and automated tests.`

If publishing from an authenticated computer with GitHub CLI:

```bash
git init -b main
git add .
git commit -m "Build career matcher with explained scores and tests"
gh repo create apprenticeship-career-matcher --private --source=. --remote=origin --push
```

Start private so you can review the repository. When ready to share it with recruiters, change its visibility to public in GitHub settings and pin it on your profile. Do not invent earlier commits or dates.

The included GitHub Actions workflow runs the tests after pushes and pull requests. The workflow has not been executed on GitHub until the repository is uploaded.
