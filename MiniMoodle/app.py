from collections import defaultdict
import json, os, getpass, random, sys 

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def openFile():
	with open('dict.json') as file:
		return json.load(file)

def writeFile(data):
	with open('dict.json', 'w') as file:
		json.dump(data,file,indent=3) 


def send(a,b,message):
	try:
		data = openFile()
		if data['users'][b]['usertype'] == 1:
			user = 'teachers'
		elif data['users'][b]['usertype'] == 2:
			user = 'students'
		else:
			return False
		data[user][b]['inbox']['count_static']+=1
		newmes = data[user][b]['inbox']['count_static']
		data[user][b]['inbox'][str(newmes)] = {
			"From" : a,
			"message" : message
		}
		writeFile(data)
		return True
		
	except:
		return False


def check(self):
	pass

class users(object):
	def __init__(self,login,password,usertype):
		data = openFile()
		entry = {
			"password" : password, 
			"usertype" : usertype
		}
		data['users'][login] = entry
		data['users']['count']+=1
		writeFile(data)
		print("User added. Login: {}, Password: {}".format(login,password))
				
class admin():
	def __init__(self, login):
		self.login = login
		self.homePage()

	def show(self,usertype):
		data = openFile()
		print(usertype.capitalize()+':')
		for i in data[usertype]:
			if i=='count':
				continue
			print('Login: {}, Full Name: {}'.format(i,data[usertype][i]['fullname']))
		print()
	
	def create_user(self,usertype='students'):
		fullName = input('Full Name: ').strip()
		login = input('Login: ').strip()
		password = input('Password (If you want to set it as a login leave this empty): ').strip()
		if password=='':
			password=login
		if fullName=='' or login=='':
			print('Full Name and Login cannot be empty!')
			return self.create_user(usertype)
		data = openFile()
		if (login in data['users'] or login in data[usertype]):
			print('Such login already exist!')
			return self.create_user(usertype)
		x = 1
		if usertype == 'students':
			x = 2
		entry = {
			"fullname" : fullName,
			"courses": [],
			"rating" :{},
			"inbox" : {
				"count_static" : 0
			}
		}
		data[usertype][login] = entry
		data[usertype]['count']+=1
		writeFile(data)
		cls()
		users(login,password,x)

	def update_user(self,usertype):
		data = openFile()
		if data[usertype]['count'] == 0:
			print('0 {} in database!'.format(usertype))
			return
		self.show(usertype)
		login = input('Enter the login (or enter "_b" if you want to go back): ').strip()
		if login == "_b":
			cls()
			return
		newFullName = input('Enter new Full Name: ').strip()
		try:
			data[usertype][login]['fullname'] = newFullName
			writeFile(data)
		except:
			print('Wrong login!')
			self.update_user()
		else:
			print('Done!')
			self.show(usertype)
			return

	def delete_user(self,usertype):
		data = openFile()
		if data[usertype]['count'] == 0:
			print('0 {} in database!'.format(usertype))
			return
		self.show(usertype)
		login = input('Enter the login (or enter "_b" if you want to go back): ').strip()
		if login == "_b":
			cls()
			return
		try:
			for i in data[usertype][login]["courses"]:
				data['courses'][i][usertype].remove(login)
			del data[usertype][login]
			del data['users'][login]
			data[usertype]['count'] -=1
			data['users']['count'] -=1
			writeFile(data)
		except:
			print('Wrong login!')
			self.delete_user(usertype)
		else:
			print('Done!')
			self.show(usertype)
			return			

	def c_u_d_user(self,role):
		while True:
			choice = input('''Select an action:
1. Create
2. Update
3. Delete
4. Back
''').strip()
			if choice == '1':
				self.create_user(role)
			elif choice == '2':
				self.update_user(role)
			elif choice == '3':
				self.delete_user(role)
			elif choice == '4':
				cls()
				return
			else:
				print('Wrong choice, please try it again')	

	def show_courses(self,regular=None):
		data = openFile()
		if regular==None:
			print('Courses:')
		elif regular:
			print('Regular courses:')
		else:
			print('Free courses:')
		count=0
		for i in data['courses']:
			if count<2:
				count+=1
				continue
			if regular==None:
				if data['courses'][i]['limitation'] != 0:
					x = 'free'
				else:
					x = 'regular'
				print('Course id: {}, Name: {}, Type: {}\n'.format(i,data['courses'][i]['course'],x))
				continue
			if data['courses'][i]['limitation'] == 0 and regular:
				print('Course id: {}, Course name: {}\n'.format(i,data['courses'][i]['course']))
				continue
			if data['courses'][i]['limitation'] != 0 and regular==False:
				print('Course id: {}, Course name: {}, Limit:{}\n'.format(i,data['courses'][i]['course'],data['courses'][i]['limitation']))
				continue
	
	def create_course(self):
		course = input('Course(subject) name: ').strip()
		limitation = input('Free course participant limitation (leave empty if it is regular course): ').strip()
		if course == '':
			print('Course name cannot be empty!')
			return self.create_course()
		if not limitation.isnumeric():
			limitation = 0
		data = openFile()
		data['courses']['count_static']+=1
		data['courses']['count']+=1
		courseid = data["courses"]["count_static"]
		entry = {
			"course" : course,
			"limitation" : int(limitation),
			"teachers" : [],
			"students" : [],
			"marks" : {

			}
		}
		data['courses'][courseid] = entry
		writeFile(data)
		cls()

	def update_course(self):
		data = openFile()
		if data['courses']['count'] == 0:
			print('0 courses in database!')
			return
		self.show_courses()
		course_id = input('Enter id of the course (or enter "_b" if you want to go back): ').strip()
		if course_id == "_b":
			cls()
			return
		try:
			new_name = input('Enter new course name (leave empty if not needed): ').strip()
			new_limitation = input('New limitation: empty(no change), 0(it become regular), otherwise(become free course): ').strip()
			if new_name!='':
				data['courses'][course_id]['course'] = new_name
			if new_limitation!='':
				data['courses'][course_id]['limitation'] = int(new_limitation)
			writeFile(data)	
		except:
			print('Wrong data!')
			self.update_course()
		else:
			print('Done!')
			self.show_courses()
			return


	def delete_course(self):
		data = openFile()
		if data['courses']['count'] == 0:
			print('0 courses in database!')
			return
		self.show_courses()
		course_id = input('Enter id of the course (or enter "_b" if you want to go back): ').strip()
		if course_id == "_b":
			cls()
			return
		try:
			for i in data['courses'][course_id]['students']:
				data['students'][i]['courses'].remove(course_id)
			for i in data['courses'][course_id]['teachers']:
				data['teachers'][i]['courses'].remove(course_id)
			del data['courses'][course_id]
			data['courses']['count'] -=1
			writeFile(data)
		except:
			print('Wrong data!')
			self.delete_course()
		else:
			print('Done!')
			self.show_courses()
			return			

	def attach(self,usertype,course_id,login):
		data = openFile()
		try:
			if login in data['courses'][course_id][usertype]:
				return None
			data['courses'][course_id][usertype].append(login)
			data[usertype][login]['courses'].append(course_id)
			writeFile(data)
		except:
			return False
		else:
			return True


	def attach_to_the_courses(self):
		data = openFile()
		if data['courses']['count'] == 0:
			print('0 courses in database!')
			return
		self.show_courses()
		course_id = input('Enter id of the course (or enter "_b" if you want to go back): ').strip()
		if course_id == "_b":
			cls()
			return
		choice = input('Choose the role of the user. Teacher(t)/Studnet(otherwise): ').strip()
		if choice=='t':
			choice = 'teachers'
		else:
			choice = 'students'
		self.show(choice)
		login = input('Enter login of needed user: ').strip()
		x = self.attach(choice,course_id,login)
		if x==None:
			print('Already attached')
		elif x:
			print('Done!')
		else:
			print('Wrong data!')
		return self.attach_to_the_courses()

	def manage_courses(self):
		while True:
			choice = input('''Select an action:
1. Create (regular/free) course
2. Update course
3. Delete course
4. Attach students and teachers to the courses
5. Back
''').strip()
			if choice == '1':
				self.create_course()
			elif choice == '2':
				self.update_course()
			elif choice == '3':
				self.delete_course()
			elif choice == '4':
				self.attach_to_the_courses()
			elif choice == '5':
				cls()
				return
			else:
				print('Wrong choice, please try it again')

	def homePage(self):
		while True:
			choice = input('''Home page. User - {}
Select an action:
1. Create/Update/Delete Teachers
2. Create/Update/Delete Students
3. Create/Update/Delete Courses
4. Exit from account
5. Terminate a program
'''.format(self.login)).strip()
			if choice == '1':
				self.c_u_d_user('teachers')
			elif choice == '2':
				self.c_u_d_user('students')
			elif choice == '3':
				self.manage_courses()
			elif choice == '4':
				return
			elif choice == '5':
				sys.exit()
			else:
				cls()
				print('Wrong choice, please try it again')

