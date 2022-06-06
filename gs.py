#git shortcut main
import os
from git_path import GitPath
from style import Color

MIN_OPTIONS = -6
MAX_OPTIONS = 5

def main():
    # keeping this because it is useful to know which OS version is running
    print(Color.string(Color.BOLD + Color.GREEN + Color.UNDERLINE, "Version: " + GitPath.plat))

    # setting to very low value to make sure it runs at least once
    option = -999999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = user_options()

    if option != 0:
        run_commands(option)
    
    return option

def user_options():
    print(Color.string(Color.BOLD + Color.RED, "WARNING: Make sure to put this outside of your git project!"))
    choice = int(input(
                   Color.string(Color.BOLD + Color.GREEN, "#)  Option\n") +
                   Color.string(Color.BOLD + Color.GREEN, "GIT SHORTCUTS:\n") + 
                   "1)  git branch > <file>\n" +
                   "2)  git diff > <file>\n" +
                   "3)  git checkout <list_of_branches>\n" +
                   "4)  git branch -D <list_of_branches>\n" +
                   "5)  git branches from remote\n" + 
                   "0)  Exit\n" +
                   Color.string(Color.BOLD + Color.GREEN, "MISC SHORTCUTS:\n") +
                   "-1) Add Path\n" +
                   "-2) Change Path\n" +
                   "-3) Remove Path\n" + 
                   "-4) Open cmd in <" + Color.string(Color.DARKCYAN, GitPath.path) + ">\n" +
                   "-5) Open git-bash in <" + Color.string(Color.DARKCYAN, GitPath.path) + ">\n" +
                   "-6) Explore Git repo\n" +
                   Color.string(Color.GREEN, "Choice: ")
                ))

    return choice

def run_commands(option):
    match option:
        case 1:
            GitPath.cmd_to_txt("branch", True)
        case 2:
            GitPath.cmd_to_txt("diff", True)
        case 3:
            git_cmd_shortcut("checkout")
        case 4:
            git_cmd_shortcut("branch -D")
        case 5:
            retrieve_branches_from_remote()
        case -1:
            GitPath.new_path()
        case -2:
            GitPath.pick_path(GitPath.SAVE_PATH)
        case -3:
            GitPath.remove_path(GitPath.SAVE_PATH)
        case -4:
            GitPath.cmd_at_path("start cmd.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
        case -5:
            GitPath.cmd_at_path("start git-bash.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
        case -6:
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
    while GitPath.pick_path(GitPath.SAVE_PATH) == False:
        print(Color.string(Color.RED, "Something went wrong with picking/creating a path...\nTry again."))
    retVal = main()
    while retVal != 0:
        retVal = main()