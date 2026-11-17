import pandas as pd

LABELS = {
    "age": "Age (years)",
    "sex": "Sex",
    "cp": "Chest pain type",
    "trestbps": "Resting blood pressure (mm Hg)",
    "chol": "Cholesterol (mg/dl)",
    "fbs": "Fasting blood sugar > 120 mg/dl",
    "restecg": "Resting ECG result",
    "thalch": "Maximum heart rate achieved",
    "exang": "Exercise-induced angina",
    "oldpeak": "ST depression (oldpeak)",
    "slope": "Slope of peak exercise ST segment",
    "ca": "Major vessels coloured by fluoroscopy (0-3)",
    "thal": "Thalassemia (thal)",
}
INT_COLS = {"age", "trestbps", "chol", "thalch", "ca"}


def label(name):
    return LABELS.get(name, name)


def risk_level(prob):
    if prob < 0.35:
        return "Low", "success"
    if prob < 0.65:
        return "Moderate", "warning"
    return "High", "error"


def clean_feature_name(raw):
    name = raw.split("__", 1)[-1]
    for col in LABELS:
        if name == col:
            return label(col)
        if name.startswith(col + "_"):
            return f"{label(col)}: {name[len(col) + 1:]}"
    return name


def top_importances(pipeline, n=8):
    """Return a DataFrame of the top-n features, or None if the model has no importances."""
    model = pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_"):
        values = abs(model.coef_[0])
    else:
        return None
    names = [clean_feature_name(x) for x in pipeline.named_steps["prep"].get_feature_names_out()]
    df = pd.DataFrame({"Feature": names, "Importance": values})
    df = df.sort_values("Importance", ascending=False).head(n)
    return df.set_index("Feature")


def age_group(age):
    if age < 13:
        return "Child", "🧒"
    if age < 18:
        return "Teenager", "🧑"
    if age < 40:
        return "Young adult", "🧑‍💼"
    if age < 60:
        return "Adult", "👨"
    return "Senior", "👴"
