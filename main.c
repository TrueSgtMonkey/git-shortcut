#include <stdio.h>
#include <stdlib.h>

int main()
{
    int choice;
    printf("1) cmd\n2) git-bash.exe\n0) Exit\nChoice: ");
    scanf("%d", &choice);
    if (choice <= 0) {
        return 0;
    }
    
    switch (choice) {
        case 1:
            system("python gs.py");
            break;
        case 2:
            system("git-bash.exe -c \"python gs.py\"");
            break;
    }
    
    printf("Oh, that went well!\n");
    return 0;
}