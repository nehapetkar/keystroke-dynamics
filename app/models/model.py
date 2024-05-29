import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the preprocessed data
data_path = 'data/processed/final_data.csv'
df = pd.read_csv(data_path)

# Separate features (dwell times) and target variable (user_id)
X = df.drop(['user_id', 'user_name'], axis=1)  # Assuming 'user_id' and 'user_name' are not part of dwell times
y = df['user_name']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)

# Initialize Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Predict on the testing set
y_pred = rf_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model to a file
model_path = 'data/models/rf_classifier.pkl'
joblib.dump(rf_classifier, model_path)
print(f"Model saved to {model_path}")
