from style import Color

class GitUtilFunctions:
    @classmethod
    def get_continue_choice(self) -> int:
        cont = int(input(
            "Continue?\n" +
            "  " + Color.string(Color.GREEN, "1) Yes\n") +
            "  " + Color.string(Color.RED + Color.BOLD, "2) No\n") +
            "Choice: " 
        ))
        
        return cont