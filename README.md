# Git Shortcut

## Usage
![alt text](./images/CLI.png)
* Here is the CLI and how it looks when GitShortcut is running.

### GIT SHORTCUTS
* These are all the `positive` options `(1, 2, 3, 4, ...)`
* These options are all git related and are shortcuts for git commands that are commonly used in MRC.

Below are the explanations for the most useful of these:
* `2. git rebase with <rebase_branch>`
    * This runs `git remote update` and then `git rebase <rebase_branch>`
    * In the image above, we are currently rebasing with `origin/dev/cmrc/lnl` whenever we run this command.
    * Useful for quickly making sure you are up to date.
    * Running this enough times will activate a `git prune` command to keep things running smoothly.
* `3. git checkout <list_of_branches>` and `4. git branch -D <list_of_branches>`
    * Both of these commands display a list of all the branches you have on your current repo.
    * You then select one of these by their ID to switch to them or delete them.
* `6. git checkout -b <branch_name>`
    * Simply a shortcut for the `git checkout -b` git command.
    * Will create a new branch and then switch to it.
* `7. amend PR code review`
    * runs `git add .`, `git commit --amend`, and then prompts the user for the branch to push from, and the remote branch to push to.
    * This is great for amending a commit to a PR and not creating a new commit on accident.
* `8. git push --set-upstream origin <current_branch_name>`
    * This creates a new branch on the remote with the name of the current branch after adding a commit or amending a commit.
    * Useful for PTL and beyond.
    * Also works for already existing branches on the remote (with the `git commit --amend` option)
* `9. git restore <list_of_files>`
    * This one is great for checking what may need to be `git restore`'d
    * Sometimes not too handy as not *everything* shows up under this.
        * You may still need to go into git-bash or cmd for this.
* `11. get all files altered in git commit <commit-id>`
    * This returns all the files altered in a git commit and copies them to into a new directory with the title of the hash of the commit.

### MISC SHORTCUTS
* As the name implies, these are more for repository-related functions.