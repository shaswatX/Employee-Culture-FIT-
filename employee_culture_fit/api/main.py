from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load models
culture_model = joblib.load("models/culture_fit_reg.pkl")
conflict_model = joblib.load("models/conflict_risk_clf.pkl")
team_model = joblib.load("models/team_fit_clf.pkl")

class EmployeeInput(BaseModel):
    Openness: float
    Conscientiousness: float
    Extraversion: float
    Agreeableness: float
    Neuroticism: float
    Pref_Work_Pace: str
    Pref_Communication: str
    Pref_Work_Setting: str
    Value_Innovation: int
    Value_Teamwork: int
    Value_Leadership: int
    Value_Ethics: int


@app.post("/predict_all")
def predict_all(data: EmployeeInput):

    # Convert input to DataFrame (REQUIRED)
    df = pd.DataFrame([{
        "Openness": data.Openness,
        "Conscientiousness": data.Conscientiousness,
        "Extraversion": data.Extraversion,
        "Agreeableness": data.Agreeableness,
        "Neuroticism": data.Neuroticism,
        "Pref_Work_Pace": data.Pref_Work_Pace,
        "Pref_Communication": data.Pref_Communication,
        "Pref_Work_Setting": data.Pref_Work_Setting,
        "Value_Innovation": data.Value_Innovation,
        "Value_Teamwork": data.Value_Teamwork,
        "Value_Leadership": data.Value_Leadership,
        "Value_Ethics": data.Value_Ethics
    }])

    try:
        score = culture_model.predict(df)[0]
        conflict = conflict_model.predict(df)[0]
        team = team_model.predict(df)[0]

        return {
            "culture_fit_score": float(score),
            "conflict_risk": str(conflict),
            "recommended_team": str(team)
        }

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}
