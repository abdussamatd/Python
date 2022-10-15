import sqlite3 as sql

# setting connection to Final.db (will be created if doesn't exist)
conn = sql.connect("Final.db")

# cursor object for manipulations with db
cursor = conn.cursor()

# create tables
tables = ["CREATE TABLE IF NOT EXISTS Author(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);",
          """CREATE TABLE IF NOT EXISTS Book(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);""",
          """CREATE TABLE IF NOT EXISTS Library(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          genre_type TEXT NOT NULL,
                                          author_id INTEGER NOT NULL,
                                          book_id INTEGER NOT NULL,
                                          FOREIGN KEY (author_id)
                                          REFERENCES Author ON UPDATE CASCADE ON DELETE CASCADE,
                                          FOREIGN KEY (book_id)
                                          REFERENCES Book ON UPDATE CASCADE ON DELETE CASCADE);"""
          ]

# executing table creation
[cursor.execute(i) for i in tables]

# commiting creation of tables
conn.commit()

# data to fill up the Author table
authors = [("Mukhtar Auezov",),
           ("Viktor Hugo",),
           ("E.M Renark",),
           ("Aleksandr Duma",)
           ]

# data to fill up the Book table
books = [("The Abai Way",),
         ("The Hunchback of Notre Dame",),
         ("The Arc of Triumph",),
         ("The Count of Monte Cristo",)
         ]

# data to fill up the Library table
library = [("histrical", "1", "1"),
           ("romanance", "2", "2"),
           ("war novel", "3", "3")
           ]

# running the sql statments for population of tables
cursor.executemany("INSERT INTO Author(name) VALUES(?)", authors)
cursor.executemany("INSERT INTO Book(name) VALUES(?)", books)
cursor.executemany("INSERT INTO Library(genre_type, author_id, book_id) VALUES(?,?,?)",
                   library)

# commiting changes to db
conn.commit()

# cheking the db content
cursor.execute("SELECT * from Library")
print(cursor.fetchall())

# closing streams
cursor.close()
conn.close()