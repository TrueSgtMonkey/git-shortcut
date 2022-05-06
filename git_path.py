import os
import platform

class GitPath:
    # constants
    SAVE_PATH = "path.txt"

    # variables
    curr_dir = os.getcwd()
    path = ""
    txt_file = ""
    path_loaded = False
    plat = platform.system()
    new_branch_detected = True
    chk_dict = {}

    @classmethod
    def new_path(Self):
        # making sure path is valid - returning if not
        old_path = Self.path
        Self.path = input("path: ")
        if not os.path.isdir(Self.path):
            print("\'" + Self.path + "\' does not exist...\n switching back to " + old_path)
            Self.path = old_path
            return

        # no matter what, this will write to a valid file
        file = open(Self.SAVE_PATH, "w")
        file.write(Self.path)
        file.close()

        Self.path_loaded = True

    @classmethod
    def load_path(Self, file):
        Self.path = file.readline()
        if not os.path.isdir(Self.path):
            print("loaded file was not a directory. Enter a new directory below.")
            Self.new_path()
            return

        Self.path_loaded = True

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

        if Self.plat == "Windows":
            os.system("del " + Self.txt_file)
        else:
            os.system("rm " + Self.txt_file)