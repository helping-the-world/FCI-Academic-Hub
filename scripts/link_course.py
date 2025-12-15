#!/usr/bin/env python3
"""
Script to link a course in program term files.

This script will:
1. Find all term files that mention the course code
2. Add/update the course link to point to the correct course folder

Usage:
    python3 link_course.py <course-code> <course-slug>
    python3 link_course.py <course-code> <course-slug> --dry-run

Examples:
    python3 link_course.py BSD227 ordinary-differential-equations
    python3 link_course.py CSD230 analysis-of-algorithms --dry-run
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
COURSES_DIR = DOCS_DIR / "materials" / "courses"
PROGRAMS_DIR = DOCS_DIR / "programs"


def find_and_update_term_files(course_code, course_slug, dry_run=False):
    """Find term files with course code and update links."""
    updated_files = []
    
    # The link format in term files
    course_link = f"[Open](../../../materials/courses/{course_slug}/index.md)"
    
    for md_file in PROGRAMS_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # Skip if course code not in file
        if course_code not in content:
            continue
        
        original = content
        
        # Pattern to match table row with course code
        # Matches: | CODE | Name | anything |
        # We want to replace the last column with our link
        pattern = rf'\| {re.escape(course_code)} \| ([^|]+) \|([^|]*)\|'
        
        def replace_link(match):
            name = match.group(1).strip()
            return f"| {course_code} | {name} | {course_link} |"
        
        content = re.sub(pattern, replace_link, content)
        
        if content != original:
            if not dry_run:
                md_file.write_text(content, encoding='utf-8')
            rel_path = md_file.relative_to(BASE_DIR)
            updated_files.append(str(rel_path))
    
    return updated_files


def verify_course_exists(course_slug):
    """Check if the course folder exists."""
    course_dir = COURSES_DIR / course_slug
    return course_dir.exists()


def main():
    parser = argparse.ArgumentParser(
        description="Link a course code to its course folder in term files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 link_course.py BSD227 ordinary-differential-equations
    python3 link_course.py CSD230 analysis-of-algorithms --dry-run
    
Course Codes Format:
    BSD### - Basic Science Department
    CSD### - Computer Science Department  
    ISD### - Information Systems Department
    SEN### - Software Engineering
    CSC### - Computer Science Core
    UNI### - University Requirements
        """
    )
    parser.add_argument("course_code", help="Course code (e.g., BSD227, CSD230)")
    parser.add_argument("course_slug", help="Course folder name (e.g., ordinary-differential-equations)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    
    args = parser.parse_args()
    
    course_code = args.course_code.upper()
    course_slug = args.course_slug.lower()
    dry_run = args.dry_run
    
    print()
    print("=" * 60)
    print("  LINK COURSE")
    print("=" * 60)
    print(f"\n  Code: {course_code}")
    print(f"  Slug: {course_slug}")
    if dry_run:
        print("\n  ⚠️  DRY RUN MODE - No changes will be made")
    
    # Verify course folder exists
    if not verify_course_exists(course_slug):
        print(f"\n⚠️  Warning: Course folder '{course_slug}' does not exist!")
        print(f"   Available courses:")
        for d in sorted(COURSES_DIR.iterdir())[:10]:
            if d.is_dir():
                print(f"     - {d.name}")
        print("     ...")
        
        if not dry_run:
            response = input("\nContinue anyway? (yes/no): ").strip().lower()
            if response != "yes":
                print("Aborted.")
                sys.exit(0)
    else:
        print(f"\n  ✅ Course folder exists: {course_slug}/")
    
    # Find and update term files
    print(f"\n[Updating term files]")
    print("-" * 50)
    
    updated_files = find_and_update_term_files(course_code, course_slug, dry_run)
    
    if updated_files:
        print(f"  ✅ {'Would update' if dry_run else 'Updated'} {len(updated_files)} files:")
        for f in updated_files:
            print(f"     - {f}")
    else:
        print(f"  ⚠️  No term files found with course code {course_code}")
    
    # Summary
    print()
    print("=" * 60)
    print("  DONE" if not dry_run else "  DRY RUN COMPLETE")
    print("=" * 60)
    
    if dry_run:
        print("\n  Run without --dry-run to apply changes.")
    elif updated_files:
        print(f"\n  Run: python3 scripts/update_taken_at.py --force")
        print(f"       to update 'Taken At' sections in courses.")


if __name__ == "__main__":
    main()
