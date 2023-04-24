import atexit

COUNT_STRING = "prune_count: "
REBASE_STRING = "rebase_branch: "
SAVE_VAR_STRING = "save_var_file"

MAX_COUNT = 5

# keeps track of variables and saves all under __slots__
class GitSaveVars:
  __slots__ = (
    "prune_count",
    "rebase_branch",
    SAVE_VAR_STRING
  )

  # this is used as a static class
  # call this function instead of __init__
  # loads all the vars saved at the exit of the program
  # NOTE: resets state of this class!
  @classmethod
  def initialize(self) -> None:
    self.prune_count = 0
    self.rebase_branch = "origin/dev/cmrc/lnl"
    self.save_var_file = SAVE_VAR_STRING + ".txt"
    try:
      file = open(self.save_var_file, "r")
    except FileNotFoundError:
      return

    for line in file.readlines():
      if line.startswith(COUNT_STRING):
        line = line[len(COUNT_STRING):len(line)].strip()
        self.prune_count = int(line)
      elif line.startswith(REBASE_STRING):
        line = line[len(REBASE_STRING):len(line)].strip()
        self.rebase_branch = line
    
    file.close()

  # used to check if we have exceeded the number of operations that count 
  # toward a prune
  # we want to use a git prune or some other action if this condition is true
  @classmethod
  def addPruneCountCheck(self):
    self.prune_count += 1
    if self.prune_count >= MAX_COUNT:
      self.prune_count = 0
      return True
    
    return False

  @classmethod
  def set_rebase_branch(self, branch):
    self.rebase_branch = branch

  # iterates through all elements of the dictionary and saves all defined 
  # under __slots__
  @classmethod
  def saveVars(self):
    file = open(self.save_var_file, "w")
    for var in self.__dict__:
      if var in self.__slots__ and var != SAVE_VAR_STRING:
        file.write(var + ": " + str(self.__dict__[var]) + "\n")
    
    file.close()

# calls a save function on program close
atexit.register(GitSaveVars.saveVars)
