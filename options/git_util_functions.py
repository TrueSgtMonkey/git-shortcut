from style import Color
from git_path import GitPath
import os as os

MAX_FILE_RETRIES: int = 5

class GitUtilFunctions:
    @classmethod
    def get_continue_choice(self) -> int:
        cont = int(input(
            "Continue?\n" +
            "  " + Color.string(Color.GREEN, "1) Yes\n") +
            "  " + Color.string(Color.RED + Color.BOLD, "2) No\n") +
            "Choice: " 
        ))
        
        return cont

    @classmethod
    def was_file_created_correctly(self, git_path: GitPath, file_name: str) -> bool:
        retries: int = 0

        while not os.path.isfile(file_name) and retries < MAX_FILE_RETRIES:
            os.system("touch " + file_name)
            Color.print(Color.RED, "Cannot obtain status! " + file_name + " does not exist!\nRetrying...")
            git_path.cmd_at_path("git status > \"" + git_path.curr_dir + f"\{file_name}\"")
            retries += 1

        if retries >= MAX_FILE_RETRIES:
            Color.print(Color.RED, f"Retries failed. Cannot retrieve {file_name}.\nAborting...")
            return False

        return True
