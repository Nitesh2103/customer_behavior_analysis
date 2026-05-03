import pandas as pd
df = pd.read_csv(r"D:\Data_Analytics\Project\customer_shopping_behavior.csv")
print(df.head())
print(df.info())
print(df.describe(include = "all"))
# print(df.isnull().sum())
df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" " , "_")
print(df.columns)
df = df.rename(columns = {"purchase_amount_(usd)" : "purchase_amount"})
print(df.columns)
# Creating New Column as age
labels = [ "Young Adult" , "Adult" , "Middle-aged" , "Senior"]
df["age_group"] = pd.qcut(df["age"], q = 4 , labels = labels)
print(df[["age" , "age_group"]].head(10))
# Creating new column as purchase_frequency_days
frequency_mapping = {
    "Fortnightly" : 14,
    "Weekly" : 7,
    "Montly" : 30,
    "Quarterly" : 30,
    "Bi-Weekly" : 14,
    "Annually" : 365,
    "Every 3 Months" : 90
}
df["purchase_frequency_days"] = df["frequency_of_purchases"].map(frequency_mapping)
df["purchase_frequency_days"] = df["purchase_frequency_days"].fillna(0).astype(int)
print(df[["purchase_frequency_days" , "frequency_of_purchases"]].head(10))
print(df.head())
# To check if discoubnt_applied and promo_code_used columns carry same information
print((df["discount_applied"] == df["promo_code_used"]).all())
df = df.drop("promo_code_used" , axis = 1)
print(df.columns)

# To connect sheet with Databse
# Replace placeholder i.e strings with actual details
from sqlalchemy import create_engine
from urllib.parse import quote_plus
username = "postgres"  # Default database usernmae 
password = quote_plus("Root@123")  # Password set during installation
host = "localhost" # If running locallly
port = "5432" # By default port 
database = "customer_behaviour" # The database created in pgadmin
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2 : Load dataframe into postgresql
table_name = "customer" # Choose any tablename
df.to_sql(table_name,engine,if_exists="replace",index=False)
print(f"Data Successfully loaded into table '{table_name}' in database '{database}'")
 