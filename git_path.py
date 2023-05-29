# Contains GitPath class - performs most of path related stuff needed for Git

from array import array
from importlib.resources import path
from style import Color
import os
import platform
from git_save import GitSaveVars

CURRENT_BRANCH_TXT = "___tmp___.txt"

class GitPath:
    # constants
    SAVE_PATH = "path.txt"

    # variables
    curr_dir = ""
    curr_branch = ""
    all_branches = []
    paths = []
    path = ""                   #current paths
    txt_file = ""
    plat = ""
    new_branch_detected = False
    chk_dict = {}

    @classmethod
    def __init__(Self):
        Self.curr_dir = os.getcwd()
        Self.plat = platform.system()
        Self.new_branch_detected = True
        if Self.plat == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @classmethod
    def new_path(Self):
        # making sure path is valid - returning if not
        old_path = Self.path
            
        Self.path = input("path: ")
        if not os.path.isdir(Self.path):
            print("\'" + Self.path + "\' does not exist...\n switching back to \'" + old_path + "\'")
            Self.path = old_path
            return

        for path in Self.paths:
            if path == Self.path:
                print(Self.path + " already exists! Returning...")
                return

        # no matter what, this will write to a valid file
        file = open(Self.SAVE_PATH, "a")
        file.write(Self.path + "\n")
        file.close()

        Self.paths.append(Self.path)

    @classmethod
    def pick_path(Self, path):
        try:
            file = open(path, "r")
        except FileNotFoundError:
            print("Cannot find " + GitPath.SAVE_PATH + "...\ncreating new one...")
            Self.new_path()
            return False

        count = 0
        lines = file.readlines()

        # reading the file line by line and displaying indices to user
        # only run if Self.paths is empty
        if len(Self.paths) == 0:
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    print(str(count) + ": " + line)
                    Self.paths.append(line)
                    count += 1

            if len(Self.paths) == 0:
                print("Git Repo path not added to \"path.txt\"\nAdd new path below:")
                Self.new_path()
                file.close()
                return False
        else:
            count = Self.print_curr_paths()

        # picking the path that we want to load from file
        while count >= len(Self.paths):
            print("Choose a number < 0 to not choose a path.")
            countString = input("Which path (#): ")
            while not countString.isnumeric() or int(countString) < 0:
                Color.print(Color.RED, "Please input an integer (..., -3, -2, -1, 0, 1, 2, 3, ...)")
                countString = input("Which path (#): ")
            count = int(countString)
            if count >= len(Self.paths):
                Self.print_curr_paths()
            elif count < 0:
                print("Exiting...")
                file.close()
                return False

        Self.path = Self.paths[count]
        
        file.close()
        return True

    ## Calling w/ False returns curr Branch unless curr branch not loaded yet
    ## Calling w/ True forces branch to grab curr branch from text file
    @classmethod
    def get_current_branch(Self, force_update) -> str:
        str_to_ret = ""

        # iterates through a text file so only want to run this once in a while
        if force_update or Self.curr_branch == "":
            branches = Self.get_all_branches(force_update)
            for line in branches:
                if line.startswith("*"):
                    str_to_ret = line[(line.find("*") + 2):len(line)]
            
            Self.curr_branch = str_to_ret

        str_to_ret = Self.curr_branch
        return str_to_ret

    @classmethod
    def get_all_branches(Self, force_update) -> array:
        if force_update or len(Self.all_branches) == 0:
            old_text = Self.txt_file
            Self.all_branches = []

            Self.txt_file = CURRENT_BRANCH_TXT
            Self.cmd_to_txt("branch", False)

            file = open(Self.txt_file, "r")

            for line in file.readlines():
                line = line.strip()
                Self.all_branches.append(line)

            Self.txt_file = old_text
            file.close()
        

        return Self.all_branches

    @classmethod
    def print_curr_paths(Self):
        count = 0
        for path in Self.paths:
            print(str(count) + ": " + Color.string(Color.DARKCYAN + Color.BOLD, path))
            count += 1
        return count

    @classmethod
    def remove_path(Self, path):
        # picking the path we want to delete and removing from array
        will_del = Self.pick_path(path)
        if not will_del:
            return
        Self.paths.remove(Self.path)

        # overwriting the file to erase the path from the file
        file = open(path, "w")

        for curr_path in Self.paths:
            file.write(curr_path + "\n")

        file.close()

        print("Pick a new repo to switch to below (if one exists)...")
        # picking a new path or creating one if we deleted all
        Self.pick_path(path)

    @classmethod
    def explore_at_path(Self):
        if Self.plat == "Windows":
            path = os.path.realpath(Self.path)
            os.startfile(path)
        else: 
            os.system("open %s" % Self.path)

    @classmethod
    def set_curr_dir(Self, path):
        if type(path) is str:
            Self.curr_dir = path

    @classmethod
    def add_branch_to_local(Self, key):
        if len(Self.chk_dict) <= 0:
            return
        branch = Self.chk_dict[key]
        # main branch
        if branch.find("->") != -1:
            return
        local_branch = branch[branch.find("/")+1 : len(branch)]

        Self.cmd_at_path("git checkout -b " + local_branch + " " + branch)

    @classmethod
    def cmd_to_txt(Self, command, new_txt_file):
        # creating text file to write branches to if new_txt_file == True
        if new_txt_file:
            Self.txt_file = input("file: ")
            if Self.txt_file.find(".") == -1:
                Self.txt_file += ".txt"

        # writing to a text file all of our current branches
        os.chdir(Self.path)
        if Self.plat == "Windows":
            os.system("git " + command + " > \"" + Self.curr_dir + "\\" + Self.txt_file + "\"")
        else:
            os.system("git " + command + " > \"/" + Self.curr_dir + "/" + Self.txt_file + "\"")
        os.chdir(Self.curr_dir)

        # opening in notepad if we created a new text file
        if new_txt_file:
            app_cmd = "notepad " if Self.plat == "Windows" else "open -a TextEdit "
            os.system(app_cmd + Self.txt_file)

    @classmethod
    def cmd_at_path(Self, app):
        os.chdir(Self.path)
        os.system(app)
        os.chdir(Self.curr_dir)

    @classmethod
    def new_branch(Self, cmd, disp):
        Self.txt_file = "_______branch_______.txt"
        Self.cmd_to_txt(cmd, False)
        Self.chk_dict = {}
        with open(Self.txt_file) as file:
            inc = 1
            for line in file:
                line_strip = line.rstrip()
                Self.chk_dict[inc] = line_strip
                if disp:
                    print(str(inc) + ") " + line_strip)
                inc += 1    
            file.close()

        if Self.plat == "Windows":
            os.system("del " + Self.txt_file)
        else:
            os.system("rm " + Self.txt_file)