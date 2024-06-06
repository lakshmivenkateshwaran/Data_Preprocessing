import pandas as pd
import numpy as np

# Sample function for demonstration
def some_function(value):
    if pd.isna(value):
        return 0
    else:
        return len(str(value))

# Process data function
def process_data(df):
    # Apply some_function to the 'Country' column
    df['ProcessedCountry'] = df['Country'].apply(some_function)
    return df

# Function to extract datetime features
def extract_datetime_features(df, InvoiceDate):
    df[InvoiceDate] = pd.to_datetime(df[InvoiceDate])
    df['hour'] = df[InvoiceDate].dt.hour
    df['minute'] = df[InvoiceDate].dt.minute
    df['year'] = df[InvoiceDate].dt.year
    df['month'] = df[InvoiceDate].dt.month
    df['day'] = df[InvoiceDate].dt.day
    df.drop(columns=[InvoiceDate], inplace=True)
    return df

# Read the Excel file into a DataFrame
df = pd.read_csv(r"C:\Users\venki\Downloads\archive (4)\data.csv", encoding='latin1')  # Replace 'data.xlsx' with the path to your Excel file

# Replace NaN values with "Unknown" in the 'Country' column
df['CustomerID'].fillna('Not known', inplace=True)

# Sample a subset of the data (e.g., 100 rows) for testing
df_sample = df.sample(n=100, random_state=1)  # Adjust the number of rows as needed

# Apply the extract_datetime_features function
df_sample = extract_datetime_features(df_sample, 'InvoiceDate')

# Apply the process_data function
df_sample = process_data(df_sample)

# Check for null values column-wise
null_columns = df_sample.columns[df_sample.isnull().any()]
print("Columns with null values:")
print(df_sample[null_columns].isnull().sum())

# Check for null values row-wise
null_rows = df_sample[df_sample.isnull().any(axis=1)]
print("\nRows with null values:")
print(null_rows)

# Overall null value count
print("\nTotal null values in the dataset:")
print(df_sample.isnull().sum().sum())

# Print the processed sample dataframe
print("\nProcessed sample DataFrame:")
print(df_sample.columns)

# Export the processed sample DataFrame to an Excel file
df_sample.to_excel(r"C:\Users\venki\Work\Data_Engineering\Data_cleaning\processed_data_updated_3.xlsx", index=False)

print("Data exported to Excel successfully!")
