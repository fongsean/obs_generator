import random
import datetime
import json

# Helper function to simulate activity levels with variability, including days without workouts
def generate_activity(hour, workout_day_probability=0.7, workout_probability=0.5):
    # Randomly determine if today is a workout day
    is_workout_day = random.random() < workout_day_probability  # 70% chance to have a workout day

    # If it's not a workout day, treat it as a regular active day
    if not is_workout_day:
        workout_morning = workout_evening = False
    else:
        # Randomly determine if the user works out in the morning or evening
        workout_morning = random.random() < workout_probability  # 50% chance to workout in the morning
        workout_evening = random.random() < workout_probability  # 50% chance to workout in the evening

    if 6 <= hour < 9:  # Morning time
        if workout_morning:
            return "workout"
        else:
            return "active"
    elif 9 <= hour < 18:  # Daytime (normal activity)
        return "active"
    elif 18 <= hour < 22:  # Evening time
        if workout_evening:
            return "workout"
        else:
            return "active"
    else:  # Nighttime (sleep/rest)
        return "rest"

# Function to generate heart rate based on activity and impact level
def generate_heart_rate(activity, impact):
    # Adjust heart rate ranges based on impact level
    if impact == "low":
        workout_heart_rate_range = (110, 140)  # Lower heart rate during workout for low impact
        active_heart_rate_range = (70, 90)     # Normal heart rate during normal activity
    elif impact == "medium":
        workout_heart_rate_range = (120, 150)  # Moderate heart rate during workout for medium impact
        active_heart_rate_range = (80, 100)    # Moderate heart rate during normal activity
    else:  # high impact
        workout_heart_rate_range = (130, 160)  # Higher heart rate during workout for high impact
        active_heart_rate_range = (90, 120)    # Elevated heart rate during normal activity

    # Generate heart rate based on activity and adjusted ranges
    if activity == "workout":
        return random.randint(*workout_heart_rate_range)  # Adjusted based on impact level
    elif activity == "active":
        return random.randint(*active_heart_rate_range)   # Adjusted based on impact level
    else:
        return random.randint(60, 75)  # Lower during rest/sleep

# Function to generate step count based on activity and impact level
def generate_steps(activity, impact):
    # Adjust step ranges based on impact level
    if impact == "low":
        workout_step_range = (300, 600)  # Higher step count during workout for low impact
        active_step_range = (30, 100)    # Higher step count during normal activity
    elif impact == "medium":
        workout_step_range = (200, 400)  # Medium step count during workout for medium impact
        active_step_range = (10, 50)     # Moderate step count during normal activity
    else:  # high impact
        workout_step_range = (100, 300)  # Lower step count during workout for high impact
        active_step_range = (0, 30)      # Lower step count during normal activity

    # Generate steps based on activity and adjusted ranges
    if activity == "workout":
        return random.randint(*workout_step_range)  # Adjusted based on impact level
    elif activity == "active":
        return random.randint(*active_step_range)   # Adjusted based on impact level
    else:
        return 0  # No steps during rest/sleep


# Function to generate oxygen saturation based on activity and impact level
def generate_oxygen_saturation(activity, impact):
    # Adjust oxygen saturation ranges based on impact level
    if impact == "low":
        workout_saturation_range = (94, 97)  # Higher oxygen saturation during workout for low impact
        active_saturation_range = (96, 99)   # Higher oxygen saturation during normal activity
    elif impact == "medium":
        workout_saturation_range = (92, 96)  # Moderate saturation during workout for medium impact
        active_saturation_range = (94, 98)   # Moderate oxygen saturation during normal activity
    else:  # high impact
        workout_saturation_range = (90, 94)  # Lower saturation during workout for high impact
        active_saturation_range = (92, 97)   # Lower oxygen saturation during normal activity

    # Generate oxygen saturation based on activity and adjusted ranges
    if activity == "workout":
        return random.uniform(*workout_saturation_range)  # Adjusted based on impact level
    elif activity == "active":
        return random.uniform(*active_saturation_range)   # Adjusted based on impact level
    else:
        return random.uniform(96, 99)  # High during rest/sleep


# Function to generate observations with impact parameter
def generate_observations(start_time, interval_minutes, total_days, impact):
    observations = []
    current_time = start_time
    total_intervals = (total_days * 24 * 60) // interval_minutes

    for _ in range(total_intervals):
        activity = generate_activity(current_time.hour)
        heart_rate = generate_heart_rate(activity, impact)
        steps = generate_steps(activity, impact)
        oxygen_saturation = generate_oxygen_saturation(activity, impact)

        observation = {
            "effectiveDateTime": current_time.isoformat(),
            "activity": activity,
            "heartRate": heart_rate,
            "steps": steps,
            "oxygenSaturation": round(oxygen_saturation, 2)
        }
        observations.append(observation)

        # Move to the next time interval
        current_time += datetime.timedelta(minutes=interval_minutes)

    return observations

# Set the start time and generate observations
start_time = datetime.datetime.now()

# Generate observations and output the observations in JSON format with different impact levels
# This is just an example. You can randomise it and use a for loop to generate
observations_medium = generate_observations(start_time, interval_minutes=60, total_days=7, impact="medium")
with open('./generated/observations_medium.json', 'w') as f:
    json.dump(observations_medium, f, indent=4)

observations_low = generate_observations(start_time, interval_minutes=60, total_days=7, impact="low")
with open('./generated/observations_low.json', 'w') as f:
    json.dump(observations_low, f, indent=4)

observations_high = generate_observations(start_time, interval_minutes=60, total_days=7, impact="high")
with open('./generated/observations_high.json', 'w') as f:
    json.dump(observations_high, f, indent=4)

# Next steps would be to:
# 1. convert these observations into FHIR Observations (168 observations per category)
# 2. Extend this script to store them in a FHIR server with patient references i.e A patient would have 504 observation resources (3 categories * 168 observations)
# 3. The `impact` variable can be based on the completed Questionnaire Response submitted by the patient i.e. A "Generate" button on the patient's app can call to this script and generate + upload the observations based on the CAT result's impact (low, medium, high)
# 4. Further tweak the data to be more realistic i.e. more randomised?, more variability?, etc.

# Additional notes:
# - Can test out the entire complete questionnaire -> generate observations -> upload observations flow on a single patient first
# - Prefer to use a PUT request instead of a POST request to prevent creating too many resources. That means you can dynamically create resource IDs like obs_heart_rate_patient_a_1, obs_heart_rate_patient_a_2, etc.
# - All of the above are just suggestions. Feel free to modify and adapt to your needs.



print("Observations generated.")
