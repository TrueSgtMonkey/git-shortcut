from git_path import GitPath
from style import Color
import os as os
from io import TextIOWrapper

TEMP_COMMIT_TXT_NAME = "___commit___.txt"
TEMP_STATUS_TXT_NAME = "..temp_status.txt"

class GetCurrentCommitInfo:
    @classmethod
    def get_all_files_from_commit(self, git_path: GitPath):
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
            
    @classmethod
    def get_current_changes_as_arrays(self, git_path: GitPath) -> tuple[list, list, list]:
        # printing the git status to a text file in this repo's directory (to not 
        # create text files in that directory)
        git_path.cmd_at_path("git status > \"" + git_path.curr_dir + "\\" + TEMP_STATUS_TXT_NAME + "\"")

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
        add_to_staged =    False
        add_to_unstaged =  False
        add_to_untracked = False
        for line in file.readlines():
            line: str = line.strip()
            if line.startswith("Changes not staged for commit:"):
                add_to_unstaged  = True
                add_to_staged    = False
                add_to_untracked = False
            elif line.startswith("Changes to be committed:"):
                add_to_unstaged  = False
                add_to_staged    = True
                add_to_untracked = False
            elif line.startswith("Untracked files"):
                add_to_unstaged  = False
                add_to_staged    = False
                add_to_untracked = True
            elif line.startswith("no changes added to commit"):
                add_to_unstaged  = False
                add_to_staged    = False
                add_to_untracked = False
                

            if (not add_to_staged) and (not add_to_unstaged) and (not add_to_untracked):
                continue
            
            idx = line.find(":")
            if idx == -1 and (not add_to_untracked):
                continue
            
            if line.find("git add <file>...") != -1:
                continue
            
            if add_to_untracked and line.find("nothing added to commit but untracked files present") != -1:
                continue

            # For untracked files, idx == -1
            # But, that will be fine since we will just grab the entire string
            line = line[(idx+1):len(line)]
            line = line.strip()
            if len(line) == 0:
                continue

            if add_to_staged:
                staged_files.append(line)
            elif add_to_unstaged:
                unstaged_files.append(line)
            elif add_to_untracked:
                untracked_files.append(line)