class teacher():
	def __init__(self, login):
		self.login = login
		self.homePage()

	def show_subjects(self):
		data = openFile()
		for i in data['teachers'][self.login]['courses']:
			if data['courses'][i]['limitation']!=0:
				x = 'regular'
			else:
				x = 'free'
			print('Course id = {}, Course name = {}, type = {}\n'.format(i,data['courses'][i]['course'],x))
		print()

	def mark_students(self):
		subject_id = input('Enter subject id (_b to back): ').strip()
		if subject_id=='_b':
			return
		data = openFile()
		try:
			j = 1
			for i in data['courses'][subject_id]['students']:
				print(str(j),'Login:',i,'Full Name:',data['students'][i]['fullname'])
			print()
			student = input('Enter login of needed student: ').strip()
			if student in data['courses'][subject_id]['students']:
				mark = int(input('Enter mark(0-100): '))
				if mark >100 or mark <0:
					print('Wrong mark!')
					return self.mark_students()
				data['courses'][subject_id]['marks'][student] = mark
				writeFile(data)
			else:
				print('Wrong student login!')
				return self.mark_students()
		except:
			print('Error!')
			return self.mark_students()
		else:
			print('Done!')
			return
	
	def add_to_course(self):
		self.show_subjects()
		subject_id = input('Enter id of needed course: ').strip()
		admin.show(None,'students')
		login = input('Enter login of needed student: ').strip()
		try:
			x = admin.attach(None,'students',subject_id,login)
			if x==None:
				print('Already attached')
			elif x:
				print('Done!')
			else:
				print('Wrong data!')
			return
		except:
			pass
		
	def delete_from_course(self):
		self.show_subjects()
		subject_id = input('Enter id of needed course: ').strip()
		data = openFile()
		try:
			for i in data['courses'][subject_id]['students']:
				print(i,data['students'][i]['fullname'])
			login = input('Enter login of needed student: ').strip()
			data['courses'][subject_id]['students'].remove(login)
			data['students'][login]['courses'].remove(subject_id)
			writeFile(data)
		except:
			print('Wrong data')
			return
		else:
			print('Done!')
			pass

	def rate(self):
		admin.show(None,'students')
		data = openFile()
		login = input('Enter login of needed student: ').strip()
		if login in data['students']:
			if not self.login in data['students'][login]['rating']:
				point = input('Enter rating: ').strip()
				data['students'][login]['rating'][self.login] = point
				print('Rated!')
				writeFile(data)
				return
			else:
				print('Already rated')
				return
		else:
			print('Wrong login')
			return

	def homePage(self):
		print('''Home page. Teacher - {}

Select an action:
1. Show my subjects
2. Mark student
3. Add or Delete student to/from a course
4. Rate student
5. Send message
6. Check inbox
7. Exit
'''.format(self.login))
		while True:
			choice = input().strip()
			if choice == '1':
				self.show_subjects()
			elif choice == '2':
				self.mark_students()
			elif choice == '3':
				x = input('Add(a) or delete(d)? ').strip()
				if x=='a':
					self.add_to_course()
					self.homePage()
				elif x=='d':
					self.delete_from_course()
				else: 
					print('Wrong choice')
					continue
			elif choice == '4':
				self.rate()
			elif choice == '5':
				self.send()
			elif choice == '6':
				self.check()
			elif choice == '7':
				return
			else:
				cls()
				print('Wrong choice, please try it again')
				self.homePage()

			
