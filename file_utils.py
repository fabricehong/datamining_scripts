__author__ = 'fabrice'

def write_to_file(filename, content):
    f=open(filename, 'w')
    f.write(content)
    f.close()