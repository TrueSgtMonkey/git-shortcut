from git_path import GitPath
from style import Color

class GitBranchShortcut:
    @classmethod
    def git_checkout_shortcut(self, git_path: GitPath):
        choice = self.choose_branch(git_path, "Choose a branch below to checkout to")
        if choice < 1 or choice > len(git_path.get_all_branches(False)):
            return
        
        if git_path.get_all_branches(False)[choice-1].startswith("*"):
            print(Color.string(Color.BOLD, "Cannot checkout the branch you are currently on!"))
            return
        
        git_path.cmd_at_path("git checkout " + git_path.get_all_branches(False)[choice-1])

    @classmethod
    def git_delete_shortcut(self, git_path: GitPath):
        choice = self.choose_branch(git_path, "Choose a branch below to delete")
        if choice < 1 or choice > len(git_path.get_all_branches(False)):
            return
        
        if git_path.get_all_branches(False)[choice-1].startswith("*"):
            print(Color.string(Color.BOLD, "Cannot delete the branch you are currently on!"))
            return
        
        git_path.cmd_at_path("git branch -D " + git_path.get_all_branches(False)[choice-1])

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
