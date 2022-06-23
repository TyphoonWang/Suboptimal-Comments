import re
import csv
import os
import sys

path1 = ""
dirs1 = os.listdir(path1)
path2 = ""
dirs2 = os.listdir(path2)

def get_diff(path,f):
	print(f[:-4])
	openfile = open(path+'/'+f,'r', encoding='UTF-8',errors='ignore')
	reader = csv.reader( (line.replace('\0','') for line in openfile))
	outputfile = open(''+f,'w', encoding='UTF-8',errors='ignore',newline='')
	writer = csv.writer(outputfile)
	if f[:-4] in dirs1:
		os.chdir(path1 + '/' + f[:-4])
	elif f[:-4] in dirs2:
		os.chdir(path2 + '/' + f[:-4])
	cache = []
	for item in reader:
		change = item[0] + item[1]
		if change in cache:
			continue
		flag = 0
		add = item[4].split('\n')
		delete = item[5].split('\n')
		for line in add:
			if '/**' in line or line.startswith('*') or '*/' in line:
				flag = 1
				break
		for line in delete:
			if '/**' in line or line.startswith('*') or '*/' in line:
				flag = 1
				break
		if flag == 1:
			try:
				cache.append(change)
				pip = os.popen("git show -p -U100000 " + item[0] + ' -- ' + item[1].replace('/','',1))
				blames = pip.buffer.read().decode(encoding='utf8',errors='ignore').split('\n')
				parse(item[0],item[1],blames,writer)
			except Exception as e:
				print(e)

def parse(commit,filename,lines,writer):
	endnum = len(lines)
	i = 0
	flag = 0
	while i < endnum:
		if flag == 0:
			if lines[i].startswith('@@'):
				i = i+3
				flag = 1
				continue
		if '/**' in lines[i]:
			addcomment = ''
			deletecomment = ''
			addcode = ''
			deletecode = ''
			if lines[i].startswith('+'):
				addcomment = addcomment + lines[i] +'\n'
			elif lines[i].startswith('-'):
				deletecomment = deletecomment + lines[i] +'\n'
			while not '*/' in lines[i]:
				i =i+1
				if lines[i].startswith('+'):
					addcomment = addcomment + lines[i] +'\n'
				elif lines[i].startswith('-'):
					deletecomment = deletecomment + lines[i] +'\n'
			if lines[i].startswith('+') and lines[i+1].startswith('-'):
				cur = i + 1
				curdelete = ''
				while lines[cur].startswith('-'):
					curdelete = curdelete + lines[cur] +'\n'
					cur =cur + 1
				if '*/' in curdelete:
					i = cur-1
					deletecomment = deletecomment+curdelete +'\n'
			if addcomment != '' or deletecomment != '':
				if '{' in lines[i+1] or '{' in lines[i+2]:
					cur = i+1
					depth = 0 
					if lines[cur].startswith('+'):
						addcode = addcode + lines[cur]  +'\n'
						depth = depth +lines[cur].count('{') - lines[cur].count('}')
					elif lines[cur].startswith('-'):
						deletecode = deletecode + lines[cur]  +'\n'
					else:
						if '//' in lines[cur]:
							line = re.split(r'//',lines[cur])[0]
						else:
							line = lines[cur]
						depth = depth + line.count('{') - line.count('}')
					cur = cur + 1
					if lines[cur].startswith('+'):
						addcode = addcode + lines[cur]  +'\n'
						depth = depth +lines[cur].count('{') - lines[cur].count('}')
					elif lines[cur].startswith('-'):
						deletecode = deletecode + lines[cur]  +'\n'
					else:
						if '//' in lines[cur]:
							line = re.split(r'//',lines[cur])[0]
						else:
							line = lines[cur]
						depth = depth + line.count('{') - line.count('}')
					cur = cur + 1
					while depth > 0:
						if lines[cur].startswith('+'):
							addcode = addcode + lines[cur]  +'\n'
							depth = depth +lines[cur].count('{') - lines[cur].count('}')
						elif lines[cur].startswith('-'):
							deletecode = deletecode + lines[cur]  +'\n'
						else:
							if '//' in lines[cur]:
								line = re.split(r'//',lines[cur])[0]
							else:
								line = lines[cur]
							depth = depth + line.count('{') - line.count('}')
						cur = cur + 1
					writer.writerow([commit,filename,addcomment,deletecomment,addcode,deletecode])
					


		i = i+1


if __name__=="__main__":
	maxInt = sys.maxsize

	while True:
		# decrease the maxInt value by factor 10 
		# as long as the OverflowError occurs.
		try:
			csv.field_size_limit(maxInt)
			break
		except OverflowError:
			maxInt = int(maxInt/10)

	path = ""
	files = os.listdir( path )
	for f in files:
		get_diff(path,f)

