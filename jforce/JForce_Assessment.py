import pandas as pd
data = data = {
    "Roll No": [1, 1, 2, 2, 1, 2],
    "Subject": ["DS", "Java", "DS", "Java", "DS", "Java"],
    "Marks":   [25, 40, 30, 26, 40, 50],
    "Date":    ["01-01-23", "02-01-23", "01-01-23", "02-01-23", "15-01-23", "15-01-23"],
}
df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="%d-%m-%y")
 
print("Input DataFrame:")
print(df.to_string(index=False))
print()
 
# sort entire df by date so within each group the order is oldest -> newest
df = df.sort_values(["Roll No", "Subject", "Date"]).reset_index(drop=True)
 
rows = []
 
for (roll, subject), group in df.groupby(["Roll No", "Subject"], sort=False):
    # take only last 3 attempts
    recent = group.tail(3)
 
    marks = recent["Marks"].tolist()[::-1]  # reverse so latest = index 0
 
    # pad with 0 if fewer than 3 attempts
    marks += [0] * (3 - len(marks))
 
    rows.append({
        "Roll No": roll,
        "Subject": subject,
        "M1":      marks[0],
        "M2":      marks[1],
        "M3":      marks[2],
        "Date":    recent["Date"].max().strftime("%d-%m-%y"),
    })
 
result = pd.DataFrame(rows)
result = result.sort_values(["Roll No", "Subject"]).reset_index(drop=True)
 
print("Output DataFrame:")
print(result.to_string(index=False))