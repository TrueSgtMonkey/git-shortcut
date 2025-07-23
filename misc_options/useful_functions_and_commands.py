

import json
import os

from git_path import GitPath
from style import Color

TRAININGS_DICT_NAME = "trainings.json"

class UsefulFunctions:
    @classmethod
    def useful_functions_and_commands(self, git_path: GitPath):
        choice = 1
        while choice != 0:
            choice = int(input(
                "1) Replace String with another String\n" +
                "2) Open VSCode in " + Color.string(Color.CYAN, git_path.path) + "\n" +
                "3) Remove lines with string and output to new file\n" +
                "0) Exit Mode\n" +
                "Choice: "
            ))

            self.useful_func_command_pick(git_path, choice)

    @classmethod
    def useful_func_command_pick(self, git_path: GitPath, choice : int):
        match choice:
            case 1:
                self.replace_string_with_string()
            case 2:
                self.open_vscode_in_repo(git_path)
            case 3:
                self.remove_string_from_file_output_to_new(git_path)

    @classmethod
    def replace_string_with_string(self):
        old_char = input("Old String: ")
        new_char = input("New String: ")

        full_string = input("String: ")
        full_string = full_string.replace(old_char, new_char)
        print(full_string)
        
    @classmethod
    def open_vscode_in_repo(self, git_path: GitPath):
        git_path.cmd_at_path("code .")

    @classmethod
    def remove_string_from_file_output_to_new(self, git_path: GitPath):
        file_input_path: str  = input("input file: ")
        file_output_path: str = input("path to output: ")
        output_file_name: str = input("output file name: ")
        remove_str: str       = input("string to remove: ")
        
        file_input = open(file_input_path, "r")
        
        ## TODO: need a different character for linux
        file_output = open(file_output_path + "\\" + output_file_name, "w")
        
        for line in file_input.readlines():
            if line.find(remove_str) != -1:
                continue
            
            file_output.write(line)