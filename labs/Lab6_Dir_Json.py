import sys
import random
import os
import shutil
import json
import string
import linecache


def deleteDirectories():
	try:
		shutil.rmtree("task1")
	except OSError as err:
		print(err)
	else:
		print("Successfully deleted")

def ex1():
	try:	
		os.mkdir("task1")
	except:
		pass
	n = int(input("Quantity of files: "))
	m = int(input("Quantity of numbers in each file: "))
	maxNum = -sys.maxsize - 1
	maxSum = -sys.maxsize - 1
	for i in range(n):
		filename='file_'+str(i)+'.txt'
		file = open(('task1/'+filename),'w')
		numbers = random.sample(range(1000), m)
		file.write(str(numbers))
		file.close()
		if maxNum < max(numbers):
			maxNumFile = filename
			maxNum = max(numbers)
		if maxSum < sum(numbers):
			maxSumFile = filename
			maxSum = sum(numbers)
	print("Maximum number maxNum ("+str(maxNum)+") is in the",maxNumFile)
	print("Maximum sum of the numbers ("+str(maxSum)+") in the",maxSumFile)

def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict) # Return value ignored.
    return results


def generate(len1=10,len2=15):
	try:	
		os.mkdir("task4")
	except:
		pass
	l = string.ascii_lowercase	
	file1 = open("task4/file_1.txt","w")
	file2 = open("task4/file_2.txt","w")
	for i in range(len1):
		s = ''.join(random.choice(l) for i in range(20))
		file1.write(s+"\n")
	for i in range(len2):
		s = ''.join(random.choice(l) for i in range(20))
		file2.write(s+"\n")
	file1.close()
	file2.close()

def ex4():
	generate()
	file1 = open("task4/file_1.txt","r")
	file2 = open("task4/file_2.txt","r")
	file3 = open("task4/file_3.txt","w")
	l1=len([0 for _ in file1])
	l2=len([0 for _ in file2])
	if l1==l2:
		with open("task4/file_1.txt","r") as f1, open("task4/file_2.txt","r") as f2, open("task4/file_3.txt","w") as fout:
			for fst, snd in zip(f1, f2):
				fout.write('{0}{1}\n'.format(fst.rstrip(), snd.rstrip()))
	else:
		ans = input("Cut the excessive lines?(Y = Yes, N = No): ")
		i = 0
		if (ans == 'Y'):
			with open("task4/file_1.txt","r") as f1, open("task4/file_2.txt","r") as f2, open("task4/file_3.txt","w") as fout:
				for fst, snd in zip(f1, f2):
					fout.write('{0}{1}\n'.format(fst.rstrip(), snd.rstrip()))
					i+=1
					if (i>=min(l1,l2)):
						break
			
		else:		
			if l1>l2:
				f = open("task4/file_2.txt","w")
				for i in range(l1):
					l = string.ascii_lowercase
					s = ''.join(random.choice(l) for i in range(20))
					f.write(s+"\n")	
			else:
				f = open("task4/file_1.txt","w")
				for i in range(l2):
					l = string.ascii_lowercase
					s = ''.join(random.choice(l) for i in range(20))
					f.write(s+"\n")	
			with open("task4/file_1.txt","r") as f1, open("task4/file_2.txt","r") as f2, open("task4/file_3.txt","w") as fout:
				for fst, snd in zip(f1, f2):
					fout.write('{0}{1}\n'.format(fst.rstrip(), snd.rstrip()))
	print("Done! Check task4/file_3.txt")


	file1.close()
	file2.close()
	file3.close()

ex1()
ex4()


# deleteDirectories()

