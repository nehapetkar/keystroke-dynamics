import pandas as pd

# Load the CSV file
data = pd.read_csv('data/processed/final_data.csv')
import matplotlib.pyplot as plt

# Scatter plot of dwell_time vs flight_time
plt.figure(figsize=(10, 6))
plt.scatter(data['dwell_time'], data['flight_time'], alpha=0.5)

# Adding labels and title
plt.xlabel('Dwell Time')
plt.ylabel('Flight Time')
plt.title('Scatter Plot of Dwell Time vs Flight Time')

# Show the plot
plt.show()
