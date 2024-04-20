from git_path import GitPath
from git_save import GitSaveVars
from style import Color

class GitStatusRebase:
    @classmethod
    def git_status_rebase(self, git_path: GitPath, git_save_vars: GitSaveVars):
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

        if git_save_vars.addPruneCountCheck():
            print(Color.BLUE)
            git_path.cmd_at_path("git prune")
            print(Color.END)

        # if local changes dealt with, perform a fetch then rebase
        git_path.cmd_at_path("git remote update")
        git_path.cmd_at_path("git rebase " + git_save_vars.rebase_branch)
