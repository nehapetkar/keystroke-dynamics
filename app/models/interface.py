import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import time

# Load the trained model from the pickle file
model_filename = r'app/models/random_forest_model.pkl'
with open(model_filename, 'rb') as file:
    trained_model = pickle.load(file)

# Load label encoder classes
label_encoder = LabelEncoder()
label_encoder_classes = np.load(r'app/models/label_encoder_classes.npy', allow_pickle=True)
label_encoder.classes_ = label_encoder_classes

# Load scaler used during training
scaler_filename = r'app/models/scaler.pkl'
with open(scaler_filename, 'rb') as file:
    scaler = pickle.load(file)

# Function to preprocess the user input
def preprocess_input(keystrokes):
    from_keys = [keystrokes[i][0] for i in range(len(keystrokes) - 1)]
    to_keys = [keystrokes[i + 1][0] for i in range(len(keystrokes) - 1)]
    flight_times = [keystrokes[i + 1][1] for i in range(len(keystrokes) - 1)]
    
    from_keys_encoded = label_encoder.transform(from_keys)
    to_keys_encoded = label_encoder.transform(to_keys)
    
    input_data = pd.DataFrame({
        'from_key': from_keys_encoded,
        'to_key': to_keys_encoded,
        'flight_time': flight_times
    })
    
    input_data_scaled = scaler.transform(input_data)
    return input_data_scaled

# Input paragraph for reference
reference_paragraph = "A good way to increase your typing speed is to type easy sentences over and over. That will help you to type smoothly without pausing. Try taking a typing speed test before and after to see for yourself. You can even work through this section multiple times and then track your progress.",

# Prompt the user to type the paragraph and capture keystrokes
print("Please type the following paragraph:")
print(reference_paragraph)
print("\nStart typing:")

start_time = time.time()
user_input = input()
end_time = time.time()

# Calculate flight times
keystrokes = [(char, (end_time - start_time) / len(user_input)) for char in user_input]

# Preprocess the input data
input_data = preprocess_input(keystrokes)

# Predict the user based on the input
predicted_user = trained_model.predict(input_data)

# Print predicted user and check predictions
print("Predicted User:", predicted_user[0])

# Debugging: Print the distribution of predictions
unique, counts = np.unique(predicted_user, return_counts=True)
prediction_distribution = dict(zip(unique, counts))
print("Prediction Distribution:", prediction_distribution)
