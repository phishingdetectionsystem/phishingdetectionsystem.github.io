"""
Train Real Phishing Detection Model
Uses pre-engineered dataset features
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE


# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv("phishing_dataset.csv")

print("Dataset Columns:", df.columns)

# -----------------------------
# SPLIT FEATURES & LABEL
# -----------------------------
X = df.drop("label", axis=1)
y = df["label"]

print("Feature shape:", X.shape)

# -----------------------------
# BALANCE DATA
# -----------------------------
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled,
    y_resampled,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("🚀 Training model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATE
# -----------------------------
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "phishing_model.pkl")

print("\n✅ Model saved successfully")
print(f"Model expects {model.n_features_in_} features")
