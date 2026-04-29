# ==============================
# Loan Approval Prediction Model
# ==============================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load Dataset
df = pd.read_csv("loan_approval_dataset.csv")

# Data Cleaning
for col in df.columns:
    if df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].median(), inplace=True)

# Encode Categorical Data
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])

# Feature & Target Split
target_column = "Loan_Status"
X = df.drop(target_column, axis=1)
y = df[target_column]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model Training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save Model
joblib.dump(model, "loan_model.pkl")

# Prediction Function
def predict_loan(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return "Approved" if prediction[0] == 1 else "Rejected"
