
from functions.write_file import write_file

def main():

    re = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(re)
    re = write_file("calculator", "pkg/jibon_ektai/morelorem.txt", "jibon ektai lorem ipsum dolor sit amet")
    print (re)
    re = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print (re)
    re = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(re)

main()
