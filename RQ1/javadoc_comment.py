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


path = ""
files = os.listdir( path )
outputfile = open('javadoc_comment.csv','w', encoding='UTF-8',errors='ignore',newline='')
writer = csv.writer(outputfile)
'''
outputfile = open('javadoc_comment.csv','w', encoding='UTF-8',errors='ignore',newline='')
outputfile1 = open('javadoc_comment_add_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
outputfile2 = open('javadoc_comment_delete_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
writer = csv.writer(outputfile)
writer1 = csv.writer(outputfile1)
writer2 = csv.writer(outputfile2)
outputfile3 = open('javadoc_comment_update_withoutcode.csv','w', encoding='UTF-8',errors='ignore',newline='')
writer3 = csv.writer(outputfile3)
'''
for f in files:
	print(f[:-4])
	inputfile = open(path+'/'+f,'r',encoding='UTF-8',errors='ignore')
	reader = csv.reader( (line.replace('\0','') for line in inputfile))
	openfile = open('/woc4_fast/ind_file/'+f[:-4] + '.txt','r',encoding='UTF-8',errors='ignore')
	allindf = openfile.read().splitlines()
	openfile.close()
	openfile = open('/woc4_fast/ind_com/'+f[:-4] + '.txt','r',encoding='UTF-8',errors='ignore')
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
		flag = 0
		addflag = 0
		delflag = 0
		add_code = item[4].replace('+','').strip()
		if add_code != '':
			flag = 1
		delete_code = item[5].replace('-','').strip()
		if delete_code != '':
			flag = 1
		if item[2].replace('*','').replace('+','').strip() != '':
			addflag = 1
		if item[3].replace('*','').replace('-','').strip() != '':
			delflag = 1

		if addflag > 0 and delflag>0:
			update = update + 1
			if flag == 0:
				update_nocode = update_nocode + 1
				#writer3.writerow([f[:-4],item[0],item[1],item[2],item[3]])
				if item[0] in allindc:
					update_indc = update_indc + 1
				if item[0] +',' + item[1] in allindf:
					update_indf = update_indf + 1
		elif addflag > 0 and delflag == 0:
			add = add + 1
			if flag == 0:
				add_nocode = add_nocode + 1
				#writer1.writerow([f[:-4],item[0],item[1],item[2],item[3]])
				if item[0] in allindc:
					add_indc = add_indc + 1
				if item[0] +',' + item[1] in allindf:
					add_indf = add_indf + 1
		elif delflag > 0 and addflag == 0:
			delete = delete + 1
			if flag == 0:
				delete_nocode = delete_nocode + 1
				#writer2.writerow([f[:-4],item[0],item[1],item[2],item[3]])
				if item[0] in allindc:
					delete_indc = delete_indc + 1
				if item[0] +',' + item[1] in allindf:
					delete_indf = delete_indf + 1

	writer.writerow([f[:-4],add,delete,update,add_nocode,delete_nocode,update_nocode,add_indf,delete_indf,update_indf,add_indc,delete_indc,update_indc])
	outputfile.flush()
