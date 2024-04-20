from git_path import GitPath
from style import Color
import os as os

TEMP_COMMIT_TXT_NAME = "___commit___.txt"

class GetAllFilesFromCommit:
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
