import os
import re
import csv
import logging
import javalang

rroot = ''
croot = ''
repos = os.listdir(rroot)
comment = os.listdir(croot)

logging.basicConfig(
        #filename='new.log',
        #filemode='w',
        format="%(asctime)s (Process %(process)d) [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        level=logging.INFO)

def get_path(repo):
    rroot = ''
    croot = ''
    repos = os.listdir(rroot)
    comment = os.listdir(croot)
    if repo in repos:
        return rroot + repo
    elif repo in comment:
        return croot + repo


def check_author_tag(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                    javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', content)
                except:
                    continue
                for javadoc in javadocs:
                    if '@author' in javadoc:
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
    return results


def check_since_tag(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                    javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', content)
                except:
                    continue
                for javadoc in javadocs:
                    if '@since' in javadoc:
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
    return results


def check_todo(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                    javadocs = re.findall(r'/\*([\s\S]*?)\*/', content)
                except:
                    continue
                for javadoc in javadocs:
                    if 'todo' in javadoc.lower() or 'fixme' in javadoc.lower():
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
                lines = content.split('\n')
                for line in lines:
                    if '//' in line:
                        if line.startswith('//'):
                            comment = line.lower()
                        else:
                            comment = "//" + line.split('//')[1].lower()
                        if 'todo' in comment or 'fixme' in comment:
                            results.append((repo, root + os.sep + file, comment ))
    return results


def iscode(code):
    code = 'public class Test{  public static void main(){' + code + '}}'
    try:
        tree = javalang.parse.parse(code)
        return True
    except:
        return False

def check_commented_code(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                    javadocs = re.findall(r'/\*([\s\S]*?)\*/', content)
                except:
                    continue
                for javadoc in javadocs:
                    if javadoc.strip() and iscode(javadoc):
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
                lines = content.split('\n')
                for i in range(len(lines)):
                    line = lines[i]
                    if '//' in line:
                        if line.startswith('//'):
                            comment = line.replace('//','',1)
                        else:
                            comment = line.split('//')[1]
                        if comment.strip() and iscode(comment):
                            results.append((repo, root + os.sep + file +':' + str(i+1), comment))
    return results


def check_class(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root.lower() + os.sep + file.lower():
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.readlines()
                
                except:
                    continue
                linenunm = 0
                for i in range(len(content)-1):
                    if content[i].strip().startswith('/*') or content[i].strip().startswith('*') or content[i].strip().startswith('//'):
                        continue
                    if 'class' in content[i] or 'interface' in content[i] or 'enum' in content[i]:
                        if '{' in content[i] or '{' in content[i+1]:
                            linenunm = i
                            break
                header = ''
                if linenunm == 0:
                    continue
                for i in range(linenunm):
                    header = header + content[i] + '\n'
                javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', header)
                if not javadocs:
                    if 'test' not in file.lower():
                        results.append((repo, root + os.sep + file))
                    
    return results

def check_public_method(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root + os.sep + file:
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                except:
                    continue
                public_methods = re.findall(r'public ([a-zA-Z0-9_ ]*?)\(([a-zA-Z0-9_ ]*?)\)[\s\S]*?\{[\s\S]*?\}', content)
                for m in public_methods:
                    if 'get' in m[0] or 'set' in m[0] or 'boolean is' in m[0]:
                        continue
                    if len(m[0].split()) == 1:
                        continue
                    method = 'public ' + m[0] + '('
                    check = content.split(method)[0].split('\n')
                    if len(check) < 4:
                        continue
                    if '*/' in check[-1] or '*/' in check[-2] or '*/' in check[-3] or '*/' in check[-4]:
                        continue
                    if '@Override' in check[-1] or '@Override' in check[-2] or '@Override' in check[-3] or '@Override' in check[-4]:
                        continue
                    else:
                        results.append((repo, root + os.sep + file, 'public ' + m[0]))

    return results

def check_code_tag(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root + os.sep + file:
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                    javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', content)
                except:
                    continue
                for javadoc in javadocs:
                    lines = javadoc.split('\n')
                    for line in lines:
                        line = line.replace('*','').strip()
                        if line and iscode(line):
                            results.append((repo, root + os.sep + file, "/**" + javadoc + "*/",line))
                            break
    return results

def check_class_author(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root + os.sep + file:
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.readlines()
                
                except:
                    continue
                linenunm = 0
                for i in range(len(content)-1):
                    if content[i].strip().startswith('/*') or content[i].strip().startswith('*') or content[i].strip().startswith('//'):
                        continue
                    if 'class' in content[i] or 'interface' in content[i] or 'enum' in content[i]:
                        if '{' in content[i] or '{' in content[i+1]:
                            linenunm = i
                            break
                header = ''
                if linenunm == 0:
                    continue
                for i in range(linenunm):
                    header = header + content[i] + '\n'
                javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', header)
                if not javadocs:
                    continue
                else:
                    javadoc = javadocs[0]
                    if '@author' in javadoc:
                        continue
                    else:
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
                    
    return results

def check_class_since(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root + os.sep + file:
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.readlines()
                
                except:
                    continue
                linenunm = 0
                for i in range(len(content)-1):
                    if content[i].strip().startswith('/*') or content[i].strip().startswith('*') or content[i].strip().startswith('//'):
                        continue
                    if 'class' in content[i] or 'interface' in content[i] or 'enum' in content[i]:
                        if '{' in content[i] or '{' in content[i+1]:
                            linenunm = i
                            break
                header = ''
                if linenunm == 0:
                    continue
                for i in range(linenunm):
                    header = header + content[i] + '\n'
                javadocs = re.findall(r'/\*\*([\s\S]*?)\*/', header)
                if not javadocs:
                    continue
                else:
                    javadoc = javadocs[-1]
                    if '@since' in javadoc or "creat" in javadoc.lower() or '@version' in javadoc:
                        continue
                    else:
                        results.append((repo, root + os.sep + file, "/**" + javadoc + "*/"))
                    
    return results

def check_override(repo):
    results = []
    root = get_path(repo)
    os.chdir(root)
    for root, dirs, files in os.walk(root):
        for file in files:
            if 'test' in root + os.sep + file:
                continue
            if file.endswith('.java'):
                logging.info(
                    "Checking file {}  {}".format(repo, root + os.sep + file))

                try:
                    f = open(root + os.sep + file,'r',encoding='utf-8',errors='ignore')
                    content = f.read()
                except:
                    continue
                public_methods = re.findall(r'public ([a-zA-Z0-9_ ]*?)\(([a-zA-Z0-9_ ]*?)\)[\s\S]*?\{[\s\S]*?\}', content)
                for m in public_methods:
                    if len(m[0].split()) == 1:
                        continue
                    method = 'public ' + m[0] + '('
                    check = content.split(method)[0].split('\n')
                    if len(check) < 3:
                        continue
                    if '@Override' in check[-1] or '@Override' in check[-2] or '@Override' in check[-3]:
                        if '*/' in check[-1] or '*/' in check[-2] or '*/' in check[-3]:
                            results.append((repo, root + os.sep + file, 'public ' + m[0]))
                    
    return results


if __name__ == "__main__":
    
    of = open("sampled_repos.csv", 'r', encoding='UTF-8', errors='ignore')
    reader = csv.reader(of)
    output = open("violations.csv",'w', encoding='UTF-8', errors='ignore',newline='')
    writer = csv.writer(output)
    for item in reader:
        if 'where->general_rules->explicit->all_classes' in item[7]:
            results = check_class(item[0].replace('/','_'))
            for r in results:
                writer.writerow([r[0],r[1]])
    