class student():
	def __init__(self, login):
		self.login = login
		self.homePage()

	def show_subjects(self):
		data = openFile()
		for i in data['students'][self.login]['courses']:
			print(i,data['courses'][i]['course'],'|','Teachers:',data['courses'][i]['teachers'])

	def see_marks(self):
		data = openFile()
		self.show_subjects()
		subject_id = input('Enter id of needed subject or (all) for all marks(_b to back): ').strip()
		if subject_id == '_b':
			return
		if subject_id == 'all':
			for i in data['students'][self.login]['courses']:
				try:
					print(data['courses'][i]['course'],'marked =',data['courses'][i]['marks'][self.login])
				except:
					print(data['courses'][i]['course'],'no mark')
			print()
			return
		if subject_id in data['students'][self.login]['courses']:
			try:
				print(data['courses'][subject_id]['course'],'marked =',data['courses'][subject_id]['marks'][self.login])	
			except:
				print('Teacher did not mark yet!')
		else:
			print('Enter valid subject id')
			self.see_marks()

	def show_free_courses(self):
		admin.show_courses(None,False)

	def enroll(self):
		data = openFile()
		self.show_free_courses()
		course_id = input('Enter id of needed course: ').strip()
		try:
			if data['courses'][course_id]['limitation']>len(data['courses'][course_id]['students']):
				x = admin.attach(None,'students',course_id,self.login)
				if x==None:
					print('Already attached')
				elif x:
					print('Done!')
				else:
					print('Wrong data!')
			else:
				print('No spaces in free course (it is full):')
		except:
			print('Wrong data!')
			return

	def unenroll(self):
		option = []
		data = openFile()
		for i in data['students'][self.login]['courses']:
			if data['courses'][i]['limitation']>0:
				print(i,data['courses'][i]['course'])
				option.append(i)
		if len(option)==0:
			print('You are not participating any free course!')
			return
		course_id = input('Enter id of needed course: ').strip()
		try:
			data['students'][self.login]['courses'].remove(course_id)
			data['courses'][course_id]['students'].remove(self.login)
			writeFile(data)
			print('Done!')
			return
		except:
			print('Wrong data!')
			return

	def rate(self):
		admin.show(None,'teachers')
		data = openFile()
		login = input('Enter login of needed teacher: ').strip()
		if login in data['teachers']:
			if not self.login in data['teachers'][login]['rating']:
				point = input('Enter rating: ').strip()
				data['teachers'][login]['rating'][self.login] = point
				print('Rated!')
				writeFile(data)
				return
			else:
				print('Already rated')
				return
		else:
			print('Wrong login')
			return

	def send(self):
		data = openFile()
		for i in data['users']:
			if i=="count" or i == "admin":
				continue
			print('User login: ',i)
		login = input('Enter needed login: ').strip()
		message = input ('Enter message: \n').strip()
		if send(self.login,login,message):
			print('Send!')
		else:
			print('Wrong data!')
		return

	def homePage(self):
		while True:
			print('''Home page. Student - {}

Select an action:
1. Enroll/Unenroll to/from free courses
2. See marks
3. See teachers
4. See free courses to enroll
5. Rate teacher
6. Send message
7. Check inbox
8. Exit
'''.format(self.login))
			choice = input().strip()
			if choice == '1':
				choice = input('Choose Enroll(e) or Unenroll(u): ').strip()
				if choice=='e':
					self.enroll()
				elif choice == 'u':
					self.unenroll()
				else:
					print('Wrong choice!')
					continue
			elif choice == '2':
				self.see_marks()
			elif choice == '3':
				admin.show(None,'teachers')			
			elif choice == '4':
				self.show_free_courses()
			elif choice == '5':
				self.rate()
			elif choice == '6':
				self.send()
			elif choice == '7':
				self.check()
			elif choice == '8':
				return
			else:
				cls()
				print('Wrong choice, please try it again')
				self.homePage()	

