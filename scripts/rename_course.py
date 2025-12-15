#!/usr/bin/env python3
"""
Script to rename a course and update all references throughout the project.

This script will:
1. Rename the course folder
2. Update courses/index.md (course entry)
3. Update all program term files (links)
4. Update the course's index.md (title and references)
5. Update "Taken At" sections in all courses

Usage:
    python3 rename_course.py <old-slug> <new-slug>
    python3 rename_course.py <old-slug> <new-slug> --name "New Course Name"
    python3 rename_course.py <old-slug> <new-slug> --dry-run

Examples:
    python3 rename_course.py data-structure data-structures
    python3 rename_course.py ml machine-learning --name "Machine Learning"
    python3 rename_course.py old-course new-course --dry-run
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
COURSES_DIR = DOCS_DIR / "materials" / "courses"
PROGRAMS_DIR = DOCS_DIR / "programs"
COURSES_INDEX = COURSES_DIR / "index.md"


def print_header(text):
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_step(step_num, text):
    """Print a step indicator."""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 50)


def rename_course_folder(old_slug, new_slug, dry_run=False):
    """Rename the course folder."""
    old_dir = COURSES_DIR / old_slug
    new_dir = COURSES_DIR / new_slug
    
    if not old_dir.exists():
        return False, f"Source folder not found: {old_slug}/"
    
    if new_dir.exists():
        return False, f"Destination folder already exists: {new_slug}/"
    
    if not dry_run:
        shutil.move(str(old_dir), str(new_dir))
    
    return True, f"Renamed {old_slug}/ → {new_slug}/"


def update_course_index_file(new_slug, new_name, dry_run=False):
    """Update the course's own index.md with new name."""
    index_file = COURSES_DIR / new_slug / "index.md"
    
    if not index_file.exists():
        return False, "Course index.md not found"
    
    content = index_file.read_text(encoding='utf-8')
    original = content
    
    # Update the title (# 📘 Course Name)
    if new_name:
        content = re.sub(
            r'^# 📘 .+$',
            f'# 📘 {new_name}',
            content,
            flags=re.MULTILINE
        )
    
    if content != original:
        if not dry_run:
            index_file.write_text(content, encoding='utf-8')
        return True, "Updated course title"
    
    return False, "No title change needed"


def update_courses_index(old_slug, new_slug, new_name, dry_run=False):
    """Update courses/index.md with new slug and optionally new name."""
    if not COURSES_INDEX.exists():
        return False, "courses/index.md not found"
    
    content = COURSES_INDEX.read_text(encoding='utf-8')
    original = content
    changes = []
    
    # Update links in the course table
    # Pattern: | CODE | Name | [Open](./old-slug/index.md) |
    old_link = f"./{old_slug}/index.md"
    new_link = f"./{new_slug}/index.md"
    
    if old_link in content:
        content = content.replace(old_link, new_link)
        changes.append("Updated table link")
    
    # Update links in category lists
    # Pattern: - [Course Name](./old-slug/index.md)
    old_list_link = f"](./{old_slug}/index.md)"
    new_list_link = f"](./{new_slug}/index.md)"
    
    if old_list_link in content:
        content = content.replace(old_list_link, new_list_link)
        changes.append("Updated category link")
    
    # Optionally update course name in table
    if new_name and old_slug != new_slug:
        # Try to find and update the course name in table row
        pattern = rf'\| ([A-Z]{{2,3}}[0-9]+) \| ([^|]+) \| \[Open\]\(\.\/{re.escape(new_slug)}\/index\.md\) \|'
        match = re.search(pattern, content)
        if match:
            old_row = match.group(0)
            code = match.group(1)
            new_row = f"| {code} | {new_name} | [Open](./{new_slug}/index.md) |"
            content = content.replace(old_row, new_row)
            changes.append("Updated course name in table")
    
    if content != original:
        if not dry_run:
            COURSES_INDEX.write_text(content, encoding='utf-8')
        return True, ", ".join(changes)
    
    return False, "No changes needed"


def update_term_files(old_slug, new_slug, new_name, dry_run=False):
    """Update all program term files with new slug and optionally new name."""
    updated_files = []
    
    for md_file in DOCS_DIR.rglob("*.md"):
        # Skip courses directory (we handle that separately)
        if "courses" in str(md_file):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        if old_slug not in content:
            continue
        
        original = content
        
        # Update course slug in links
        content = content.replace(
            f"courses/{old_slug}/",
            f"courses/{new_slug}/"
        )
        
        # Optionally update course name if it appears
        if new_name:
            # Pattern for table rows: | CODE | Old Name | [Open](...) |
            # We need to be careful not to change unrelated text
            pass  # Name updates in term files require manual review
        
        if content != original:
            if not dry_run:
                md_file.write_text(content, encoding='utf-8')
            rel_path = md_file.relative_to(BASE_DIR)
            updated_files.append(str(rel_path))
    
    return updated_files


