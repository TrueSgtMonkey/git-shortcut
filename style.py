class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m' # reset code

    ## adds the style passed in to the message passed in and performs reset
    @classmethod
    def string(Self, style, message):
        return style + message + Self.END

    ## shortcut method to call print with the string() function
    @classmethod
    def print(Self, style, message):
        print(Self.string(style, message))
