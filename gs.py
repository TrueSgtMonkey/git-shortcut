#git shortcut main
# contains main function as well as specific Git functions
from random import randint, random
from threading import local
from style import Color
from git_path import GitPath
from git_save import GitSaveVars
import os

TEMP_STATUS_TXT_NAME = "temp_status.txt"
TEMP_COMMIT_TXT_NAME = "___commit___.txt"
MIN_OPTIONS = -8
MAX_OPTIONS = 11

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
    user_input = ""
    print(
        Color.string(Color.BOLD + Color.GREEN, "#)  Option\n") +
        Color.string(Color.BOLD + Color.GREEN, "GIT SHORTCUTS:\n") + 
        "1)  git branch > <file>\n" +
        "2)  git rebase with " + Color.string(Color.YELLOW, GitSaveVars.rebase_branch) + "\n" +
        "3)  git checkout <list_of_branches>\n" +
        "4)  git branch -D <list_of_branches>\n" +
        "5)  git branches from remote\n" + 
        "6)  git checkout -b <branch_name>\n" +
        "7)  amend PR code review\n" +
        "8)  git push --set-upstream origin " + Color.string(Color.CYAN, git_path.get_current_branch(False)) + "\n" +
        "9)  git restore <list_of_files>\n" +
        "10) git clean\n" +
        "11) get all files altered in commit <commit-id>\n" +
        "0)  Exit\n" +
        Color.string(Color.BOLD + Color.GREEN, "MISC SHORTCUTS:\n") +
        "-1) Add Path\n" +
        "-2) Change Path\n" +
        "-3) Remove Path\n" + 
        "-4) Open cmd in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
        "-5) Open git-bash in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
        "-6) Explore Git repo\n" +
        "-7) Refresh\n" +
        "-8) Set branch to rebase with (current=" + Color.string(Color.YELLOW, GitSaveVars.rebase_branch) + ")\n" +
        Color.string(Color.DARKCYAN, "Current Branch: ") + Color.string(Color.CYAN, git_path.get_current_branch(False)) + "\n" +
        Color.string(Color.GREEN, "Choice: "),
        end=""
    )
    while user_input == "":
        user_input = input("")
    choice = int(user_input)

    return choice

def run_commands(git_path, option):
    match option:
        case 1:
            git_path.cmd_to_txt("branch", True)
        case 2:
            git_status_rebase()
        case 3:
            git_checkout_shortcut()
            git_path.get_current_branch(True)
        case 4:
            git_delete_shortcut()
            git_path.get_current_branch(True)
        case 5:
            retrieve_branches_from_remote()
        case 6:
            git_create_branch("Checkout ")
            git_path.get_current_branch(True)
        case 7:
            git_add_amend_push()
        case 8:
            git_set_upstream_origin_branch()
        case 9:
            git_restore_files()
        case 10:
            git_clean()
        case 11:
            get_all_files_from_commit()
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
        case -8:
            set_rebase_branch()

def choose_branch(message) -> int:
    count = 1
    print(message)
    print(Color.string(Color.BOLD, "(Press 0 to not do anything)"))
    for branch in git_path.get_all_branches(False):
        if count & 1 == 0:
            print("\t" + str(count) + ") " + Color.string(Color.DARKCYAN, branch))
        else:
            print("\t" + str(count) + ") " + Color.string(Color.CYAN, branch))
        count += 1

    choice = int(input("Choice (int): "))
    return choice

