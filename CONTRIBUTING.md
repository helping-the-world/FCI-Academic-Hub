# 📖 Contributing Guide

Welcome to the **FCI Academic Hub**! This guide explains how to contribute materials and maintain consistency.

---

## 📋 Table of Contents

- [📖 Contributing Guide](#-contributing-guide)
  - [📋 Table of Contents](#-table-of-contents)
  - [📁 Project Structure](#-project-structure)
  - [🛠️ Scripts \& Tools](#️-scripts--tools)
  - [📝 Naming Conventions](#-naming-conventions)
    - [Course Folders](#course-folders)
    - [File Names](#file-names)
  - [➕ Adding a New Course](#-adding-a-new-course)
  - [📚 Adding Materials](#-adding-materials)
  - [⚠️ Common Mistakes](#️-common-mistakes)
  - [🔄 Pull Request Guidelines](#-pull-request-guidelines)
    - [Before Submitting](#before-submitting)
    - [Commit Format](#commit-format)
  - [🔒 Anonymous Contribution](#-anonymous-contribution)
    - [1. Anonymous GitHub Account](#1-anonymous-github-account)
    - [2. Configure Git (Local Only)](#2-configure-git-local-only)
    - [3. Clean File Metadata](#3-clean-file-metadata)
    - [4. Anonymous Commit](#4-anonymous-commit)
    - [5. Push with Anonymous Account](#5-push-with-anonymous-account)
    - [6. Switch GitHub Account for This Repo Only](#6-switch-github-account-for-this-repo-only)
      - [Option A: Use HTTPS with Token (Recommended)](#option-a-use-https-with-token-recommended)
      - [Option B: Use Separate SSH Key](#option-b-use-separate-ssh-key)
      - [Option C: Temporarily Override SSH Key](#option-c-temporarily-override-ssh-key)
      - [Verify Current Account](#verify-current-account)
    - [Quick Workflow](#quick-workflow)
    - [Privacy Checklist](#privacy-checklist)

---

## 📁 Project Structure

```
FCI/
├── mkdocs.yml                    # MkDocs configuration
├── docs/
│   ├── index.md                  # Homepage
│   ├── materials/courses/        # All course materials
│   └── programs/                 # Academic programs (ai, cyber-security, etc.)
├── scripts/                      # Utility scripts
├── templates/                    # Templates
└── CONTRIBUTING.md               # This file
```

---

## 🛠️ Scripts & Tools

All scripts are in `scripts/`. See [`scripts/README.md`](scripts/README.md) for full documentation.

| Script | Description |
|--------|-------------|
| [`create_course.py`](scripts/README.md#create_coursepy) | Create new course with all folders |
| [`rename_course.py`](scripts/README.md#rename_coursepy) | Rename a course slug |
| [`merge_courses.py`](scripts/README.md#merge_coursespy) | Merge duplicate courses |
| [`link_course.py`](scripts/README.md#link_coursepy) | Link course code to folder in term files |
| [`fix_missing_links.py`](scripts/README.md#fix_missing_linkspy) | Batch fix missing course links |
| [`update_taken_at.py`](scripts/README.md#update_taken_atpy) | Update "Taken At" sections |
| [`clean_metadata.py`](scripts/README.md#clean_metadatapy) | Remove metadata from files (privacy) |
| [`anon-commit.sh`](scripts/README.md#anon-commitsh) | Commit with randomized UTC timestamp |

> 💡 Use `--dry-run` with most scripts to preview changes.

---

## 📝 Naming Conventions

### Course Folders

| ✅ Correct | ❌ Incorrect |
|-----------|-------------|
| `data-structures` | `Data Structures` |
| `object-oriented-programming` | `OOP` |
| `software-engineering-1` | `SE1` |

**Rules:** lowercase, hyphens only, no spaces/underscores.

### File Names

| Type | Format | Example |
|------|--------|---------|
| Lecture | `lecture-##.pdf` | `lecture-01.pdf` |
| Assignment | `assignment-##.pdf` | `assignment-01.pdf` |
| Midterm | `mid-YYYY-model-X.pdf` | `mid-2024-model-A.pdf` |
| Final | `final-YYYY-model-X.pdf` | `final-2024.pdf` |

---

## ➕ Adding a New Course

**Recommended:** Use the script:

```bash
python3 scripts/create_course.py "Course Name" --code BSD101
```

This creates the folder structure, `index.md`, and updates the courses index.

**Manual:** See [`templates/course-template.md`](templates/course-template.md)

---

## 📚 Adding Materials

1. Locate: `docs/materials/courses/<course-slug>/`
2. Add files to the appropriate subfolder:

| Type | Folder |
|------|--------|
| Books | `book/` |
| Assignments | `assignments/` |
| Notes | `notes/` |
| Lectures | `lectures/` |
| Section | `section/` |
| Midterms | `exams/mid/` |
| Finals | `exams/final/` |

3. Update the course `index.md` with links to your files.

---

## ⚠️ Common Mistakes

| ❌ Mistake | ✅ Fix |
|-----------|-------|
| Duplicate courses | Check existing courses first |
| Spaces in folder names | Use lowercase with hyphens |
| Broken links | Use correct relative paths |
| Empty folders | Always create `index.md` |

---

## 🔄 Pull Request Guidelines

### Before Submitting

```bash
mkdocs build                        # Test build
mkdocs build 2>&1 | grep WARNING    # Check warnings
mkdocs serve                        # Preview locally
```

### Commit Format

```
<type>: <description>

Types: add, fix, update, docs
```

---

## 🔒 Anonymous Contribution

Contribute without revealing your identity.

### 1. Anonymous GitHub Account

Create using [ProtonMail](https://protonmail.com) or [Tutanota](https://tutanota.com) with a random username.

### 2. Configure Git (Local Only)

> ⚠️ This only affects THIS repo, not your global config.

```bash
cd /path/to/FCI
git config user.name "Anonymous"
git config user.email "anon@users.noreply.github.com"
```

To verify it's local only:
```bash
git config user.name              # Shows "Anonymous" (local)
git config --global user.name     # Shows your real name (unchanged)
```

### 3. Clean File Metadata

Use the provided script:

```bash
# Single file
python3 scripts/clean_metadata.py document.pdf

# Directory (recursive)
python3 scripts/clean_metadata.py docs/materials/courses/calculus/
```

The script handles PDFs, images, and Office documents. See `scripts/clean_metadata.py --help`.

### 4. Anonymous Commit

Use the provided script for randomized UTC timestamps:

```bash
./scripts/anon-commit.sh "add: new materials"
```

### 5. Push with Anonymous Account

Add your anonymous GitHub account as a remote:

```bash
# Add anonymous remote (one-time setup)
git remote add anon https://github.com/YOUR_ANON_USERNAME/FCI-Academic-Hub.git

# Push to anonymous account
git push anon main
```

Or push with credentials inline:

```bash
git push https://YOUR_ANON_USERNAME@github.com/YOUR_ANON_USERNAME/FCI-Academic-Hub.git main
```

> 💡 Use a [Personal Access Token](https://github.com/settings/tokens) instead of password.

### 6. Switch GitHub Account for This Repo Only

If you get permission errors like:
```
ERROR: Permission to org/repo.git denied to YourMainAccount.
fatal: Could not read from remote repository.
```

This means Git is using your main account's credentials. Here's how to fix it:

#### Option A: Use HTTPS with Token (Recommended)

1. Generate a [Personal Access Token](https://github.com/settings/tokens) from your anonymous account
2. **Clear cached credentials first** (important!):

```bash
# Clear stored credentials for github.com
git credential reject <<EOF
protocol=https
host=github.com
EOF

# Or remove from credential store file
sed -i '/github.com/d' ~/.git-credentials 2>/dev/null
```

3. Configure the remote with your anonymous username:

```bash
# Remove existing origin if needed
git remote remove origin

# Add origin with your anonymous username embedded
git remote add origin https://YOUR_ANON_USERNAME@github.com/ORG/FCI-Academic-Hub.git

# Push (will prompt for password - use your token)
git push -u origin main
```

4. To save credentials for **this repo only** (not global):

```bash
# Create a local credential store for this repo only
git config --local credential.helper 'store --file=.git/.git-credentials'

# Set credentials to use only for this repo's URL
git config --local credential.https://github.com.username YOUR_ANON_USERNAME

# Next push will save the token locally in .git/.git-credentials
git push origin main
# Enter your token when prompted
```

> 💡 This stores credentials inside `.git/` folder, so they only apply to this repo and won't affect your other projects.

> ⚠️ **Still getting permission denied?** Your system may cache credentials. Try:
> ```bash
> # Check credential helpers
> git config --list | grep credential
> 
> # If using credential-cache, clear it
> git credential-cache exit
> 
> # If using GNOME Keyring or libsecret (Linux)
> secret-tool clear server github.com
> 
> # If using macOS Keychain
> git credential-osxkeychain erase <<EOF
> host=github.com
> protocol=https
> EOF
> ```

#### Option B: Use Separate SSH Key

1. Generate a new SSH key for anonymous account:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_anon -C "anon@users.noreply.github.com"
```

2. Add the public key to your anonymous GitHub account (Settings → SSH Keys)

3. Create/edit `~/.ssh/config`:

```
# Anonymous GitHub account
Host github-anon
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_anon
    IdentitiesOnly yes
```

4. Use the custom host in your remote:

```bash
git remote remove origin
git remote add origin git@github-anon:ORG/FCI-Academic-Hub.git
git push -u origin main
```

#### Option C: Temporarily Override SSH Key

```bash
# Push using specific SSH key (one-time)
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_anon" git push origin main
```

#### Verify Current Account

```bash
# Check which account SSH is using
ssh -T git@github.com

# Check remote URL
git remote -v

# Check local git config
git config user.name
git config user.email
```

### Quick Workflow

```bash
cd /path/to/FCI
git config user.name "Anonymous"
git config user.email "anon@users.noreply.github.com"

cp ~/my-notes.pdf docs/materials/courses/calculus/notes/
python3 scripts/clean_metadata.py docs/materials/courses/calculus/notes/

git add .
./scripts/anon-commit.sh "add: calculus notes"
git push anon main
```

### Privacy Checklist

- [ ] Anonymous GitHub account
- [ ] Local git config set (not global)
- [ ] Metadata cleaned (`python3 scripts/clean_metadata.py`)
- [ ] No personal info in files/commits
- [ ] Push to anonymous remote

---

**Thank you for contributing!** 🎓
