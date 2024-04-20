

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
                "0) Exit Mode\n" +
                "Choice: "
            ))

            self.useful_func_command_pick(git_path, choice)

    @classmethod
    def useful_func_command_pick(self, git_path: GitPath, choice : int):
        match choice:
            case 1:
                self.replace_string_with_string()

    @classmethod
    def replace_string_with_string(self):
        old_char = input("Old String: ")
        new_char = input("New String: ")

        full_string = input("String: ")
        full_string = full_string.replace(old_char, new_char)
        print(full_string)
