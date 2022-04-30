#git shortcut main
import os
import sys
from tkinter.tix import MAX

MIN_OPTIONS = -1
MAX_OPTIONS = 2

class GitPath:
    curr_dir = os.getcwd()
    path = ""
    txt_file = ""
    save_path = "path.txt"

def main():
    option = -999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = user_options()

    # setting up paths to directories
    try:
        f = open(GitPath.save_path)
        load_path(f)

        f.close()
    except FileNotFoundError:
        new_path()

    if option == 1:
        cmd_to_txt("branch")
    elif option == 2:
        cmd_to_txt("diff")
    elif option == -1:
        new_path()
    
    return option

def user_options():
    print("WARNING: Make sure to put this outside of your git project!")
    choice = int(input("#) Option\n" +
                   "1) git branch > <file>\n" +
                   "2) git diff > <file>\n" +
                   "0) Exit\n" +
                   "-1) Change Path\n" +
                   "Choice: "))

    return choice

def new_path():
    GitPath.path = input("path: ")

    file = open(GitPath.save_path, "w")
    file.write(GitPath.path)
    file.close()

def load_path(file):
    GitPath.path = file.readline()

def cmd_to_txt(command):
    # creating text file to write branches to
    GitPath.txt_file = input("file: ")
    if GitPath.txt_file.find(".") == -1:
        GitPath.txt_file += ".txt"

    os.chdir(GitPath.path)
    os.system("git " + command + " > \"" + GitPath.curr_dir + "\\" + GitPath.txt_file + "\"")
    os.chdir(GitPath.curr_dir)
    os.system("notepad " + GitPath.txt_file)

if __name__ == '__main__':
    retVal = main()
    while retVal < 0:
        retVal = main()