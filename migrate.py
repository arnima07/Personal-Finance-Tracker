import pandas as pd

# Read old file
df = pd.read_csv("expenses.csv")

# Create new dataframe
new_df = pd.DataFrame()

new_df["Type"] = "Expense"
new_df["Amount"] = df["TransactionAmount"]
new_df["Category"] = df["TransactionType"]
new_df["Description"] = df["Description"]

# Save migrated file
new_df.to_csv("expenses_new.csv", index=False)

print("Migration Complete!")
print(new_df.head())