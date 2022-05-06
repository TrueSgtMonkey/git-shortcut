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