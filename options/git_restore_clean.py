from git_path import GitPath
from style import Color
from get_current_commit_info import GetCurrentCommitInfo

class GitRestoreClean:
    @classmethod
    def git_restore_files(self, git_path: GitPath):
        # retrieving the types of changes below from a git_status call
        staged_files, unstaged_files, untracked_files = GetCurrentCommitInfo.get_current_changes_as_arrays(git_path)
        
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

