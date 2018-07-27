import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT answer FROM ques_and_ans")
results = cursor.fetchall()
print(results)

conn.close()
