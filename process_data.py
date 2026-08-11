import pandas as pd

files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]
dataframes = []

for file in files:
    df = pd.read_csv(file)

    # Keep only pink morsels
    df = df[df["product"] == "pink morsel"]
    # Convert price from "$3.00" to a number
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

    # Calculate sales
    df["sales"] = df["price"] * df["quantity"]
    # Keep only the required fields
    df = df[["sales", "date", "region"]]

    dataframes.append(df)
# Combine all three files
result = pd.concat(dataframes, ignore_index=True)
# Save the formatted data
result.to_csv("formatted_sales_data.csv", index=False)

print("Data processing completed.")
print(result.head())