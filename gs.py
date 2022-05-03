#git shortcut main
import os
import subprocess
from git_path import GitPath

MIN_OPTIONS = -4
MAX_OPTIONS = 2

def main():
    print(GitPath.plat)
    option = -999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = user_options()

    if option != 0:
        # setting up paths to directories - no matter what the option!
        if not GitPath.path_loaded:
            try:
                f = open(GitPath.SAVE_PATH)
                GitPath.load_path(f)

                f.close()
            except FileNotFoundError:
                GitPath.new_path()

        run_commands(option)
    
    return option

def user_options():
    print("WARNING: Make sure to put this outside of your git project!")
    choice = int(input(
                   "#)  Option\n" +
                   "1)  git branch > <file>\n" +
                   "2)  git diff > <file>\n" +
                   "0)  Exit\n" +
                   "-1) Change Path\n" +
                   "-2) Open cmd in directory\n" +
                   "-3) Open git-bash in directory\n" + 
                   "-4) Explore Git repository directory\n" +
                   "Choice: "
                ))

    return choice

def run_commands(option):
    if option == 1:
        cmd_to_txt("branch")
    elif option == 2:
        cmd_to_txt("diff")
    elif option == -1:
        GitPath.new_path()
    elif option == -2:
        cmd_at_path("start cmd.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -3:
        cmd_at_path("start git-bash.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -4:
        explore_at_path()

def cmd_to_txt(command):
    # creating text file to write branches to
    GitPath.txt_file = input("file: ")
    if GitPath.txt_file.find(".") == -1:
        GitPath.txt_file += ".txt"

    os.chdir(GitPath.path)
    if GitPath.plat == "Windows":
        os.system("git " + command + " > \"" + GitPath.curr_dir + "\\" + GitPath.txt_file + "\"")
    else:
        os.system("git " + command + " > \"/" + GitPath.curr_dir + "/" + GitPath.txt_file + "\"")
    os.chdir(GitPath.curr_dir)
    app_cmd = "notepad " if GitPath.plat == "Windows" else "open -a TextEdit "
    os.system(app_cmd + GitPath.txt_file)

def cmd_at_path(app):
    os.chdir(GitPath.path)
    os.system(app)
    os.chdir(GitPath.curr_dir)

def explore_at_path():
    if GitPath.plat == "Windows":
        path = os.path.realpath(GitPath.path)
        os.startfile(path)
    else: 
        os.system("open %s" % GitPath.path)

if __name__ == '__main__':
    retVal = main()
    while retVal < 0:
        retVal = main()