#git shortcut main
import os
import subprocess
from threading import local
from git_path import GitPath

MIN_OPTIONS = -4
MAX_OPTIONS = 5

def main():
    # keeping this because it is useful to know which OS version is running
    print("Version: " + GitPath.plat)
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
                   "GIT SHORTCUTS:\n" +
                   "1)  git branch > <file>\n" +
                   "2)  git diff > <file>\n" +
                   "3)  git checkout <list_of_branches>\n" +
                   "4)  git branch -D <list_of_branches>\n" +
                   "5)  git branches from remote\n" + 
                   "0)  Exit\n" +
                   "MISC SHORTCUTS:\n" +
                   "-1) Change Path\n" +
                   "-2) Open cmd in directory\n" +
                   "-3) Open git-bash in directory\n" + 
                   "-4) Explore Git repo\n" +
                   "Choice: "
                ))

    return choice

def run_commands(option):
    if option == 1:
        GitPath.cmd_to_txt("branch", True)
    elif option == 2:
        GitPath.cmd_to_txt("diff", True)
    elif option == 3:
        git_cmd_shortcut("checkout")
    elif option == 4:
        git_cmd_shortcut("branch -D")
    elif option == 5:
        retrieve_branches_from_remote()
    elif option == -1:
        GitPath.new_path()
    elif option == -2:
        GitPath.cmd_at_path("start cmd.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -3:
        GitPath.cmd_at_path("start git-bash.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -4:
        explore_at_path()

def git_cmd_shortcut(cmd):
    GitPath.new_branch("branch", True)
            
    my_choice = int(input(cmd + " (integer): "))
    if my_choice < 1 or my_choice > len(GitPath.chk_dict):
        return
    
    GitPath.cmd_at_path("git " + cmd + " " + GitPath.chk_dict[my_choice])
    
    if cmd == "branch -D":
        print("deleting branch...")
        GitPath.chk_dict = {}

def retrieve_branches_from_remote():
    GitPath.new_branch("branch -r", False)
    choice = -1
    while choice < 0 or choice > 2:
        choice = int(input("Choose an option:\n" +
                   "1) Retrieve All Remote Branches\n" +
                   "2) Retrieve A Specified # of branches\n" + 
                   "0) Back to main menu"))

    if choice == 1:
        get_all_branches_remote()
    elif choice == 2:
        get_branches_remote()

def get_branches_remote():
    for key in GitPath.chk_dict:
        print(str(key) + ") " + GitPath.chk_dict[key])
    line = input("Enter #s separated by spaces: ")

    choice = ""
    for c in line:
        if c == " ":
            GitPath.add_branch_to_local(int(choice))
            choice = ""
        elif c.isdigit():
            choice += c
    GitPath.add_branch_to_local(int(choice))

def get_all_branches_remote():
    for key in GitPath.chk_dict:
        GitPath.add_branch_to_local(key)

def explore_at_path():
    if GitPath.plat == "Windows":
        path = os.path.realpath(GitPath.path)
        os.startfile(path)
    else: 
        os.system("open %s" % GitPath.path)

if __name__ == '__main__':
    retVal = main()
    while retVal != 0:
        retVal = main()