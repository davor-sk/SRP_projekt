import pandas as pd
import os

CSV_FILE_PATH = r"C:\Users\Davor\OneDrive\Radna površina\FAKS\3. godina\SRP\projekt\student_mental_health_burnout.csv"

df = pd.read_csv(CSV_FILE_PATH, delimiter=",")
print("CSV size before: ", df.shape)

df = df.dropna()
df.columns = df.columns.str.lower() 
df.columns = df.columns.str.replace(' ', '_') 
print("CSV size after: ", df.shape) 
print(df.head()) 

duplicates = df.duplicated().sum()
print(f"Number of duplicates: {duplicates}")

df20 = df.sample(frac=0.2, random_state=1)
df = df.drop(df20.index)
print("CSV size 80: ", df.shape)
print("CSV size 20: ", df20.shape)

os.makedirs("2_relational_model/processed", exist_ok=True)

df.to_csv("2_relational_model/processed/student_mental_health_PROCESSED.csv", index=False)
df20.to_csv("2_relational_model/processed/student_mental_health_PROCESSED_20.csv", index=False)