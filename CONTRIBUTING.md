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

```bash
cd /path/to/FCI
git config user.name "Anonymous"
git config user.email "anon@users.noreply.github.com"
```

> This only affects THIS repo, not your global config.

### 3. Clean File Metadata

Use the provided script:

```bash
# Single file
python3 scripts/clean_metadata.py document.pdf

# All PDFs in docs/
python3 scripts/clean_metadata.py docs/**/*.pdf

# Recursive
python3 scripts/clean_metadata.py --recursive docs/
```

The script handles PDFs, images, and Office documents. See `scripts/clean_metadata.py --help`.

### 4. Anonymous Commit

Use the provided script for randomized UTC timestamps:

```bash
./scripts/anon-commit.sh "add: new materials"
```

### Quick Workflow

```bash
cd /path/to/FCI
git config user.name "Anonymous"
git config user.email "anon@users.noreply.github.com"

cp ~/my-notes.pdf docs/materials/courses/calculus/notes/
python3 scripts/clean_metadata.py docs/materials/courses/calculus/notes/my-notes.pdf

git add .
./scripts/anon-commit.sh "add: calculus notes"
git push origin main
```

### Privacy Checklist

- [ ] Anonymous GitHub account
- [ ] Local git config set
- [ ] Metadata cleaned (`python3 scripts/clean_metadata.py`)
- [ ] No personal info in files/commits

---

**Thank you for contributing!** 🎓
