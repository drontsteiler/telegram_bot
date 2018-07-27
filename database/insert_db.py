import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

with open("bank.txt", "r") as ins:
    array = ["zero"]
    for line in ins:
        array.append(line.strip())

length = len(array)
inc = 1

while (inc < length):
    cursor.execute("INSERT INTO ques_and_ans VALUES (NULL, '" + array[inc] + "', '" + array[inc + 1] + "')")
    inc = inc + 3

conn.commit()
conn.close()
