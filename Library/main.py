import sqlite3 as sql

conn = sql.connect("Final.db")
cursor = conn.cursor()


def get_info(book):
    data = conn.execute(f"SELECT *FROM Book WHERE name ='{book}'").fetchall()
    if len(data) == 0:
        return 'No such book in the table Book'
    book_id = data[0][0]
    author_id = conn.execute(f"SELECT *FROM Library WHERE book_id = {book_id}").fetchall()[0][2]
    return conn.execute(f"SELECT *FROM Author WHERE id = {author_id}").fetchall()[0][1]


def genres():
    data = conn.execute("SELECT *FROM Library GROUP BY genre_type").fetchall()
    for i in data:
        print(i[1])


def add_to_lib(genre, author_id, book_id):
    cursor.execute(f"INSERT INTO Library(genre_type, author_id, book_id) VALUES('{genre}',{author_id},{book_id})")
    conn.commit()
    print('Added')


def delete(book_id):
    cursor.execute(f"DELETE FROM Library WHERE book_id={book_id}")
    conn.commit()
    print('Deleted')


def print_all():
    data = conn.execute("SELECT *FROM Library")
    for i in data:
        print(f"id = {i[0]}, Genre = {i[1]}, Author id = {i[2]}, Book id = {i[3]}")


def not_exist():
    aut = conn.execute("SELECT id FROM Author").fetchall()
    a=[]
    for i in aut:
        a.append(i[0])

    data = conn.execute("SELECT author_id FROM Library").fetchall()
    for i in data:
        if i[0] not in a:
            print(i[0]+' Not exist')



def start():
    while True:
        option = input("""Choose your option:
    1. Get book info by book Name (Book name and author name should be shown) 
    2. Get all available genres in library 
    3. Add book by author ID (automatically assign book to existing author, if author does 
    not exist go to 4th option(add new book the library))
    4. Add a new book to the Library (with this fields: id, genre, author, book)
    5. Delete book by book_id from library
    6. See all library entries (you have to print out all info in the format of: id, genre, author, 
    book)
    7. Find Author without entry in Library (print out Author name and Book name that is 
    not in library)
    8. Exit\n""").strip()
        if option == '1':
            book = input('Enter the book name: ')
            print(book, '-', get_info(book))
        elif option == '2':
            genres()
        if option == '3':
            genre = input('Genre: ')
            author = input('Author id: ')
            book = input('Book id: ')
            add_to_lib(genre, author, book)
        elif option == '4':
            genre = input('Genre: ')
            author = input('Author id: ')
            book = input('Book id: ')
            add_to_lib(genre, author, book)
        if option == '5':
            delete(input('Book id: '))
        elif option == '6':
            print_all()
        if option == '7':
            not_exist()
        elif option == '8':
            exit(0)


start()
