# 🛠️ Scripts Documentation

This folder contains utility scripts for managing the FCI Academic Hub.

## 📋 Available Scripts

### Course Management
| Script | Description |
|--------|-------------|
| [create_course.py](#create_coursepy) | Create a new course with folder structure |
| [rename_course.py](#rename_coursepy) | Rename a course and update all links |
| [merge_courses.py](#merge_coursespy) | Merge duplicate courses into one |
| [link_course.py](#link_coursepy) | Link a course code to its folder in term files |
| [fix_missing_links.py](#fix_missing_linkspy) | Batch fix all missing course links |
| [update_taken_at.py](#update_taken_atpy) | Update "Taken At" sections in all courses |
| [mcq_to_pdf.py](#mcq_to_pdfpy) | Convert MCQ text files to PDF |

### 🔒 Privacy Tools
| Script | Description |
|--------|-------------|
| [clean_metadata.py](#clean_metadatapy) | Remove identifying metadata from files |
| [anon-commit.sh](#anon-commitsh) | Create commits with anonymous timestamps |

---

## create_course.py

Creates a new course with proper folder structure and template files.

### Usage

```bash
python3 scripts/create_course.py "Course Name"
python3 scripts/create_course.py "Course Name" --code BSD101
python3 scripts/create_course.py "Course Name" --code BSD101 --slug my-course
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `course_name` | Yes | Display name of the course |
| `--code` | No | Course code (default: XXX000) |
| `--slug` | No | Custom URL slug (auto-generated if not provided) |

### Example

```bash
python3 scripts/create_course.py "Machine Learning" --code CSD450
```

Creates:
```
docs/materials/courses/machine-learning/
├── index.md
├── book/
├── assignments/
├── notes/
├── lectures/
├── section/
└── exams/
    ├── mid/
    └── final/
```

---

## rename_course.py

Renames a course and updates all references throughout the project.

### Usage

```bash
python3 scripts/rename_course.py <old-slug> <new-slug>
python3 scripts/rename_course.py <old-slug> <new-slug> --name "New Name"
python3 scripts/rename_course.py <old-slug> <new-slug> --dry-run
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `old_slug` | Yes | Current course folder name |
| `new_slug` | Yes | New course folder name |
| `--name` | No | New display name for the course |
| `--dry-run` | No | Preview changes without modifying files |

### What It Updates

1. Course folder name
2. Course's index.md title
3. `courses/index.md` entries
4. All program term file links
5. "Taken At" sections in all courses

### Example

```bash
# Preview changes
python3 scripts/rename_course.py data-structure data-structures --dry-run

# Apply changes
python3 scripts/rename_course.py data-structure data-structures --name "Data Structures"
```

---

## merge_courses.py

Merges two duplicate courses by copying files and updating all references.

### Usage

```bash
python3 scripts/merge_courses.py <source-course> <destination-course>
python3 scripts/merge_courses.py <source-course> <destination-course> --dry-run
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `source` | Yes | Course to merge FROM (will be deleted) |
| `destination` | Yes | Course to merge INTO (will be kept) |
| `--dry-run` | No | Preview changes without modifying files |

### What It Does

1. Copies all files from source to destination
2. Removes source from `courses/index.md`
3. Updates all term file links to point to destination
4. Deletes the source course folder
5. Updates "Taken At" sections

### Example

```bash
# Preview merge
python3 scripts/merge_courses.py programming-principles fundamentals-of-programming --dry-run

# Perform merge
python3 scripts/merge_courses.py programming-principles fundamentals-of-programming
```

⚠️ **Warning:** The source course will be deleted after merging!

---

## link_course.py

Links a specific course code to its course folder in program term files.

### Usage

```bash
python3 scripts/link_course.py <course-code> <course-slug>
python3 scripts/link_course.py <course-code> <course-slug> --dry-run
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `course_code` | Yes | Course code (e.g., BSD227, CSD230) |
| `course_slug` | Yes | Course folder name (e.g., ordinary-differential-equations) |
| `--dry-run` | No | Preview changes without modifying files |

### Example

```bash
# Preview changes
python3 scripts/link_course.py BSD227 ordinary-differential-equations --dry-run

# Apply changes
python3 scripts/link_course.py BSD227 ordinary-differential-equations
```

### Course Code Formats

- `BSD###` - Basic Science Department
- `CSD###` - Computer Science Department
- `ISD###` - Information Systems Department
- `SEN###` - Software Engineering
- `CSC###` - Computer Science Core
- `UNI###` - University Requirements

---

## fix_missing_links.py

Automatically finds and fixes all missing course links in term files.

### Usage

```bash
python3 scripts/fix_missing_links.py           # Preview changes
python3 scripts/fix_missing_links.py --apply   # Apply changes
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--apply` | No | Apply changes (default is preview only) |

### What It Does

1. Scans all term files in `docs/programs/`
2. Finds rows with empty link columns
3. Matches course codes to existing course folders
4. Updates all links automatically

### Example Output

```
Found 48 missing links:
  ✅ Can fix: 28
  ❌ Cannot fix (no matching folder): 20

[Links that will be fixed]
  📁 docs/programs/general-hours/year2/year2-term2.md
      BSD227 -> ordinary-differential-equations/
      BSD228 -> advanced-math/
```

---

## update_taken_at.py

Updates the "Taken At" section in all course index files based on which program term files reference each course.

### Usage

```bash
python3 scripts/update_taken_at.py           # Update only changed files
python3 scripts/update_taken_at.py --force   # Force update all files
python3 scripts/update_taken_at.py --list    # List courses not in curriculum
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--force` | No | Re-write all course files |
| `--list` | No | Only list courses not in any term file |

### How It Works

1. Scans all program term files (`docs/programs/<program>/year<N>/*.md`)
2. Finds which courses are referenced in each term
3. Updates the "📅 Taken At" section in each course's index.md

### Example Output

```
⚠️  Courses NOT in any program term file (need to be added):
   - advanced-math
   - big-data-analysis
   - physics
```

---

## mcq_to_pdf.py

Converts Multiple Choice Question (MCQ) text files to formatted PDF documents.

### Usage

```bash
python3 scripts/mcq_to_pdf.py <input.txt> <output.pdf> [title]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `input.txt` | Yes | Input text file with MCQ questions |
| `output.pdf` | Yes | Output PDF file path |
| `title` | No | Title for the PDF document |

### Input Format

```text
Q1. What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid

Q2. Which planet is known as the Red Planet?
A) Venus
B) Mars
C) Jupiter
D) Saturn
```

### Example

```bash
python3 scripts/mcq_to_pdf.py questions.txt exam.pdf "Final Exam 2024"
```

---

## 🔧 Common Workflows

### Adding a New Course

```bash
# 1. Create the course
python3 scripts/create_course.py "New Course" --code CSD500

# 2. Link the course in term files
python3 scripts/link_course.py CSD500 new-course

# 3. Update Taken At sections
python3 scripts/update_taken_at.py --force
```

### Fixing Missing Course Links

```bash
# 1. Preview what will be fixed
python3 scripts/fix_missing_links.py

# 2. Apply the fixes
python3 scripts/fix_missing_links.py --apply

# 3. Update Taken At sections
python3 scripts/update_taken_at.py --force
```

### Linking a Single Course

```bash
# Preview first
python3 scripts/link_course.py BSD227 ordinary-differential-equations --dry-run

# Apply the link
python3 scripts/link_course.py BSD227 ordinary-differential-equations
```

### Fixing a Course Name Typo

```bash
# Preview changes first
python3 scripts/rename_course.py data-sturcture data-structures --dry-run

# Apply the fix
python3 scripts/rename_course.py data-sturcture data-structures
```

### Merging Duplicate Courses

```bash
# Preview what will happen
python3 scripts/merge_courses.py old-course new-course --dry-run

# Perform the merge
python3 scripts/merge_courses.py old-course new-course
```

---

## clean_metadata.py

Removes identifying metadata from files (PDF, images, Office documents) before contributing.

### Usage

```bash
python3 scripts/clean_metadata.py <file1> [file2] ...
python3 scripts/clean_metadata.py --all <directory>
python3 scripts/clean_metadata.py --info <file>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `files` | Yes* | Files to clean |
| `--all DIR` | Yes* | Clean all files in directory recursively |
| `--info FILE` | No | Show metadata without cleaning |
| `--dry-run` | No | Preview what would be cleaned |
| `--verbose` | No | Show detailed output |

*Either `files` or `--all` is required.

### Supported Formats

- **Documents:** PDF, DOCX, XLSX, PPTX, DOC, XLS, PPT
- **Images:** JPEG, PNG, GIF, WebP, TIFF, BMP

### Examples

```bash
# Clean a single PDF
python3 scripts/clean_metadata.py document.pdf

# Clean all PDFs in a folder
python3 scripts/clean_metadata.py *.pdf

# Clean all files in course folder
python3 scripts/clean_metadata.py --all docs/materials/courses/calculus/

# View file metadata
python3 scripts/clean_metadata.py --info document.pdf

# Preview what would be cleaned
python3 scripts/clean_metadata.py --all docs/ --dry-run
```

### Requirements

Requires `exiftool`:
```bash
# Linux (Debian/Ubuntu)
sudo apt install libimage-exiftool-perl

# macOS
brew install exiftool
```

---

## anon-commit.sh

Creates Git commits with anonymized timestamps to protect contributor privacy.

### Usage

```bash
./scripts/anon-commit.sh "commit message"
./scripts/anon-commit.sh "commit message" --no-random
```

### Features

- Uses UTC timezone (hides your location)
- Randomizes commit time within past week
- Verifies anonymous git config
- Warns if email looks personal

### Example

```bash
# Stage your files
git add docs/materials/courses/calculus/notes/

# Clean metadata first!
python3 scripts/clean_metadata.py docs/materials/courses/calculus/notes/*.pdf

# Create anonymous commit
./scripts/anon-commit.sh "add: calculus lecture notes"
```

### Setup Anonymous Git Config

Before using:
```bash
git config user.name "Anonymous"
git config user.email "anonymous@users.noreply.github.com"
```

---

## 📝 Notes

- All scripts use Python 3 and should work on Linux, macOS, and Windows
- Always use `--dry-run` first to preview changes
- Run `mkdocs build` after making changes to verify no broken links
- Scripts update relative paths automatically

## 🔗 Related Documentation

- [Contributing Guide](../CONTRIBUTING.md) - How to contribute to the project
- [Anonymous Contribution Guide](../CONTRIBUTING.md#-anonymous-contribution) - Privacy-focused contribution
- [Course Template](../templates/course-template.md) - Template for course pages
