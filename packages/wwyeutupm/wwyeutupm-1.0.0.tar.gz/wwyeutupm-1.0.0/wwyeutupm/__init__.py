def ipyFile(filename):
    file = open(filename+'.py', 'w+')
    return file

def ithisFile(filename):
    thisFile = open(filename+'py', 'w+')

def iready(thisfile, file):
    lines = thisfile.readlines()
    body = lines[:-1]
    thisfile.truncate(0)
    thisfile.write(f"from {file} import *\n{body}")

def eclosePyFile(file):
    file.close()