#!/usr/bin/env python3
"""
Script to create a new course with proper folder structure.

This script will:
1. Create course folder with subfolders (book, assignments, notes, lectures, section, exams)
2. Create index.md with template content
3. Add course to courses/index.md

Usage:
    python3 create_course.py "Course Name"
    python3 create_course.py "Course Name" --code BSD101
    python3 create_course.py "Course Name" --code BSD101 --slug my-course

Examples:
    python3 create_course.py "Machine Learning"
    python3 create_course.py "Machine Learning" --code CSD450
    python3 create_course.py "Machine Learning" --code CSD450 --slug ml-course
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
COURSES_DIR = BASE_DIR / "docs" / "materials" / "courses"
COURSES_INDEX = COURSES_DIR / "index.md"

# Course template
COURSE_TEMPLATE = '''# 📘 {course_name}

> **Course Code:** {course_code}

---

## 📅 Taken At

| Program | Year | Term | Link |
|---------|------|------|------|
| General Hours | Year X | Term X | [View Term](../../../programs/general-hours/yearX/yearX-termX.md) |
| AI | Year X | Term X | [View Term](../../../programs/ai/yearX/yearX-termX.md) |
| Cyber Security | Year X | Term X | [View Term](../../../programs/cyber-security/yearX/yearX-termX.md) |
| Software Engineering | Year X | Term X | [View Term](../../../programs/software-engineering/yearX/yearX-termX.md) |

> 📝 **Note:** Update the year/term values and remove programs that don't include this course.

---

## 📚 Books

| # | Book | Author | Description |
|---|------|--------|-------------|
| 1 | [Book Name](./book/) | - | Main textbook |

---

## 🧾 Assignments

| # | File | Description |
|---|------|--------------|
| 1 | [Assignment 1](./assignments/) | - |

---

## 🧠 Notes

| # | File | Description |
|---|------|--------------|
| 1 | [Notes](./notes/) | - |

---

## 🎥 Lectures

| # | Lecture | Instructor | Description |
|---|---------|------------|--------------|
| 1 | [Lecture 1](./lectures/) | - | - |

---

## 📝 Section

| # | Section | Instructor | Description |
|---|---------|------------|--------------|
| 1 | [Section 1](./section/) | - | - |

---

## 📋 Exams

### 📝 Midterm

| # | File | Year | Description |
|---|------|------|-------------|
| 1 | [Midterm](./exams/mid/) | - | - |

### 📝 Final

| # | File | Year | Description |
|---|------|------|-------------|
| 1 | [Final](./exams/final/) | - | - |

---
'''


def slugify(name):
    """Convert course name to URL-friendly slug."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def create_course_folder(course_dir):
    """Create course folder with all subfolders."""
    subfolders = [
        "book",
        "assignments",
        "notes",
        "lectures",
        "section",
        "exams/mid",
        "exams/final"
    ]
    
    for subfolder in subfolders:
        (course_dir / subfolder).mkdir(parents=True, exist_ok=True)
    
    return subfolders


def create_course_index(course_dir, course_name, course_code):
    """Create course index.md with template."""
    content = COURSE_TEMPLATE.format(
        course_name=course_name,
        course_code=course_code
    )
    
    index_file = course_dir / "index.md"
    index_file.write_text(content, encoding='utf-8')
    return index_file


def add_to_courses_index(course_name, course_slug, course_code):
    """Add course to courses/index.md if not already present."""
    if not COURSES_INDEX.exists():
        print(f"  ⚠️  courses/index.md not found, skipping index update")
        return False
    
    content = COURSES_INDEX.read_text(encoding='utf-8')
    
    # Check if course already exists
    if course_slug in content:
        print(f"  ⚠️  Course already in index.md")
        return False
    
    # Find the Course Directory table and add entry
    # Look for the table header pattern
    table_pattern = r'(\| Course Code \| Course Name \| Course Page \|\n\|[-|\s]+\|)'
    match = re.search(table_pattern, content)
    
    if match:
        # Add new row after the table header
        new_row = f"\n| {course_code} | {course_name} | [Open](./{course_slug}/index.md) |"
        
        # Find where to insert (after the header separator)
        insert_pos = match.end()
        new_content = content[:insert_pos] + new_row + content[insert_pos:]
        
        COURSES_INDEX.write_text(new_content, encoding='utf-8')
        return True
    else:
        print(f"  ⚠️  Could not find course table in index.md")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Create a new course with proper folder structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 create_course.py "Machine Learning"
    python3 create_course.py "Machine Learning" --code CSD450
    python3 create_course.py "Machine Learning" --code CSD450 --slug ml-course
        """
    )
    parser.add_argument("course_name", help="Name of the course (e.g., 'Machine Learning')")
    parser.add_argument("--code", default="XXX000", help="Course code (e.g., BSD101, CSD221)")
    parser.add_argument("--slug", help="Custom URL slug (default: auto-generated from name)")
    
    args = parser.parse_args()
    
    course_name = args.course_name
    course_code = args.code
    course_slug = args.slug if args.slug else slugify(course_name)
    course_dir = COURSES_DIR / course_slug
    
    print()
    print("=" * 60)
    print("  CREATE NEW COURSE")
    print("=" * 60)
    print(f"\n  Name: {course_name}")
    print(f"  Code: {course_code}")
    print(f"  Slug: {course_slug}")
    print(f"  Path: {course_dir.relative_to(BASE_DIR)}")
    print()
    
    # Check if course already exists
    if course_dir.exists():
        print(f"❌ Error: Course folder already exists: {course_slug}/")
        print(f"   Use a different name or delete the existing folder.")
        sys.exit(1)
    
    # Step 1: Create folder structure
    print("[Step 1] Creating folder structure...")
    subfolders = create_course_folder(course_dir)
    print(f"  ✅ Created {len(subfolders)} subfolders")
    
    # Step 2: Create index.md
    print("\n[Step 2] Creating course index.md...")
    index_file = create_course_index(course_dir, course_name, course_code)
    print(f"  ✅ Created {index_file.relative_to(BASE_DIR)}")
    
    # Step 3: Add to courses index
    print("\n[Step 3] Adding to courses/index.md...")
    if add_to_courses_index(course_name, course_slug, course_code):
        print(f"  ✅ Added to courses index")
    
    # Summary
    print()
    print("=" * 60)
    print("  COURSE CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\n  📁 {course_slug}/")
    print(f"     ├── index.md")
    print(f"     ├── book/")
    print(f"     ├── assignments/")
    print(f"     ├── notes/")
    print(f"     ├── lectures/")
    print(f"     ├── section/")
    print(f"     └── exams/")
    print(f"         ├── mid/")
    print(f"         └── final/")
    print()
    print("  Next steps:")
    print(f"    1. Edit {course_slug}/index.md to update course details")
    print(f"    2. Add course to appropriate term file in docs/programs/")
    print(f"    3. Run: python3 scripts/update_taken_at.py --force")
    print()


if __name__ == "__main__":
    main()
