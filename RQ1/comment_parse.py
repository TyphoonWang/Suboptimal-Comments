import sys
import os
import csv
import re
from comment_parser import comment_parser

def parsecomment(code):
	try:
		comments = comment_parser.extract_comments_from_str(code,mime = 'text/x-java-source')
	except:
		count = 0
		codelines = code.split('\n')
		flag = 1
		for line in codelines:
			if line.strip().startswith('*'):
				if flag:
					count = count + 1
					flag = 0
			else:
				flag = 1
			if '//' in line:
				try:
					tmp = comment_parser.extract_comments_from_str(line,mime = 'text/x-java-source')
					count = count + len(tmp)
				except:
					pass
		return count

	if len(comments) == 0:
		count = 0
		codelines = code.split('\n')
		flag = 1
		for line in codelines:
			if line.strip().startswith('*'):
				if flag:
					count = count + 1
					flag = 0
			else:
				flag = 1
		return count
	else:
		return len(comments)

def diff_parse(path,project,outputfile):
	logfile = open(path+'/'+project,'r', encoding='UTF-8',errors='ignore')
	lines = logfile.readlines()
	recordfile = open(''+project[:-4]+'.csv','w', encoding='UTF-8',errors='ignore',newline='')
	writer = csv.writer(recordfile)

	commit = ''
	flag = 0
	sflag = 0
	content = ''
	add = ''
	delete = ''
	filename = ''
	number = [0,0,0]
	cnt = 0
	yes = 0
	no = 0
	start = 0
	offset = 0
	for i in range(0,len(lines)):
		line = lines[i]
		if line.startswith('commit '):
			
			
			if flag:
				anum = parsecomment(add)
				dnum = parsecomment(delete)
				if anum + dnum > 0:
					if anum == dnum:
						try:
							addcomments = comment_parser.extract_comments_from_str(add,mime = 'text/x-java-source')
							delcomments = comment_parser.extract_comments_from_str(delete,mime = 'text/x-java-source')
							myflag = 0
							if len(addcomments) > 0 and len(addcomments) == len(delcomments):
								for i in range(0,len(addcomments)):
									if addcomments[i].text().strip() != delcomments[i].text().strip():
										myflag = 1
										break
								if myflag == 0:
									flag = 0
									add = ''
									delete = ''
									continue
						except:
							pass
					yes = yes + anum
					no = no + dnum
					writer.writerow([commit,filename,anum,dnum,add,delete,start,offset])
					if dnum ==0 :
						number[0] = number[0] +1
					elif anum == 0:
						number[1] = number[1] + 1
					else:
						number[2] = number[2] + 1

				flag = 0
				add = ''
				delete = ''
			commit = line.strip().split(' ')[-1]
			continue
			commit = line.strip().split(' ')[-1]

		if line.startswith('diff --git '):
			if flag:
				anum = parsecomment(add)
				dnum = parsecomment(delete)
				if anum + dnum > 0:
					if anum == dnum:
						try:
							addcomments = comment_parser.extract_comments_from_str(add,mime = 'text/x-java-source')
							delcomments = comment_parser.extract_comments_from_str(delete,mime = 'text/x-java-source')
							myflag = 0
							if len(addcomments) > 0 and len(addcomments) == len(delcomments):
								for i in range(0,len(addcomments)):
									if addcomments[i].text().strip() != delcomments[i].text().strip():
										myflag = 1
										break
								if myflag == 0:
									flag = 0
									add = ''
									delete = ''
									continue
						except:
							pass
					yes = yes + anum
					no = no + dnum
					writer.writerow([commit,filename,anum,dnum,add,delete,start,offset])
					if dnum ==0 :
						number[0] = number[0] +1
					elif anum == 0:
						number[1] = number[1] + 1
					else:
						number[2] = number[2] + 1
				flag = 0
				add = ''
				delete = ''
			filea = line.strip().split(' ')[-2]
			fileb = line.strip().split(' ')[-1]
			if filea.split('.')[-1] == 'java' or fileb.split('.')[-1] == 'java':
				if filea == '/dev/null' or fileb == '/dev/null':
					continue
				flag = 1
				cnt = cnt+1
				filename = filea.replace('a','',1)

		if flag:
			if line.startswith('+++') or line.startswith('---'):
				if "/dev/null" in line:
					flag = 0
					cnt = cnt-1
				continue
			elif line.startswith('+'):
				add = add + line.replace('+','',1)
				sflag = 1
			elif line.startswith('-'):
				delete = delete + line.replace('-','',1)
				sflag = 1
			elif sflag and line.startswith('@@'):
				anum = parsecomment(add)
				dnum = parsecomment(delete)
				if anum + dnum > 0:
					if anum == dnum:
						try:
							addcomments = comment_parser.extract_comments_from_str(add,mime = 'text/x-java-source')
							delcomments = comment_parser.extract_comments_from_str(delete,mime = 'text/x-java-source')
							myflag = 0
							if len(addcomments) > 0 and len(addcomments) == len(delcomments):
								for i in range(0,len(addcomments)):
									if addcomments[i].text().strip() != delcomments[i].text().strip():
										myflag = 1
										break
								if myflag == 0:
									flag = 0
									add = ''
									delete = ''
									continue
						except:
							pass
					
					yes = yes + anum
					no = no + dnum
					writer.writerow([commit,filename,anum,dnum,add,delete,start,offset])
					if dnum ==0 :
						number[0] = number[0] + 1
					elif anum == 0:
						number[1] = number[1] + 1
					else:
						number[2] = number[2] + 1

				sflag = 0
				add = ''
				delete = ''
				searchObj = re.search('\+([0-9]*),([0-9]*)',line)
				if searchObj:
					start = searchObj.group(1)
					offset = searchObj.group(2)


	print(project)
	#outputfile.write(project[:-4] + ',' + str(cnt) + ',' + str(number[0] + number[1] + number[2]) + ',' + str(number[0]) + ',' + str(number[1]) + ',' +str(number[2])
	#	+ ',' + str(yes) + ',' + str(no) + '\n')
	#print(yes,no)
	#dataframe = pd.DataFrame({'commit_sha':commits,'filename':files,'add':addnum,'delete':delnum})
	#dataframe.to_csv(project+".csv",index=True,header=False,sep=',',mode='w')


path = ""
files = os.listdir( path )
ff = 1
outputfile = open('snippet_granularity.txt','a')
for f in files:
	diff_parse(path,f,outputfile)
	outputfile.flush()
outputfile.close()
