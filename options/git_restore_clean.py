from io import TextIOWrapper
from git_path import GitPath
from style import Color

TEMP_STATUS_TXT_NAME = "..temp_status.txt"

class GitRestoreClean:
    @classmethod
    def git_restore_files(self, git_path: GitPath):
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
            return
        
        self.choose_file_to_restore(git_path, staged_files=staged_files, unstaged_files=unstaged_files, untracked_files=untracked_files)

        status_file.close()

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

    @classmethod
    def choose_file_to_restore(self, git_path: GitPath, staged_files: list, unstaged_files: list, untracked_files: list):
        choice = 9999
        while choice > 0:
            print(Color.string(Color.GREEN, "Staged Files:"))
            count = 0
            color_str: str = Color.BOLD
            for staged_file in staged_files:
                count += 1
                Color.print(color_str, "\t" + str(count) + ") " + staged_file)
                color_str = Color.update_color_print(count, Color.BOLD, Color.CYAN)

            print(Color.string(Color.RED, "Unstaged Files:"))
            for unstaged_file in unstaged_files:
                count += 1
                Color.print(color_str, "\t" + str(count) + ") " + unstaged_file)
                color_str = Color.update_color_print(count, Color.BOLD, Color.CYAN)
                
            Color.print(Color.PURPLE, "Untracked Files:")
            for untracked_file in untracked_files:
                count += 1
                Color.print(color_str, "\t" + str(count) + ") " + untracked_file)
                color_str = Color.update_color_print(count, Color.BOLD, Color.CYAN)
            

            count += 1
            print(Color.string(Color.YELLOW, "Options:"))
            print("\t0) Back to Main Menu")
            choice = int(input(Color.string(Color.BOLD, "Choice: ")))
            if choice <= 0:
                break
            elif choice > (len(staged_files) + len(unstaged_files) + len(untracked_files)):
                continue
            
            end_staged_files_idx: int = len(staged_files)
            end_unstaged_files_idx: int = end_staged_files_idx + len(unstaged_files)
            if end_staged_files_idx > 0 and choice <= end_staged_files_idx:
                git_path.cmd_at_path("git restore --staged " + staged_files[choice-1])
                unstaged_files.append(staged_files.pop(choice-1))
            elif len(unstaged_files) > 0 and (choice > end_staged_files_idx and choice <= end_unstaged_files_idx):
                git_path.cmd_at_path("git restore " + unstaged_files[choice-end_staged_files_idx-1])
                unstaged_files.pop(choice-end_staged_files_idx-1)
            elif len(untracked_files) > 0 and choice > end_unstaged_files_idx:
                os_cmd: str = "del " if git_path.plat == "Windows" else "rm -rf "
                git_path.cmd_at_path(os_cmd + untracked_files[choice-end_unstaged_files_idx-1])
                untracked_files.pop(choice-end_unstaged_files_idx-1)
                
    @classmethod
    def git_clean(self, git_path: GitPath):
        choice = int(input(
            Color.string(Color.YELLOW, "1) clean -f -x") + " #(files)\n" +
            Color.string(Color.YELLOW, "2) clean -f -d -x") + " #(directories)\n" +
            "0) Exit Clean Mode\n" +
            "Choice: "
        ))

        match choice:
            case 1:
                git_path.cmd_at_path("git clean -f -x")
            case 2:
                git_path.cmd_at_path("git clean -f -d -x")

