import pandas as pd
import numpy as np

# Generating a sample dataset
np.random.seed(0)  # For reproducibility

# Create a dataframe with dates representing daily records for two academic years
dates = pd.date_range(start="2022-09-01", end="2024-06-30", freq='D')

data = {
    "Date": dates,
    "Course_ID": np.random.choice(['C101', 'C102', 'C103', 'C104', 'C105'], size=len(dates)),
    "Student_ID": np.random.choice(range(1000, 1100), size=len(dates)),
    "Engagement_Score": np.random.uniform(1, 10, size=len(dates)),
    "Performance_Score": np.random.uniform(50, 100, size=len(dates)),
    "Activity_Type": np.random.choice(['Video', 'Quiz', 'Text', 'Project', 'Discussion'], size=len(dates)),
    "Completion_Flag": np.random.choice([0, 1], size=len(dates), p=[0.2, 0.8]),
    "Dropout_Flag": np.random.choice([0, 1], size=len(dates), p=[0.1, 0.9]),
    "Feedback_Score": np.random.randint(1, 6, size=len(dates)),
    "Demographic_Info": np.random.choice(['18-24', '25-34', '35-44', '45+'], size=len(dates))
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_path = "EdTech_Sample_Data.csv"
df.to_csv(csv_path, index=False)

