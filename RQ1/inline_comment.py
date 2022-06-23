import sys
import csv
import re
import os

maxInt = sys.maxsize

while True:
    try:
       csv.field_size_limit(maxInt)
       break
    except OverflowError:
        maxInt = int(maxInt/10)


path = 
files = os.listdir( path )
#outputfile = open('inline_comment.csv','w', encoding='UTF-8',errors='ignore',newline='')
#outputfile1 = open('inline_comment_add_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
#outputfile2 = open('inline_comment_delete_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
#outputfile3 = open('inline_comment_update_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
#writer = csv.writer(outputfile)
#writer1 = csv.writer(outputfile1)
#writer2 = csv.writer(outputfile2)
#writer3 = csv.writer(outputfile3)

outputfile2 = open('what_comment.csv','w', encoding='UTF-8',errors='ignore',newline='')
writer2 = csv.writer(outputfile)

for f in files:
	print(f[:-4])
	inputfile = open(path+'/'+f,'r',encoding='UTF-8',errors='ignore')
	reader = csv.reader( (line.replace('\0','') for line in inputfile))
	openfile = open(''+f[:-4] + '.txt','r',encoding='UTF-8',errors='ignore')
	allindf = openfile.read().splitlines()
	openfile.close()
	openfile = open(''+f[:-4] + '.txt','r',encoding='UTF-8',errors='ignore')
	allindc = openfile.read().splitlines()
	openfile.close()
	add = 0
	delete = 0
	update = 0
	add_nocode = 0
	delete_nocode = 0
	update_nocode = 0
	add_indf = 0
	delete_indf = 0
	update_indf = 0
	add_indc = 0
	delete_indc = 0
	update_indc = 0
	for item in reader:
		start = int(item[6])
		if start == 1:
			continue
		addlines = item[4].split('\n')
		dellines = item[5].split('\n')
		flag = 0
		add_comment = 0
		delete_comment = 0
		for line in addlines:
			line= line.strip()
			if line == '':
				continue
			if line.startswith('*'):
				continue
			elif '/*' in line and not '/**' in line:
				add_comment = add_comment + 1
			elif '*/' in line:
				continue
			elif '//' in line:
				if line.startswith('//'):
					if line in item[5]:
						continue
					else:
						add_comment = add_comment + 1
				else:
					tmp = re.split(r'//',line,maxsplit=1)
					if tmp[1] in item[5]:
						continue
					elif tmp[0] in item[5]:
						add_comment = add_comment + 1
					else:
						add_comment = add_comment + 1
						flag = 1
			else:
				flag = 1
		for line in dellines:
			line= line.strip()
			if line == '':
				continue
			if line.startswith('*'):
				continue
			elif '/*' in line and not '/**' in line:
				delete_comment = delete_comment + 1
			elif '*/' in line:
				continue
			elif '//' in line:
				if line.startswith('//'):
					if line in item[4]:
						continue
					else:
						delete_comment = delete_comment + 1
				else:
					tmp = re.split(r'//',line,maxsplit=1)
					if tmp[1] in item[4]:
						continue
					elif tmp[0] in item[4]:
						delete_comment = delete_comment + 1
					else:
						delete_comment = delete_comment + 1
						flag = 1
			else:
				flag = 1

		if add_comment > 0 and delete_comment>0:
			update = update + 1
			if flag == 0:
				update_nocode = update_nocode + 1
				#writer3.writerow([f[:-4],item[0],item[1],item[4],item[5]])
				if item[0] in allindc:
					update_indc = update_indc + 1
				if item[0] +',' + item[1] in allindf:
					update_indf = update_indf + 1
		elif add_comment > 0 and delete_comment == 0:
			add = add + 1
			if flag == 0:
				add_nocode = add_nocode + 1
				#writer1.writerow([f[:-4],item[0],item[1],item[4],item[5]])
				if item[0] in allindc:
					add_indc = add_indc + 1
				if item[0] +',' + item[1] in allindf:
					add_indf = add_indf + 1
		elif delete_comment > 0 and add_comment == 0:
			delete = delete + 1
			if flag == 0:
				delete_nocode = delete_nocode + 1
				#writer2.writerow([f[:-4],item[0],item[1],item[4],item[5]])
				if item[0] in allindc:
					delete_indc = delete_indc + 1
				if item[0] +',' + item[1] in allindf:
					delete_indf = delete_indf + 1
		if flag == 1 and item[0] +',' + item[1] in allindf:
			writer2.writerow([f[:-4],item[0],item[1],item[4],item[5]])

	#writer.writerow([f[:-4],add,delete,update,add_nocode,delete_nocode,update_nocode,add_indf,delete_indf,update_indf,add_indc,delete_indc,update_indc])
	#outputfile.flush()
