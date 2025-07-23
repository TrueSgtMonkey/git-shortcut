from git_path import GitPath
from style import Color
from get_current_commit_info import GetCurrentCommitInfo

GIT_RESTORE_STAGED: str = "git restore --staged "
GIT_RESTORE: str        = "git restore "

class GitRestoreClean:
    @classmethod
    def git_restore_files(self, git_path: GitPath, max_iterations: int):
        # restoring all files recursively calls this function
        # will lead to a stack of log2(max_iterations)
        if max_iterations <= 0:
            return

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
            print("  -1) Restore all files")
            print("   0) Back to Main Menu")
            choice = int(input(Color.string(Color.BOLD, "Choice: ")))
            if choice == 0:
                break
            elif choice < 0:
                if choice == -1:
                    self.restore_all_files(git_path, staged_files, unstaged_files, untracked_files, max_iterations)
                    self.git_restore_files(git_path, max_iterations / 2)
                else:
                    continue
            elif choice > (len(staged_files) + len(unstaged_files) + len(untracked_files)):
                continue
            
            self.choose_file_to_restore(git_path, choice, staged_files, unstaged_files, untracked_files)


    @classmethod
    def choose_file_to_restore(self, git_path: GitPath, choice: int, staged_files: list, unstaged_files: list, untracked_files: list):
        end_staged_files_idx: int = len(staged_files)
        end_unstaged_files_idx: int = end_staged_files_idx + len(unstaged_files)
        if end_staged_files_idx > 0 and choice <= end_staged_files_idx:
            git_path.cmd_at_path(GIT_RESTORE_STAGED + staged_files[choice-1])
            unstaged_files.append(staged_files.pop(choice-1))
        elif len(unstaged_files) > 0 and (choice > end_staged_files_idx and choice <= end_unstaged_files_idx):
            git_path.cmd_at_path(GIT_RESTORE + unstaged_files[choice-end_staged_files_idx-1])
            unstaged_files.pop(choice-end_staged_files_idx-1)
        elif len(untracked_files) > 0 and choice > end_unstaged_files_idx:
            # Windows: replacing "/" with "\\" avoids "Invalid Switch" errors
            print("deleting untracked file")
            file_to_remove: str = untracked_files[choice-end_unstaged_files_idx-1]
            os_cmd: str
            if git_path.plat == "Windows":
                os_cmd = "del /F /Q "
                file_to_remove = file_to_remove.replace("/", "\\")
            else:
                os_cmd = "rm -rf "
            print("os_cmd: " + os_cmd + " -> " + file_to_remove)

            git_path.cmd_at_path(os_cmd + file_to_remove)
            untracked_files.pop(choice-end_unstaged_files_idx-1)
            
    @classmethod
    def restore_all_files(self, git_path: GitPath, staged_files: list, unstaged_files: list, untracked_files: list, max_iterations: int):
        print(Color.string(Color.YELLOW, "Max Iterations: ") + str(max_iterations))
        self.restore_many_files(git_path, GIT_RESTORE_STAGED, staged_files, unstaged_files, "staged", max_iterations)
        self.restore_many_files(git_path, GIT_RESTORE, unstaged_files, None, "unstaged", max_iterations)
        os_cmd: str = "del /F /Q " if git_path.plat == "Windows" else "rm -rf "
        self.restore_many_files(git_path, os_cmd, untracked_files, None, "untracked", max_iterations)

    @classmethod
    def restore_many_files(self, git_path: GitPath, restore_start: str, current_files: list, next_files: list, current_stage: str, max_iterations: int):
        while len(current_files) > 0:
            files_to_restore: str = restore_start + " "
            iterations: int = 0
            staged_files_to_delete: list = []
            
            for staged_file in current_files:
                staged_files_to_delete.append(staged_file)
                files_to_restore += f"\"{staged_file}\" "
                iterations += 1
                if iterations >= max_iterations:
                    break
                
            for staged_file in staged_files_to_delete:
                current_files.remove(staged_file)
                if next_files is None:
                    continue

                next_files.append(staged_file)
            
            git_path.cmd_at_path(files_to_restore)
            print(f"{current_stage}: {len(current_files)}")

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

