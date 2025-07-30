from simple_db import SimpleDatabase

db = SimpleDatabase()

# this should print an error, since no table is loaded yet
db.create_index("aaa")

db.load_table("students", "students_large.csv")

table_name = db.get_table_name()
print(table_name)
print(db.header)

# this should print an error, since no such column exist
db.create_index("aaa")

selected_header, selected_rows = db.select_rows("students", "id", "a74683920")
print(selected_header)
print(selected_rows)

db.create_index("id")
selected_header, selected_rows = db.select_rows("students", "id", "a74683920")
print(selected_header)
print(selected_rows)

# this should print an error, since no such index exist
db.drop_index("surname")

db.drop_index("id")
selected_header, selected_rows = db.select_rows("students", "id", "a74683920")
print(selected_header)
print(selected_rows)