def git_status_rebase():
    # checking if there are local changes that need to be dealt with
    git_path.cmd_at_path("git status > \"" + git_path.curr_dir + "\status.log\"")
    status_file = open("status.log", "r")
    cannot_rebase = True
    for line in status_file.readlines():
        line = line.strip()
        if line.startswith("nothing to commit, working tree clean"):
            cannot_rebase = False
            break
    
    if cannot_rebase:
        git_path.cmd_at_path("git status")
        git_path.get_current_branch(force_update=True)
        print(Color.string(Color.RED, "Cannot rebase ") + Color.string(Color.CYAN, git_path.curr_branch) + Color.string(Color.RED, " until changes committed!"))
        return

    if GitSaveVars.addPruneCountCheck():
        print(Color.BLUE)
        git_path.cmd_at_path("git prune")
        print(Color.END)

    # if local changes dealt with, perform a fetch then rebase
    git_path.cmd_at_path("git remote update")
    git_path.cmd_at_path("git rebase " + GitSaveVars.rebase_branch)

def git_checkout_shortcut():
    choice = choose_branch("Choose a branch below to checkout to")
    if choice < 1 or choice > len(git_path.get_all_branches(False)):
        return
    
    if git_path.get_all_branches(False)[choice-1].startswith("*"):
        print(Color.string(Color.BOLD, "Cannot checkout the branch you are currently on!"))
        return
    
    git_path.cmd_at_path("git checkout " + git_path.get_all_branches(False)[choice-1])

def git_delete_shortcut():
    choice = choose_branch("Choose a branch below to delete")
    if choice < 1 or choice > len(git_path.get_all_branches(False)):
        return
    
    if git_path.get_all_branches(False)[choice-1].startswith("*"):
        print(Color.string(Color.BOLD, "Cannot delete the branch you are currently on!"))
        return
    
    git_path.cmd_at_path("git branch -D " + git_path.get_all_branches(False)[choice-1])

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

def git_add_amend_push():
    if GitSaveVars.addPruneCountCheck():
        print(Color.BLUE)
        git_path.cmd_at_path("git prune")
        print(Color.END)

    print(Color.YELLOW)
    git_path.cmd_at_path("git status")
    cont = -1
    cont = int(input(
        "Continue?\n" +
        "  " + Color.string(Color.GREEN, "1) Yes\n") +
        "  " + Color.string(Color.RED + Color.BOLD, "2) No\n") +
        "Choice: " 
    ))
    
    if cont != 1:
        return
    
    print(Color.YELLOW)
    git_path.cmd_at_path("git add -A")
    git_path.cmd_at_path("git commit --amend")
    print(Color.END)

    # ensuring that the local branch given exists in local repo
    # avoiding annoyances if a git prune has not been done in a while
    local_branch = ""
    while not (local_branch in git_path.get_all_branches(False)):
        local_branch = input(Color.string(Color.BOLD + Color.RED, "local branch: "))
        if local_branch.startswith("*") or local_branch == git_path.get_current_branch(False):
            local_branch = "* " + git_path.get_current_branch(False)
    if local_branch.startswith("*"):
        local_branch = git_path.get_current_branch(False)
    
    # remote branch should not be checked: may be a different name in remote
    remote_branch = input(Color.string(Color.BOLD + Color.RED, "remote branch: "))
    print(Color.YELLOW)
    git_path.cmd_at_path("git push origin " + local_branch + ":" + remote_branch + " -f")
    print(Color.END)

def git_set_upstream_origin_branch():
    choice = int(input(
        Color.string(Color.YELLOW, "1) git commit\n") +
        Color.string(Color.YELLOW, "2) git commit --amend\n") +
        "0) Exit Mode\n" +
        "Choice: "
    ))

    if choice == 0:
        return

    print(Color.YELLOW)
    git_path.cmd_at_path("git add -A")
    match choice:
        case 1:
            git_path.cmd_at_path("git commit")
        case 2:
            git_path.cmd_at_path("git commit --amend")

    git_path.cmd_at_path("git push --set-upstream origin " + git_path.get_current_branch(False))
    print(Color.END)

def git_clean():
    choice = int(input(
        Color.string(Color.YELLOW, "1) clean -f -x") + " #(files)\n" +
        Color.string(Color.YELLOW, "2) clean -f -d -x") + " #(directories)\n" +
        "0) Exit Clean Mode\n" +
        "Choice: "
    ))

    match choice:
        case 1:
            git_path.cmd_at_path("git clean -f -x")
        case 2:
            git_path.cmd_at_path("git clean -f -d -x")

