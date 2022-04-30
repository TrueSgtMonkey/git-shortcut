import os

class GitPath:
    # constants
    SAVE_PATH = "path.txt"

    # variables
    curr_dir = os.getcwd()
    path = ""
    txt_file = ""
    path_loaded = False

    @classmethod
    def new_path(Self):
        # emulating do-while loop
        # making sure path is valid
        while True:
            Self.path = input("path: ")
            if os.path.isdir(Self.path):
                break

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