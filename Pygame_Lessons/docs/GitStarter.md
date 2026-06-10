# Basic Git Workflow (Main Branch Only)

Here is a straightforward guide to the essential Git commands for working entirely on the `main` branch. This workflow is perfect for personal projects or simple collaborations where you don't need complex branching strategies.

### Prerequisites: Initial Setup
If you haven't used Git on your computer before, you need to introduce yourself to it. Open your terminal or command prompt and run these two commands (you only need to do this once):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

### Step 1: Start a Git Repository
To start tracking changes in a project folder, navigate to that folder in your terminal and initialize Git.
```bash
git init
```
*This creates a hidden `.git` folder and sets up your default `main` branch.*

### Step 2: Check Your Status
This is the most important command in Git. Use it constantly to see what files are changed, what is ready to be saved, and what branch you are on.
```bash
git status
```

### Step 3: Stage Your Changes (Add)
When you make changes to files, Git notices, but it won't save them until you tell it exactly which files to include in the next save point (this is called "staging").

To stage a specific file:
```bash
git add filename.txt
```
To stage **all** changed files in the folder at once:
```bash
git add .
```

### Step 4: Save Your Changes (Commit)
Once your files are staged, you bundle them into a "commit." A commit is a permanent snapshot of your project at that exact moment. Always include a short, descriptive message.
```bash
git commit -m "Add a brief description of what you changed"
```

### Step 5: View Your History (Log)
To see a timeline of all the commits (saves) you have made:
```bash
git log
```
*Tip: If the log is very long, you can press `q` to exit the log view.*

---

### Step 6: Connect to a Remote (Like GitHub)
If you want to back up your project online or share it (e.g., on GitHub), create an empty repository on their website first. Then, link your local folder to that online repository:
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
```
*(`origin` is just the standard nickname Git uses for your online repository).*

### Step 7: Send Your Changes Online (Push)
To send your local commits up to your online repository on the `main` branch:
```bash
git push -u origin main
```
*Note: The `-u` tells Git to remember this connection. For all future pushes in this project, you can simply type `git push`.*

### Step 8: Get Updates from Online (Pull)
If you (or a teammate) made changes directly on GitHub, or if you are working from a different computer, you need to download those changes to your local folder before you start working.
```bash
git pull origin main
```

---

### The Daily Workflow Summary
Once everything is set up, your day-to-day process will look exactly like this continuous loop:

1. Write code / edit files.
2. `git status` (to see what changed)
3. `git add .` (to stage all changes)
4. `git commit -m "describe changes"` (to save locally)
5. `git push` (to back up online)