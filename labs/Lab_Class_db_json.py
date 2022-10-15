import json
import os
import sqlite3
from pathlib import Path


def openFile():
    with open('dict.json') as file:
        return json.load(file)


def writeFile(data):
    with open('dict.json', 'w') as file:
        json.dump(data, file, indent=3)


def createJSON():
    if not os.path.exists('dict.json'):
        s = """
        {
            "1": {
                "fname": "Irene",
                "lname": "Adler",
                "email": "someone@gmail.com",
                "mobile": "87775554433"
            },
            "2": {
              "fname": "Martha",
              "lname": "Hudson",
              "email": "Alshynov@gmail.com",
              "mobile": "87776665544"
            }		
        }
        """
        with open('dict.json', 'w') as file:
            json.dump(json.loads(s), file, indent=3)
        print('dict.json file has been created!')


def task1():
    fname = input('Fill in the form:\nFirst Name: ').strip()
    lname = input('Last Name: ').strip()
    email = input('Email: ').strip()
    mob = input('Mobile number: ').strip()
    birth = input('Date of Birth: ').strip()
    createJSON()
    index = 0
    data = openFile()
    for i in data:
        index += 1
        if data[str(index)]['mobile'] == mob:
            print('Already exist!')
            return
    entry = {
        "fname": fname,
        "lname": lname,
        "email": email,
        "mobile": mob,
        "birth": birth
    }
    data[str(index + 1)] = entry
    writeFile(data)


def task2():
    form_json_path = Path("task2.db")
    if form_json_path.is_file():
        connection = sqlite3.connect('task2.db')
        connection.execute('''CREATE TABLE IF NOT EXISTS task2
                                (fname char(20),
                                lname char(20),
                                email char(20),
                                mobile char(11),
                                birth char(10) );''')
    print('Database task2.db created, table task2 created!')
    while True:
        fname = input('Fill in the form(_r to exit, /all to see the table):\nFirst Name: ').strip()
        if fname == '_r':
            return
        if fname == '/all':
            connection = sqlite3.connect('task2.db')
            sql = connection.cursor()
            sql.execute(f"select *from task2")
            data = sql.fetchall()
            for i in data:
                print(i[0], i[1], i[2], i[3], i[4])
            continue
        lname = input('Last Name: ').strip()
        email = input('Email: ').strip()
        mob = input('Mobile number: ').strip()
        birth = input('Date of Birth: ').strip()
        connection = sqlite3.connect('task2.db')
        sql = connection.cursor()
        sql.execute(f"select *from task2 where mobile='{mob}'")
        data = sql.fetchall()
        if len(data) != 0:
            print('Already exist!')
            continue
        else:
            sql.execute(
                f"insert into task2(fname,lname,email,mobile,birth) values('{fname}','{lname}','{email}','{mob}','{birth}')")
            connection.commit()


# task3
class Animal():  # class
    def __init__(self, animal, area, lifespan, weight):
        self.animal = animal
        self.area = area
        self.lifespan = lifespan
        self.weight = weight

    def move(self):  # class methods
        return f"This {self.animal} can move"

    def eat(self):
        return f"This {self.animal} eats"


def task3():
    dog = Animal('dog', 'ground', "10", "10")
    print(dog.move())
    print(dog.eat())

#task4
class Cat(Animal):

    def __init__(self, animal, area, lifespan, weight, canfly, sleep):
        super().__init__(animal, area, lifespan, weight)
        self.canFly = canfly
        self.sleep = sleep

    def move(self):
        return f"{self.animal} can move because cats have legs"

    def eat(self):
        return f"{self.animal} can eat because cats have mouth"

    def sleepy(self):
        if self.sleep:
            print(f"{self.animal} likes to sleep")
        else:
            print(f"{self.animal} does not like to sleep")


def task4():
    cat1 = Cat('caty', 'home', '10', '5', False, True)
    print(cat1.move())
    print(cat1.eat())
    cat1.sleepy()


task1()
task2()
task3()
task4()