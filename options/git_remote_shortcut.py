from git_path import GitPath
from git_save import GitSaveVars
from style import Color
from git_util_functions import GitUtilFunctions

class GitRemoteShortCut:
    @classmethod
    def git_add_amend_push(self, git_path: GitPath, git_save_vars: GitSaveVars):
        if git_save_vars.addPruneCountCheck():
            print(Color.BLUE)
            git_path.cmd_at_path("git prune")
            print(Color.END)

        print(Color.YELLOW)
        git_path.cmd_at_path("git status")

        cont: int = GitUtilFunctions.get_continue_choice()
        if cont != 1:
            return
        
        print(Color.YELLOW)
        git_path.cmd_at_path("git add .")
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
        
    @classmethod
    def git_set_upstream_origin_branch(self, git_path: GitPath):
        choice = int(input(
            Color.string(Color.YELLOW, "1) git commit\n") +
            Color.string(Color.YELLOW, "2) git commit --amend\n") +
            "0) Exit Mode\n" +
            "Choice: "
        ))

        if choice == 0:
            return

        print(Color.YELLOW)
        git_path.cmd_at_path("git add .")
        match choice:
            case 1:
                git_path.cmd_at_path("git commit")
            case 2:
                git_path.cmd_at_path("git commit --amend")

        git_path.cmd_at_path("git push --set-upstream origin " + git_path.get_current_branch(False))
        print(Color.END)