def checkAdminUsers():
	data = openFile()
	if (not "admin" in data['users']):
		users("admin",str(random.randint(100,999)),0)

def createJSON():
	if os.path.exists('dict.json')==False:
		s = """
		{
			"users":{
				"count" : 0
			},
			"teachers":{
				"count" : 0
			},
			"students":{
				"count" : 0
			},
			"courses":{
				"count" : 0,
				"count_static" : 0
			}			
		}
		"""
		with open('dict.json', 'w') as file:
			json.dump(json.loads(s),file,indent=3)
		print('dict.json file has been created!')

def sign_in():
	createJSON()
	checkAdminUsers()
	login = input("Enter user login (q - if you want exit): ").strip()
	if login == 'q':
		sys.exit()
	password = getpass.getpass("Enter the password: ")  #Works in command line
	#password = input("Enter the password: ").strip()
	data = openFile()
	try:
		usertype = -1
		if data['users'][login]['password'] == password:
			usertype = data['users'][login]['usertype']
	except:
		print('Wrong data! Try again')
	else:
		cls() #Works in command line 
		if usertype == 0:
			admin(login)
		elif usertype == 1:
			teacher(login)
		elif usertype == 2:
			student(login)
		else:
			print('Wrong data! Try again')
	return sign_in()

sign_in()