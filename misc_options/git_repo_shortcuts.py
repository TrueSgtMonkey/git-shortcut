

from io import TextIOWrapper
import json as json
import os as os
from git_path import GitPath
from git_save import GitSaveVars
from style import Color


REBASE_BRANCHES_TXT_NAME  = "rebase_branches.json"
REBASE_BRANCHES_KEY_NAME  = "rebase_branches"

class GitRepoShortcuts:
    CMD_ID: int = 4
    BASH_ID: int = 5

    @classmethod
    def open_terminal_for_os(self, git_path: GitPath, type_cmd_id: int):
        match git_path.plat.lower():
            case "windows":
                if type_cmd_id == self.CMD_ID:
                    git_path.cmd_at_path("start cmd.exe")
                elif type_cmd_id == self.BASH_ID:
                    git_path.cmd_at_path("start git-bash.exe")
                else:
                    print("Unknown ID: Check \'open_terminal_for_os\' function!")
                    return
            case "linux":
                git_path.cmd_at_path(f"konsole {git_path.path} &")
            case _:
                git_path.cmd_at_path("open -a Terminal .")

    @classmethod
    def set_rebase_branch(self, git_save_vars: GitSaveVars):
        jsonDict = {}
        file : TextIOWrapper = None

        if not os.path.exists(REBASE_BRANCHES_TXT_NAME):
            jsonDict = self.get_json_dict()
        else:
            try:
                file = open(REBASE_BRANCHES_TXT_NAME, "r")
                jsonDict = json.load(file)
            except Exception:
                jsonDict = self.get_json_dict()

        rebase_branches = []
        message = ""
        curr_idx = 1
        choice = 1
        for branch in jsonDict[REBASE_BRANCHES_KEY_NAME]:
            rebase_branches.append(branch)
            if curr_idx % 2 == 0:
                message += Color.string(Color.GREEN, str(curr_idx) + ")  " + branch + "\n")
            else:
                message += Color.string(Color.RED, str(curr_idx) + ")  " + branch + "\n")
            curr_idx += 1
        
        while choice != 0:
            choice = int(input(
                message +
                "0)  Exit Mode\n" +
                "-1) Add Path\n" +
                "-2) Remove Path\n" +
                "Choice: "
            ))

            match choice:
                case 0:
                    return
                case -1:
                    message, curr_idx = self.add_rebase_branch(rebase_branches, jsonDict, message, curr_idx)
                case -2:
                    message, curr_idx = self.remove_rebase_branch(rebase_branches, jsonDict, message, curr_idx)
                case _:
                    branch = rebase_branches[choice-1]
                    git_save_vars.set_rebase_branch(branch)
                    return

    @classmethod
    def get_json_dict(self) -> dict:
        file = open(REBASE_BRANCHES_TXT_NAME, "w")
        jsonDict = {
            REBASE_BRANCHES_KEY_NAME : {

            }
        }
        json.dump(jsonDict, file)
        file.close()

        return jsonDict
    
    @classmethod
    def add_rebase_branch(self, rebase_branches : list, jsonDict : dict, message : str, curr_idx : int):
        file = open(REBASE_BRANCHES_TXT_NAME, "w")
        branch = input("Branch: ")
        GitSaveVars.set_rebase_branch(branch)
        rebase_branches.append(branch)
        jsonDict[REBASE_BRANCHES_KEY_NAME][branch] = True
        message += str(curr_idx) + ")  " + branch + "\n"
        curr_idx += 1
        json.dump(jsonDict, file)
        file.close()

        return message, curr_idx

    @classmethod
    def remove_rebase_branch(self, rebase_branches : list, jsonDict : dict, message : str, curr_idx : int):
        del_choice = int(input(
            message +
            "0) Do not delete\n" +
            "Choice: "
        ))
        del_choice_idx = del_choice-1

        # we chose to exit instead of deleting
        if del_choice <= 0 or del_choice_idx >= len(rebase_branches):
            return message, curr_idx
        
        file = open(REBASE_BRANCHES_TXT_NAME, "w")

        # removing element from list and jsonDict
        jsonDict[REBASE_BRANCHES_KEY_NAME].pop(rebase_branches[del_choice_idx])
        rebase_branches.pop(del_choice_idx)

        # changing string for the next print
        curr_idx = 1
        message = ""
        for branch in rebase_branches:
            message += str(curr_idx) + ")  " + branch + "\n"
            curr_idx += 1

        # output all of the results to the file
        json.dump(jsonDict, file)

        file.close()

        return message, curr_idx
