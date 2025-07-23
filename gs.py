#git shortcut main
# contains main function as well as specific Git functions

import sys as sys
import json as json
import os as os

sys.path[:0] = ["options", "misc_options"]
from options.git_status_rebase       import GitStatusRebase
from options.git_branch_shortcut     import GitBranchShortcut
from options.git_remote_shortcut     import GitRemoteShortCut
from options.git_restore_clean       import GitRestoreClean
from options.get_current_commit_info import GetCurrentCommitInfo

from misc_options.git_repo_shortcuts            import GitRepoShortcuts
from misc_options.useful_functions_and_commands import UsefulFunctions

from style import Color
from git_path import GitPath
from git_save import GitSaveVars

MIN_OPTIONS = -9
MAX_OPTIONS = 11

def main(git_path) -> dict:
    # setting to very low value to make sure it runs at least once
    option = -999999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = print_user_options(git_path)

    if option != 0:
        run_commands(git_path, option)
    
    return {
        "git_path" : git_path,
        "option" : option
    }

def print_user_options(git_path):
    print(Color.string(Color.BOLD + Color.RED, "WARNING: Make sure to put this outside of your git project!"))
    user_input = ""
    print(
        Color.string(Color.BOLD + Color.GREEN, "#)  Option\n") +
        Color.string(Color.BOLD + Color.GREEN, "GIT SHORTCUTS:\n") + 
        "1)   git status\n" +
        "2)   git rebase with " + Color.string(Color.YELLOW, GitSaveVars.rebase_branch) + "\n" +
        "3)   git checkout <list_of_branches>\n" +
        "4)   git branch -D <list_of_branches>\n" +
        "5)   update current branch\n" + 
        "6)   git checkout -b <branch_name>\n" +
        "7)   amend PR code review\n" +
        "8)   git push --set-upstream origin " + Color.string(Color.CYAN, git_path.get_current_branch(False)) + "\n" +
        "9)   git restore <list_of_files>\n" +
        "10)  git clean\n" +
        "11)  get all files altered in commit <commit-id>\n" +
        "0)   Exit\n" +
        Color.string(Color.BOLD + Color.GREEN, "MISC SHORTCUTS:\n") +
        "-1)  Add Path\n" +
        "-2)  Change Path\n" +
        "-3)  Remove Path\n" + 
        "-4)  Open cmd in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
        "-5)  Open git-bash in <" + Color.string(Color.DARKCYAN, git_path.path) + ">\n" +
        "-6)  Explore Git repo\n" +
        "-7)  Refresh\n" +
        "-8)  Set branch to rebase with (current=" + Color.string(Color.YELLOW, GitSaveVars.rebase_branch) + ")\n" +
        "-9)  Useful Functions/Commands\n" +
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
            git_path.cmd_at_path("git status")
        case 2:
            GitStatusRebase.git_status_rebase(git_path, GitSaveVars)
        case 3:
            GitBranchShortcut.git_checkout_shortcut(git_path)
        case 4:
            GitBranchShortcut.git_delete_shortcut(git_path)
        case 5:
            GitBranchShortcut.git_update_current_branch(git_path)
        case 6:
            GitBranchShortcut.git_create_branch("Checkout ", git_path)
        case 7:
            GitRemoteShortCut.git_add_amend_push(git_path, GitSaveVars)
        case 8:
            GitRemoteShortCut.git_set_upstream_origin_branch(git_path)
        case 9:
            GitRestoreClean.git_restore_files(git_path, 69)
        case 10:
            GitRestoreClean.git_clean(git_path)
        case 11:
            GetCurrentCommitInfo.get_all_files_from_commit(git_path)
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
            GitRepoShortcuts.set_rebase_branch(GitSaveVars)
        case -9:
            UsefulFunctions.useful_functions_and_commands(git_path)

def git_mikkel_merge():
    # Grabbing current path and updating to ensure we are on the correct one
    current_path = git_path.get_current_branch(True)
    if current_path == "main":
        Color.print(Color.RED + Color.UNDERLINE, "checkout to your branch that you want to merge with main!")

    # Checking with user if they want to do this since this will merge PR
    choice = int(input(
        Color.string(Color.BLUE, "You are about to merge " + current_path + " in with main.\nContinue?") +
        Color.string(Color.YELLOW, "1) Yes\n") +
        Color.string(Color.YELLOW, "2) No\n")  +
        "Choice: "
    ))
    if choice != 1:
        return

    # Performing the merge
    git_path.cmd_at_path("git checkout main")
    git_path.cmd_at_path("git merge origin/" + current_path)
    git_path.cmd_at_path("git push")

if __name__ == '__main__':
    GitSaveVars.initialize()
    git_path = GitPath()

    # picking path before start of program to keep track of repo
    while git_path.pick_path(git_path.SAVE_PATH) == False:
        print(Color.string(Color.RED, "Something went wrong with picking/creating a path...\nTry again."))

    git_path.get_current_branch(True)

    # calling main function as long as user does not exit prog (user enters 0)
    print(Color.string(Color.BOLD + Color.GREEN + Color.UNDERLINE, "Version: " + git_path.plat))
    print(Color.string(Color.BOLD + Color.RED, "WARNING: Make sure to put this outside of your git project!"))
    ret_dict: dict = main(git_path)

    retVal: int       = ret_dict["option"]
    git_path: GitPath = ret_dict["git_path"]
    while retVal != 0:
        ret_dict = main(git_path)

        retVal   = ret_dict["option"]
        git_path = ret_dict["git_path"]