def get_all_files_from_commit():
    commit_id = input(Color.string(Color.CYAN, "Commit ID: "))
    folder_name = "commit_" + commit_id
    os.system("mkdir " + folder_name)
    c_drive_filename = "C:\\" + TEMP_COMMIT_TXT_NAME
    git_path.cmd_at_path("git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRT " + commit_id + " > " + c_drive_filename)
    file = open(c_drive_filename, "r")
    for filename in file.readlines():
        filename = filename.strip()
        full_filename = git_path.path + "\\" + filename
        full_filename = full_filename.replace("/", "\\")
        os.system("copy \"" + full_filename + "\" " + folder_name)

def git_create_branch(message):
    backup_pr = input(message + "Branch: ")
    git_path.cmd_at_path("git checkout -b " + backup_pr)

def git_restore_files():
    # printing the git status to a text file in this repo's directory (to not 
    # create text files in that directory)
    git_path.cmd_at_path("git status > \"" + git_path.curr_dir + "\\" + TEMP_STATUS_TXT_NAME + "\"")

    status_file = open(TEMP_STATUS_TXT_NAME)
    staged_files = []
    unstaged_files = []
    get_delta_files(file=status_file, staged_files=staged_files, unstaged_files=unstaged_files)

    if len(staged_files) == 0 and len(unstaged_files) == 0:
        git_path.cmd_at_path("git status")
        return
    
    choose_file_to_restore(staged_files=staged_files, unstaged_files=unstaged_files)

    status_file.close()

def get_delta_files(file, staged_files, unstaged_files):
    add_to_staged = False
    add_to_unstaged = False
    for line in file.readlines():
        line = line.strip()
        if line.startswith("Changes to be committed:"):
            add_to_staged = True
            add_to_unstaged = False
        elif line.startswith("Changes not staged for commit:"):
            add_to_staged = False
            add_to_unstaged = True
        elif line.startswith("no changes added to commit"):
            add_to_unstaged = False
            add_to_staged = False

        if (not add_to_staged) and (not add_to_unstaged):
            continue
        
        idx = line.find(":")
        if idx == -1:
            continue

        line = line[(idx+1):len(line)]
        line = line.strip()
        if len(line) == 0:
            continue

        if add_to_staged:
            staged_files.append(line)
        elif add_to_unstaged:
            unstaged_files.append(line)

def choose_file_to_restore(staged_files, unstaged_files):
    choice = 9999
    while choice > 0:
        print(Color.string(Color.GREEN, "Staged Files:"))
        count = 0
        unstaged_count_offset = len(staged_files)
        for staged_file in staged_files:
            count += 1
            print("\t" + str(count) + ") " + staged_file)

        print(Color.string(Color.RED, "Unstaged Files:"))
        for unstaged_file in unstaged_files:
            count += 1
            print("\t" + str(count) + ") " + unstaged_file)

        count += 1
        print(Color.string(Color.YELLOW, "Options:"))
        print("\t0) Back to Main Menu")
        choice = int(input(Color.string(Color.BOLD, "Choice: ")))
        if choice <= 0:
            break
        elif choice > (len(staged_files) + len(unstaged_files)):
            continue

        if len(staged_files) > 0 and choice <= len(staged_files):
            git_path.cmd_at_path("git restore --staged " + staged_files[choice-1])
            unstaged_files.append(staged_files.pop(choice-1))
        elif len(unstaged_files) > 0 and choice > len(staged_files):
            git_path.cmd_at_path("git restore " + unstaged_files[choice-unstaged_count_offset-1])
            unstaged_files.pop(choice-1)

def set_rebase_branch():
    branch = input("Branch: ")
    GitSaveVars.set_rebase_branch(branch)

if __name__ == '__main__':
    GitSaveVars.initialize()
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
