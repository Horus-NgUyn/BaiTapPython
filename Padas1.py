import pandas as pd
data = {
    'Name': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Huy', 'Lan', 'Mai', 'Nam', 'Tú'],
    'Age': [20, 21, 22, 20, 23, 21, 22, 20, 19, 21],
    'Gender': ['Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nữ'],
    'Score': [8.5, 6.0, 7.2, 4.8, 5.5, 9.0, 3.5, 6.8, 7.0, 5.0]
}

df_students = pd.DataFrame(data)
print(df_students)
print(df_students.head(3))
print(df_students.loc[2, 'Name'])
if 10 in df_students.index:
    print(df_students.loc[10, 'Age'])
else:
    print("Index 10 không tồn tại.")
print(df_students[['Name', 'Score']])
df_students['Pass'] = df_students['Score'] >= 5
print(df_students)
df_sorted = df_students.sort_values(by='Score', ascending=False)
print(df_sorted)

