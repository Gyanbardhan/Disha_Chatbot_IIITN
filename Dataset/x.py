import pandas as pd

# Load the CSV file
df = pd.read_csv("iiitn.csv")

# Process the 'name' column
df['Name'] = df['Name'].str.replace('-', ' ').str.replace('.', ' ')
df['Details'] = df['Details'].str.replace('_', ' ')

# Save the modified DataFrame to a new CSV file
df.to_csv("iiitn.csv", index=False)
