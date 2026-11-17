# Heart Disease Prediction - training script
# Dataset: Kaggle "redwankarimsony/heart-disease-data" -> file: heart_disease_uci.csv
import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

df = pd.read_csv("heart_disease_uci.csv")
df["target"] = (df["num"] > 0).astype(int)          # 0 = no disease, 1 = disease
df = df.drop(columns=["id", "dataset", "num"], errors="ignore")

num_cols = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"]
cat_cols = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
df[cat_cols] = df[cat_cols].astype("object").where(df[cat_cols].notna(), None)
for c in cat_cols:
    df[c] = df[c].map(lambda v: None if v is None else str(v))

X, y = df[num_cols + cat_cols], df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42),
}
try:
    from xgboost import XGBClassifier
    models["XGBoost"] = XGBClassifier(n_estimators=200, max_depth=3,
                                      learning_rate=0.05, eval_metric="logloss")
except ImportError:
    print("xgboost not installed, skipping it (pip install xgboost)")

best_name, best_auc, best_pipe = None, -1, None
for name, model in models.items():
    pipe = Pipeline([("prep", prep), ("model", model)])
    pipe.fit(X_train, y_train)
    prob = pipe.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, pipe.predict(X_test))
    auc = roc_auc_score(y_test, prob)
    print(f"{name:20s} accuracy={acc:.3f}  ROC-AUC={auc:.3f}")
    if auc > best_auc:
        best_name, best_auc, best_pipe = name, auc, pipe

print("\nBest model:", best_name)
print(classification_report(y_test, best_pipe.predict(X_test)))

info = {
    "cat_options": {c: sorted(X[c].dropna().unique().tolist()) for c in cat_cols},
    "num_ranges": {c: (float(X[c].min()), float(X[c].max()), float(X[c].median()))
                   for c in num_cols},
    "model_name": best_name,
}
joblib.dump({"pipeline": best_pipe, "info": info}, "model.joblib")
print("Saved model.joblib")
