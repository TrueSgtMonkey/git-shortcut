from git_path import GitPath
from git_save import GitSaveVars
from style import Color
import os as os

STATUS_FILE_NAME: str = "status.log"
MAX_STATUS_RETRIES: int = 5

class GitStatusRebase:
    @classmethod
    def git_status_rebase(self, git_path: GitPath, git_save_vars: GitSaveVars):
        # checking if there are local changes that need to be dealt with
        git_path.cmd_at_path("git status > \"" + git_path.curr_dir + f"\{STATUS_FILE_NAME}\"")
        if not self.was_status_file_created_correctly(git_path):
            return

        status_file = open(STATUS_FILE_NAME, "r")
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

    @classmethod
    def was_status_file_created_correctly(self, git_path: GitPath) -> bool:
        retries: int = 0

        while not os.path.isfile(STATUS_FILE_NAME) and retries < MAX_STATUS_RETRIES:
            os.system("touch " + STATUS_FILE_NAME)
            Color.print(Color.RED, "Cannot obtain status! " + STATUS_FILE_NAME + " does not exist!\nRetrying...")
            git_path.cmd_at_path("git status > \"" + git_path.curr_dir + f"\{STATUS_FILE_NAME}\"")
            retries += 1

        if retries >= MAX_STATUS_RETRIES:
            Color.print(Color.RED, f"Retries failed. Cannot retrieve {STATUS_FILE_NAME}.\nAborting...")
            return False

        return True
