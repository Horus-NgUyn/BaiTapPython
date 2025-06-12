import pandas as pd

# Tạo DataFrame
data = {
    'Name': ['An', 'Bình', 'Châu', 'Duy', 'Hà', 'Khánh', 'Linh', 'Minh', 'Ngọc', 'Quân'],
    'Age': [20, 21, 19, 22, 20, 23, 21, 20, 22, 19],
    'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'Score': [6.5, 4.0, 7.8, 5.2, 8.0, 3.9, 9.1, 6.0, 4.5, 7.0]
}
df_students = pd.DataFrame(data)

# Hiển thị toàn bộ dữ liệu
print("Toàn bộ dữ liệu:")
print(df_students)

# 3 dòng đầu tiên
print("3 dòng đầu tiên:")
print(df_students.head(3))

# Index = 2 và cột Name
print("Index = 2, cột Name:")
print(df_students.loc[2, 'Name'])

# Index = 10 và cột Age
print("Index = 10, cột Age:")
if 10 in df_students.index:
    print(df_students.loc[10, 'Age'])
else:
    print("Index 10 không tồn tại trong DataFrame.")

# Cột Name và Score
print("Các cột Name và Score:")
print(df_students[['Name', 'Score']])

# Thêm cột Pass
df_students['Pass'] = df_students['Score'] >= 5

# Sắp xếp theo Score giảm dần
df_sorted = df_students.sort_values(by='Score', ascending=False)
print("Dữ liệu sau khi sắp xếp theo Score giảm dần:")
print(df_sorted)
