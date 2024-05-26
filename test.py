import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = [2, 4, 4, 4, 5, 5, 7, 9]

# Calculate mean and standard deviation
mean = np.mean(data)
std_dev = np.std(data)

# Plot histogram
plt.figure(figsize=(8, 6))
plt.hist(data, bins=5, color='skyblue', alpha=0.7, edgecolor='black')
plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(mean - std_dev, color='green', linestyle='dotted', linewidth=2, label='Mean - Std Dev')
plt.axvline(mean + std_dev, color='green', linestyle='dotted', linewidth=2, label='Mean + Std Dev')
plt.axvline(mean - 2 * std_dev, color='orange', linestyle='dotted', linewidth=2, label='Mean - 2*Std Dev')
plt.axvline(mean + 2 * std_dev, color='orange', linestyle='dotted', linewidth=2, label='Mean + 2*Std Dev')
plt.title('Histogram of Data with Mean and Standard Deviation')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

plt.show()