def update_other_course_files(old_slug, new_slug, dry_run=False):
    """Update any references in other course index files."""
    updated_files = []
    
    for course_dir in COURSES_DIR.iterdir():
        if not course_dir.is_dir():
            continue
        
        index_file = course_dir / "index.md"
        if not index_file.exists():
            continue
        
        try:
            content = index_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        if old_slug not in content:
            continue
        
        original = content
        content = content.replace(old_slug, new_slug)
        
        if content != original:
            if not dry_run:
                index_file.write_text(content, encoding='utf-8')
            rel_path = index_file.relative_to(BASE_DIR)
            updated_files.append(str(rel_path))
    
    return updated_files


def run_taken_at_update(dry_run=False):
    """Run the update_taken_at.py script."""
    if dry_run:
        return True, "Would run update_taken_at.py --force"
    
    import subprocess
    script_path = BASE_DIR / "scripts" / "update_taken_at.py"
    if script_path.exists():
        result = subprocess.run(
            [sys.executable, str(script_path), "--force"],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )
        return result.returncode == 0, "Ran update_taken_at.py --force"
    return False, "update_taken_at.py not found"


def main():
    parser = argparse.ArgumentParser(
        description="Rename a course and update all references",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 rename_course.py data-structure data-structures
    python3 rename_course.py ml machine-learning --name "Machine Learning"
    python3 rename_course.py old-course new-course --dry-run
        """
    )
    parser.add_argument("old_slug", help="Current course slug (folder name)")
    parser.add_argument("new_slug", help="New course slug (folder name)")
    parser.add_argument("--name", help="New course display name (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    
    args = parser.parse_args()
    
    old_slug = args.old_slug
    new_slug = args.new_slug
    new_name = args.name
    dry_run = args.dry_run
    
    # Validation
    old_dir = COURSES_DIR / old_slug
    if not old_dir.exists():
        print(f"\n❌ Error: Course '{old_slug}' not found!")
        print("\nAvailable courses:")
        for d in sorted(COURSES_DIR.iterdir()):
            if d.is_dir():
                print(f"  - {d.name}")
        sys.exit(1)
    
    if old_slug == new_slug and not new_name:
        print("\n❌ Error: Old and new slugs are the same, and no new name provided.")
        sys.exit(1)
    
    # Print header
    print_header("RENAME COURSE")
    print(f"\n  From: {old_slug}")
    print(f"  To:   {new_slug}")
    if new_name:
        print(f"  Name: {new_name}")
    if dry_run:
        print("\n  ⚠️  DRY RUN MODE - No changes will be made")
    
    # Confirmation
    if not dry_run:
        response = input("\nProceed? (yes/no): ").strip().lower()
        if response != "yes":
            print("Aborted.")
            sys.exit(0)
    
    # Step 1: Rename folder
    if old_slug != new_slug:
        print_step(1, "Renaming course folder")
        success, message = rename_course_folder(old_slug, new_slug, dry_run)
        if success:
            print(f"  ✅ {message}")
        else:
            print(f"  ❌ {message}")
            sys.exit(1)
    else:
        print_step(1, "Renaming course folder")
        print("  ⏭️  Slug unchanged, skipping folder rename")
    
    # Step 2: Update course's own index.md
    print_step(2, "Updating course index.md")
    success, message = update_course_index_file(new_slug, new_name, dry_run)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⏭️  {message}")
    
    # Step 3: Update courses/index.md
    print_step(3, "Updating courses/index.md")
    success, message = update_courses_index(old_slug, new_slug, new_name, dry_run)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⏭️  {message}")
    
    # Step 4: Update term files
    print_step(4, "Updating program term files")
    updated_files = update_term_files(old_slug, new_slug, new_name, dry_run)
    if updated_files:
        print(f"  ✅ Updated {len(updated_files)} files:")
        for f in updated_files[:10]:
            print(f"     - {f}")
        if len(updated_files) > 10:
            print(f"     ... and {len(updated_files) - 10} more")
    else:
        print("  ⏭️  No term files to update")
    
    # Step 5: Update other course files
    print_step(5, "Checking other course files")
    updated_courses = update_other_course_files(old_slug, new_slug, dry_run)
    if updated_courses:
        print(f"  ✅ Updated {len(updated_courses)} course files")
    else:
        print("  ⏭️  No other courses reference this course")
    
    # Step 6: Update Taken At sections
    print_step(6, "Updating 'Taken At' sections")
    success, message = run_taken_at_update(dry_run)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⚠️  {message}")
    
    # Summary
    print_header("RENAME COMPLETE" if not dry_run else "DRY RUN COMPLETE")
    
    if dry_run:
        print("\n  No changes were made. Run without --dry-run to apply changes.")
    else:
        print(f"\n  ✅ Course renamed: {old_slug} → {new_slug}")
        print(f"\n  Next steps:")
        print(f"    1. Review {new_slug}/index.md")
        print(f"    2. Run: mkdocs build  (to verify no errors)")
        print(f"    3. Commit your changes")


if __name__ == "__main__":
    main()
