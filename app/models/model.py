import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_evaluate_model(model, X_train, X_test, y_train, y_test):
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Return evaluation metrics
    return accuracy, precision, recall, f1

# Load the processed data
final_data_path = 'data/processed/final_data.csv'
data = pd.read_csv(final_data_path)

# Split the data into features (X) and target (y)
X = data.drop(columns=['user_id', 'user_name'])
y = data['user_id']  # Assuming 'user_name' is the target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=24)

# Initialize the models
rf_model = RandomForestClassifier(n_estimators=100, random_state=24)

# Train and evaluate Random Forest model
rf_accuracy, rf_precision, rf_recall, rf_f1 = train_evaluate_model(rf_model, X_train, X_test, y_train, y_test)

# Print the evaluation metrics for both models
print("Random Forest:")
print("Accuracy:", rf_accuracy)
print("Precision:", rf_precision)
print("Recall:", rf_recall)
print("F1-score:", rf_f1)
print("\n")

