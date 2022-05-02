#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main()
{
  int x = chdir("/Users/codythompson/Documents/GitHub/git-shortcut");
  int y = system("brun run.bat\n");
  
  printf("first, last: %d, %d", x, y);

  return 0;
}
