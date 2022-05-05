#git shortcut main
import os
import subprocess
from git_path import GitPath

MIN_OPTIONS = -4
MAX_OPTIONS = 4

def main():
    # keeping this because it is useful to know which OS version is running
    print("Version: " + GitPath.plat)
    option = -999
    while (option < MIN_OPTIONS) or (option > MAX_OPTIONS):
        option = user_options()

    if option != 0:
        # setting up paths to directories - no matter what the option!
        if not GitPath.path_loaded:
            try:
                f = open(GitPath.SAVE_PATH)
                GitPath.load_path(f)

                f.close()
            except FileNotFoundError:
                GitPath.new_path()

        run_commands(option)
    
    return option

def user_options():
    print("WARNING: Make sure to put this outside of your git project!")
    choice = int(input(
                   "#)  Option\n" +
                   "1)  git branch > <file>\n" +
                   "2)  git diff > <file>\n" +
                   "3)  git checkout <list_of_branches>\n" +
                   "4)  git branch -D <list_of_branches>\n" +
                   "0)  Exit\n" +
                   "-1) Change Path\n" +
                   "-2) Open cmd in directory\n" +
                   "-3) Open git-bash in directory\n" + 
                   "-4) Explore Git repo\n" +
                   "Choice: "
                ))

    return choice

def run_commands(option):
    if option == 1:
        cmd_to_txt("branch", True)
    elif option == 2:
        cmd_to_txt("diff", True)
    elif option == 3:
        git_cmd_shortcut("checkout")
    elif option == 4:
        git_cmd_shortcut("branch -D")
    elif option == -1:
        GitPath.new_path()
    elif option == -2:
        cmd_at_path("start cmd.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -3:
        cmd_at_path("start git-bash.exe" if GitPath.plat == "Windows" else "open -a Terminal .")
    elif option == -4:
        explore_at_path()

def cmd_to_txt(command, new_txt_file):
    # creating text file to write branches to if new_txt_file == True
    if new_txt_file:
        GitPath.txt_file = input("file: ")
        if GitPath.txt_file.find(".") == -1:
            GitPath.txt_file += ".txt"

    # writing to a text file all of our current branches
    os.chdir(GitPath.path)
    if GitPath.plat == "Windows":
        os.system("git " + command + " > \"" + GitPath.curr_dir + "\\" + GitPath.txt_file + "\"")
    else:
        os.system("git " + command + " > \"/" + GitPath.curr_dir + "/" + GitPath.txt_file + "\"")
    os.chdir(GitPath.curr_dir)

    # opening in notepad if we created a new text file
    if new_txt_file:
        app_cmd = "notepad " if GitPath.plat == "Windows" else "open -a TextEdit "
        os.system(app_cmd + GitPath.txt_file)

def cmd_at_path(app):
    os.chdir(GitPath.path)
    os.system(app)
    os.chdir(GitPath.curr_dir)

def git_cmd_shortcut(cmd):
    GitPath.txt_file = "_______branch_______.txt"
    cmd_to_txt("branch", False)
    my_choice = 0
    if len(GitPath.chk_dict) == 0:
        with open(GitPath.txt_file) as file:
            inc = 1
            for line in file:
                line_strip = line.rstrip()
                GitPath.chk_dict[inc] = line_strip
                print(str(inc) + ") " + line_strip)
                inc += 1
            
    my_choice = int(input("Checkout branch (integer): "))
    if my_choice < 1 or my_choice >= len(GitPath.chk_dict):
        return
    
    cmd_at_path("git " + cmd + " " + GitPath.chk_dict[my_choice])
    
    if cmd == "branch -D":
        print("deleting branch...")
        GitPath.chk_dict = {}
    
    if GitPath.plat == "Windows":
        os.system("del " + GitPath.txt_file)
    else:
        os.system("rm " + GitPath.txt_file)
    
def explore_at_path():
    if GitPath.plat == "Windows":
        path = os.path.realpath(GitPath.path)
        os.startfile(path)
    else: 
        os.system("open %s" % GitPath.path)

if __name__ == '__main__':
    retVal = main()
    while retVal != 0:
        retVal = main()