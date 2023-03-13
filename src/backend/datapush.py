import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "plugdj"
)

file1 = "countries.txt"
file2 = "genres.txt"
file3 = "smthng.txt"

cursor = mydb.cursor()

def main():
    with open(file1, "r") as f:
        while True:
            line = f.readline()

            if len(line) > 0:
                sql = "INSERT INTO countries (name) VALUES (%s)"
                val = (line,)
                mydb.commit()
            else:
                break

    with open(file2, "r") as f:
        while True:
            line = f.readline()

            if len(line) > 0:
                sql = "INSERT INTO genre (name) VALUES (%s)"
                val = (line,)
                mydb.commit()
            else:
                break


main()