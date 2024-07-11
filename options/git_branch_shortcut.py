from git_path import GitPath
from git_save import GitSaveVars
from git_util_functions import GitUtilFunctions
from style import Color
from get_current_commit_info import GetCurrentCommitInfo

class GitBranchShortcut:
    @classmethod
    def git_checkout_shortcut(self, git_path: GitPath):
        all_branches: list = git_path.get_all_branches(True)
        choice = self.choose_branch(git_path, "Choose a branch below to checkout to")
        if choice < 1 or choice > len(all_branches):
            return
        
        if all_branches[choice-1].startswith("*"):
            print(Color.string(Color.BOLD, "Cannot checkout the branch you are currently on!"))
            return
        
        git_path.cmd_at_path("git checkout " + all_branches[choice-1])
        git_path.get_current_branch(True)

    @classmethod
    def git_delete_shortcut(self, git_path: GitPath):
        all_branches: list = git_path.get_all_branches(True)
        choice = self.choose_branch(git_path, "Choose a branch below to delete")
        if choice < 1 or choice > len(all_branches):
            return
        
        if all_branches[choice-1].startswith("*"):
            print(Color.string(Color.BOLD, "Cannot delete the branch you are currently on!"))
            return
        
        git_path.cmd_at_path("git branch -D " + all_branches[choice-1])
        git_path.get_current_branch(True)

    @classmethod
    def choose_branch(self, git_path: GitPath, message) -> int:
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
    
    @classmethod
    def git_create_branch(self, message, git_path: GitPath):
        backup_pr = input(message + "Branch: ")
        git_path.cmd_at_path("git checkout -b " + backup_pr)
        git_path.get_current_branch(True)
        
    @classmethod
    def git_update_current_branch(self, git_path: GitPath):
        git_path.cmd_at_path("git remote update")
        staged_files, unstaged_files, untracked_files = GetCurrentCommitInfo.get_current_changes_as_arrays(git_path)
        
        # untracked files might be fine to ignore
        if len(staged_files) > 0 or len(unstaged_files) > 0:
            Color.print(Color.RED, "Changes detected on current branch!\nBranch Update aborted.")
            return
        elif len(untracked_files) > 0:
            Color.print(Color.YELLOW, Color.string(Color.RED, "WARNING") + ": Untracked changes detected. Continue? (Type 0 to not continue)")
            choice = GitUtilFunctions.get_continue_choice()
            if choice != 1:
                return
        
        current_local_rebase_branch: str = GitSaveVars.rebase_branch
        current_local_rebase_branch = current_local_rebase_branch.replace("origin/", "")
        
        current_branches: list = git_path.get_all_branches(True)
        current_branch: str = git_path.get_current_branch(False)
        
        if current_local_rebase_branch in current_branches:
            print("Swtiching to: " + Color.string(Color.YELLOW, current_local_rebase_branch))
        else:
            Color.print(Color.RED, "Cannot find: " + Color.string(Color.YELLOW, current_local_rebase_branch) + " in local repo!")

        print(Color.string(Color.YELLOW, "WARNING: ") + Color.string(Color.RED, " This function will delete the local branch and then rebase with remote."))
        cont: int = GitUtilFunctions.get_continue_choice()
        if cont != 1:
            return
        
        git_path.cmd_at_path("git checkout " + current_local_rebase_branch)
        git_path.cmd_at_path("git branch -D " + current_branch)
        git_path.cmd_at_path("git checkout -b " + current_branch + " origin/" + current_branch)
        
