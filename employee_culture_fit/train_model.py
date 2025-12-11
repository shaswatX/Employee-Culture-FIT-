import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, classification_report

# Paths
DATA_PATH = os.path.join("data", "employee_culture_fit_minimal_500.csv")
MODELS_DIR = "models"

os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_PATH)

# 2. Define features & targets
target_reg = "CultureFitScore"
target_conflict = "ConflictRisk"
target_team = "RecommendedTeam"

feature_cols = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism",
    "Pref_Work_Pace",
    "Pref_Communication",
    "Pref_Work_Setting",
    "Value_Innovation",
    "Value_Teamwork",
    "Value_Leadership",
    "Value_Ethics",
]

X = df[feature_cols]
y_reg = df[target_reg]
y_conflict = df[target_conflict]
y_team = df[target_team]

# 3. Identify numeric & categorical columns
numeric_features = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism",
    "Value_Innovation",
    "Value_Teamwork",
    "Value_Leadership",
    "Value_Ethics",
]

categorical_features = [
    "Pref_Work_Pace",
    "Pref_Communication",
    "Pref_Work_Setting",
]

# 4. Preprocessor
numeric_transformer = "passthrough"
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# ---------- Model 1: Culture Fit Regression ----------
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

regressor = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

reg_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", regressor),
    ]
)

reg_pipeline.fit(X_train_r, y_train_r)

y_pred_r = reg_pipeline.predict(X_test_r)
mse = mean_squared_error(y_test_r, y_pred_r)
r2 = r2_score(y_test_r, y_pred_r)

print("=== Culture Fit Regression ===")
print(f"MSE: {mse:.2f}")
print(f"R²:  {r2:.3f}")

joblib.dump(reg_pipeline, os.path.join(MODELS_DIR, "culture_fit_reg.pkl"))

# ---------- Model 2: Conflict Risk Classification ----------
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X, y_conflict, test_size=0.2, random_state=42, stratify=y_conflict
)

conf_clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

conf_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", conf_clf),
    ]
)

conf_pipeline.fit(X_train_c, y_train_c)
y_pred_c = conf_pipeline.predict(X_test_c)

print("\n=== Conflict Risk Classification ===")
print(classification_report(y_test_c, y_pred_c))

joblib.dump(conf_pipeline, os.path.join(MODELS_DIR, "conflict_risk_clf.pkl"))

# ---------- Model 3: Team Fit Classification ----------
X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(
    X, y_team, test_size=0.2, random_state=42, stratify=y_team
)

team_clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

team_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", team_clf),
    ]
)

team_pipeline.fit(X_train_t, y_train_t)
y_pred_t = team_pipeline.predict(X_test_t)

print("\n=== Team Fit Classification ===")
print(classification_report(y_test_t, y_pred_t))

joblib.dump(team_pipeline, os.path.join(MODELS_DIR, "team_fit_clf.pkl"))

print("\n✅ Training complete. Models saved to 'models/'")
