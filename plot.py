# This is used to visualise the data for testing purposes only, feel free to ignore if you don't need it.

import matplotlib.pyplot as plt
import json
import matplotlib.dates as mdates
from datetime import datetime

# Load the observations from the generated JSON file, change the file name to the one you generated
with open('./generated/observations_medium.json', 'r') as f:
    observations = json.load(f)

# Extract data for plotting
times = [datetime.fromisoformat(obs['effectiveDateTime']) for obs in observations]
heart_rates = [obs['heartRate'] for obs in observations]
steps = [obs['steps'] for obs in observations]
oxygen_saturation = [obs['oxygenSaturation'] for obs in observations]

# Create a figure and subplots
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot heart rate and oxygen saturation on primary y-axis
ax1.set_xlabel('Time')
ax1.set_ylabel('Heart Rate (bpm) / Oxygen Saturation (%)')
ax1.plot(times, heart_rates, 'r-', label='Heart Rate (bpm)')
ax1.plot(times, oxygen_saturation, 'b-', label='Oxygen Saturation (%)')
ax1.tick_params(axis='y')

# Plot steps on secondary y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Steps')
ax2.plot(times, steps, 'g-', label='Steps')
ax2.tick_params(axis='y')

# Format the x-axis to show dates properly
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Add legends for both axes
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Display the plot
plt.title('Heart Rate, Steps, and Oxygen Saturation Over Time')
plt.show()
