#git shortcut main
# contains main function as well as specific Git functions
from random import randint, random
from style import Color
import os
from git_path import GitPath

MIN_OPTIONS = -7
MAX_OPTIONS = 6

def main(git_path):
    # keeping this because it is useful to know which OS version is running
    print(Color.string(Color.BOLD + Color.GREEN + Color.UNDERLINE, "Version: " + git_path.plat))

    # setting to very low value to make sure it runs at least once
    option = -999999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = user_options(git_path)

    if option != 0:
        run_commands(git_path, option)
    
    return {
        "git_path" : git_path,
        "option" : option
    }

def user_options(git_path):
    print(Color.string(Color.BOLD + Color.RED, "WARNING: Make sure to put this outside of your git project!"))
    choice = int(input(
                   Color.string(Color.BOLD + Color.GREEN, "#)  Option\n") +
                   Color.string(Color.BOLD + Color.GREEN, "GIT SHORTCUTS:\n") + 
                   "1)  git branch > <file>\n" +
                   "2)  git diff > <file>\n" +
                   "3)  git checkout <list_of_branches>\n" +
                   "4)  git branch -D <list_of_branches>\n" +
                   "5)  git branches from remote\n" + 
                   "6)  git checkout -b <branch_name>\n" +
                   "0)  Exit\n" +
                   Color.string(Color.BOLD + Color.GREEN, "MISC SHORTCUTS:\n") +
                   "-1) Add Path\n" +
                   "-2) Change Path\n" +
                   "-3) Remove Path\n" + 
                   "-4) Open cmd in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
                   "-5) Open git-bash in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
                   "-6) Explore Git repo\n" +
                   "-7) Refresh\n" +
                   Color.string(Color.DARKCYAN, "Current Branch: ") + Color.string(Color.CYAN, git_path.get_current_branch(False)) + "\n" +
                   Color.string(Color.GREEN, "Choice: ")
                ))

    return choice

def run_commands(git_path, option):
    match option:
        case 1:
            git_path.cmd_to_txt("branch", True)
        case 2:
            git_path.cmd_to_txt("diff", True)
        case 3:
            git_cmd_shortcut("checkout")
            git_path.get_current_branch(True)
        case 4:
            git_cmd_shortcut("branch -D")
        case 5:
            retrieve_branches_from_remote()
        case 6:
            git_create_branch("Checkout ")
            git_path.get_current_branch(True)
        case -1:
            git_path.new_path()
            git_path.get_current_branch(True)
        case -2:
            git_path.pick_path(git_path.SAVE_PATH)
            git_path.get_current_branch(True)
        case -3:
            git_path.remove_path(git_path.SAVE_PATH)
            git_path.get_current_branch(True)
        case -4:
            git_path.cmd_at_path("start cmd.exe" if git_path.plat == "Windows" else "open -a Terminal .")
        case -5:
            git_path.cmd_at_path("start git-bash.exe" if git_path.plat == "Windows" else "open -a Terminal .")
        case -6:
            git_path.explore_at_path()
        case -7:
            git_path.get_current_branch(True)
            return

def git_cmd_shortcut(cmd):
    git_path.new_branch("branch", True)
            
    my_choice = int(input(cmd + " (integer): "))
    if my_choice < 1 or my_choice > len(git_path.chk_dict):
        return
    
    git_path.cmd_at_path("git " + cmd + " " + git_path.chk_dict[my_choice])
    
    if cmd == "branch -D":
        print("deleting branch...")
        git_path.chk_dict = {}

def retrieve_branches_from_remote():
    git_path.new_branch("branch -r", False)
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
    for key in git_path.chk_dict:
        print(str(key) + ") " + git_path.chk_dict[key])
    line = input("Enter #s separated by spaces: ")

    choice = ""
    for c in line:
        if c == " ":
            git_path.add_branch_to_local(int(choice))
            choice = ""
        elif c.isdigit():
            choice += c
    git_path.add_branch_to_local(int(choice))

def get_all_branches_remote():
    for key in git_path.chk_dict:
        git_path.add_branch_to_local(key)

def git_create_branch(message):
    backup_pr = input(message + "Branch: ")
    git_path.cmd_at_path("git checkout -b " + backup_pr)

if __name__ == '__main__':
    git_path = GitPath()

    # picking path before start of program to keep track of repo
    while git_path.pick_path(git_path.SAVE_PATH) == False:
        print(Color.string(Color.RED, "Something went wrong with picking/creating a path...\nTry again."))

    git_path.get_current_branch(True)

    # calling main function as long as user does not exit prog (user enters 0)
    ret_arr = main(git_path)
    retVal = ret_arr["option"]
    git_path = ret_arr["git_path"]
    while retVal != 0:
        ret_arr = main(git_path)
        retVal = ret_arr["option"]
        git_path = ret_arr["git_path"]
