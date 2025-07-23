from git_path import GitPath
from style import Color
import os as os
from io import TextIOWrapper
from git_util_functions import GitUtilFunctions

TEMP_COMMIT_TXT_NAME = "___commit___.txt"
TEMP_STATUS_TXT_NAME = "..temp_status.txt"

class AddState:
    STAGED: int    = 0
    UNSTAGED: int  = 1
    UNTRACKED: int = 2
    NONE: int      = 3
    
    state: int
    def __init__(self):
        self.state = self.NONE

class GetCurrentCommitInfo:
    @classmethod
    def get_all_files_from_commit(self, git_path: GitPath):
        platform_slash: str = "\\" if git_path.plat == "Windows" else "/"
        commit_id = input(Color.string(Color.CYAN, "Commit ID: "))

        platform_filename: str = git_path.curr_dir + platform_slash + TEMP_COMMIT_TXT_NAME

        git_path.cmd_at_path("git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRT " + commit_id + " > " + platform_filename)
        file = open(platform_filename, "r")

        choice: int = int(input(
            "1) Output Affected Files\n" +
            "2) Output File Paths to Directory\n" +
            "0) Exit\n" +
            "Choice: "
        ))

        if choice == 1:
            self.print_all_commit_files(file)
        elif choice == 2:
            self.output_all_commit_files_to_dir(git_path, platform_slash, commit_id, file)

    @classmethod
    def print_all_commit_files(self, file: TextIOWrapper):
        print("Affected Files ...")
        for filename in file.readlines():
            filename = filename.strip()
            print(filename)

    @classmethod
    def output_all_commit_files_to_dir(self, git_path: GitPath, slash_str: str, commit_id: str, file: TextIOWrapper):
        folder_name: str = "commit_" + commit_id
        output_dir = f"\"{input("output directory: ")}\""
        os.system(f"mkdir {output_dir}{slash_str}{folder_name}")
        for filename in file.readlines():
            filename = filename.strip()
            full_filename = git_path.path + slash_str + filename
            if GitPath.plat == "Windows":
                full_filename = full_filename.replace("/", "\\")
                filename = filename.replace("/", "\\")
            
            # Need to run this function in order to work with files of the
            # same name in different directories.
            complete_path_to_new_dir: str = self.get_or_create_path_to_file(filename, folder_name, output_dir, slash_str)
            os.system("copy \"" + full_filename + "\" " + complete_path_to_new_dir)

    @classmethod
    def get_or_create_path_to_file(self, filename: str, folder_name: str, output_dir: str, slash_str: str) -> str:        
        # find the path to the file, but do not include the file itself
        last_slash_idx: int = filename.rfind(slash_str)
        path_str: str = filename[0:last_slash_idx] if last_slash_idx > 0 else filename
        
        # Check that current path we want to copy to exists
        # Need to create the path if it does not exist
        root_path: str = output_dir + slash_str + folder_name + slash_str
        complete_path_str: str = root_path + path_str
        print(f"Copying \"{path_str}\" to {complete_path_str}")
        if not os.path.isdir(complete_path_str):
            total_created_path: str = root_path
            
            # Build the path in the new directory to preserve folder structure
            path_str_arr: list = path_str.split(slash_str)
            for curr_path in path_str_arr:
                if not os.path.isdir(total_created_path + curr_path):
                    total_created_path += "\"" + curr_path + "\"" + slash_str
                    if curr_path.find(".") == -1:
                        os.system("mkdir " + total_created_path)
                
        return complete_path_str

    @classmethod
    def get_current_changes_as_arrays(self, git_path: GitPath) -> tuple[list, list, list]:
        # printing the git status to a text file in this repo's directory (to not 
        # create text files in that directory)
        platform_slash: str = "\\" if git_path.plat == "Windows" else "/"
        git_path.cmd_at_path("git status > \"" + git_path.curr_dir + platform_slash + TEMP_STATUS_TXT_NAME + "\"")
        GitUtilFunctions.was_file_created_correctly(git_path, TEMP_STATUS_TXT_NAME)

        status_file = open(TEMP_STATUS_TXT_NAME)
        staged_files = []
        unstaged_files = []
        untracked_files = []
        self.get_delta_files(file=status_file, staged_files=staged_files, unstaged_files=unstaged_files, untracked_files=untracked_files)

        if len(staged_files) == 0 and len(unstaged_files) == 0 and len(untracked_files) == 0:
            git_path.cmd_at_path("git status")
            
        status_file.close()
        return staged_files, unstaged_files, untracked_files

    @classmethod
    def get_delta_files(self, file: TextIOWrapper, staged_files: list, unstaged_files: list, untracked_files: list):
        add_state: AddState = AddState()
        for line in file.readlines():
            line: str = line.strip()
            if line.startswith("Changes not staged for commit:"):
                add_state.state = AddState.UNSTAGED
            elif line.startswith("Changes to be committed:"):
                add_state.state = AddState.STAGED
            elif line.startswith("Untracked files"):
                add_state.state = AddState.UNTRACKED

            if add_state.state == AddState.NONE:
                continue

            idx = line.find(":")
            if idx == -1 and (add_state.state != AddState.UNTRACKED):
                continue
            
            if line.find("git add <file>...") != -1:
                continue
            
            if (add_state.state == AddState.UNTRACKED) and line.find("nothing added to commit but untracked files present") != -1:
                continue

            # For untracked files, idx == -1
            # But, that will be fine since we will just grab the entire string
            line = line[(idx+1):len(line)]
            line = line.strip()
            if len(line) == 0:
                continue

            match add_state.state:
                case AddState.STAGED:
                    staged_files.append(line)
                case AddState.UNSTAGED:
                    unstaged_files.append(line)
                case AddState.UNTRACKED:
                    untracked_files.append(line)
                case _:
                    Color.print(Color.CYAN, "AddState: " + Color.string(Color.RED, str(add_state.state) + Color.string(Color.CYAN, " is not recognized!")))
