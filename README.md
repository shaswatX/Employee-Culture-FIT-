# Employee Culture Fit Analyzer (Behavioral AI)

An end-to-end Machine Learning project that predicts:

- Culture Fit Score (0–100)
- Conflict Risk (Low / Medium / High)
- Recommended Team Fit

using Big Five-like personality traits, workstyle preferences, and value alignment.

## Tech Stack

- Python, pandas, scikit-learn
- FastAPI (ML serving)
- Streamlit (interactive dashboard)
- joblib (model persistence)

## Project Structure

```bash
employee_culture_fit/
├─ data/
│   └─ employee_culture_fit_minimal_500.csv
├─ models/
│   ├─ culture_fit_reg.pkl
│   ├─ conflict_risk_clf.pkl
│   └─ team_fit_clf.pkl
├─ api/
│   └─ main.py
├─ frontend/
│   └─ app.py
├─ train_model.py
├─ requirements.txt
└─ README.md
