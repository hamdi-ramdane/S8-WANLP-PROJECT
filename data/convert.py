import pandas as pd
import numpy as np

# Define input and output file paths
input_file = r"C:\Users\Ram\Desktop\project\Main\data\arabic_news.csv"
output_file = r"C:\Users\Ram\Desktop\project\Main\data\new_arabic_news.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Keep only the first column
first_column_name = df.columns[0]  # Get the name of the first column
df = df[[first_column_name]]  # Keep only that column

# Add a 'label' column with random values (0, 1, or 2)
df['label'] = np.random.randint(0, 3, size=len(df))  # 0, 1, or 2 randomly assigned

# Save the modified DataFrame to a new CSV
df.to_csv(output_file, index=False)

print(f"Processed CSV saved to {output_file}")