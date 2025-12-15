#!/usr/bin/env python3
"""
Script to update the 'Taken At' section in all course index.md files
based on which program term files reference each course.

Usage:
    python3 update_taken_at.py           # Update only if changed
    python3 update_taken_at.py --force   # Force update all files
    python3 update_taken_at.py --list    # List courses not in curriculum
"""

import os
import re
import sys
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
COURSES_DIR = BASE_DIR / "docs" / "materials" / "courses"
PROGRAMS_DIR = BASE_DIR / "docs" / "programs"

# Program display names
PROGRAMS = {
    "general-hours": "General Hours",
    "ai": "AI",
    "cyber-security": "Cyber Security",
    "software-engineering": "Software Engineering"
}

# Term display names
TERM_NAMES = {
    "term1": "Term 1",
    "term2": "Term 2",
    "elective1": "Elective 1",
    "elective2": "Elective 2"
}


def find_course_terms(course_slug):
    """Find all program terms where a course appears."""
    terms = []
    
    for prog_slug, prog_name in PROGRAMS.items():
        prog_dir = PROGRAMS_DIR / prog_slug
        if not prog_dir.exists():
            continue
        
        for year_dir in sorted(prog_dir.glob("year*")):
            if not year_dir.is_dir():
                continue
            
            year_num = year_dir.name.replace("year", "")
            
            for term_file in sorted(year_dir.glob("year*.md")):
                # Skip index files
                if term_file.name == "index.md":
                    continue
                
                try:
                    content = term_file.read_text(encoding='utf-8')
                except Exception as e:
                    print(f"  Warning: Could not read {term_file}: {e}")
                    continue
                
                # Check if course slug appears in the file
                if course_slug in content:
                    term_name = term_file.stem  # e.g. "year1-term1"
                    # Extract term type (term1, term2, elective1, etc.)
                    term_type = term_name.replace(f"year{year_num}-", "")
                    term_display = TERM_NAMES.get(term_type, term_type.title())
                    
                    terms.append({
                        "program": prog_name,
                        "year": f"Year {year_num}",
                        "term": term_display,
                        "link": f"../../../programs/{prog_slug}/{year_dir.name}/{term_name}.md"
                    })
    
    return terms


def build_taken_at_section(terms):
    """Build the Taken At markdown section."""
    if terms:
        rows = "\n".join([
            f"| {t['program']} | {t['year']} | {t['term']} | [View Term]({t['link']}) |"
            for t in terms
        ])
    else:
        rows = "| - | - | - | - |"
    
    return f"""## 📅 Taken At

| Program | Year | Term | Link |
|---------|------|------|------|
{rows}

---"""


def update_course_file(course_slug):
    """Update a course file with the correct Taken At section."""
    index_file = COURSES_DIR / course_slug / "index.md"
    
    if not index_file.exists():
        return False, "No index.md"
    
    try:
        content = index_file.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Read error: {e}"
    
    # Find terms for this course
    terms = find_course_terms(course_slug)
    
    # Build new Taken At section
    new_taken_at = build_taken_at_section(terms)
    
    # Pattern to match the existing Taken At section
    # Matches from "## 📅 Taken At" to the next "---" after the table
    pattern = r'## 📅 Taken At\s*\n\s*\|[^\n]*\n\|[-|\s]*\n(?:\|[^\n]*\n)*\s*---'
    
    if re.search(pattern, content):
        # Replace existing section
        new_content = re.sub(pattern, new_taken_at, content)
        
        if new_content != content:
            index_file.write_text(new_content, encoding='utf-8')
            return True, f"{len(terms)} terms"
        else:
            return False, "No change needed"
    else:
        return False, "No Taken At section found"


def main():
    """Main function to update all course files."""
    force = "--force" in sys.argv
    list_only = "--list" in sys.argv
    
    print("=" * 60)
    print("Updating 'Taken At' sections in course files")
    if force:
        print("(Force mode: re-writing all files)")
    print("=" * 60)
    print()
    
    updated = 0
    skipped = 0
    errors = 0
    not_in_curriculum = []
    
    # Process all course directories
    for course_dir in sorted(COURSES_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        
        course_slug = course_dir.name
        
        # Skip if it's a file not a directory
        if course_slug.endswith('.md'):
            continue
        
        # Check if course is in any term file
        terms = find_course_terms(course_slug)
        
        if list_only:
            if not terms:
                not_in_curriculum.append(course_slug)
            continue
        
        # Force mode: always update
        if force:
            index_file = COURSES_DIR / course_slug / "index.md"
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                new_taken_at = build_taken_at_section(terms)
                pattern = r'## 📅 Taken At\s*\n\s*\|[^\n]*\n\|[-|\s]*\n(?:\|[^\n]*\n)*\s*---'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, new_taken_at, content)
                    index_file.write_text(new_content, encoding='utf-8')
                    print(f"  ✅ {course_slug}: Updated ({len(terms)} terms)")
                    updated += 1
                    if not terms:
                        not_in_curriculum.append(course_slug)
                    continue
        
        success, message = update_course_file(course_slug)
        
        if success:
            print(f"  ✅ {course_slug}: Updated ({message})")
            updated += 1
        elif "No change" in message:
            if not terms:
                not_in_curriculum.append(course_slug)
            print(f"  ⏭️  {course_slug}: {message}")
            skipped += 1
        else:
            print(f"  ⚠️  {course_slug}: {message}")
            errors += 1
    
    if not list_only:
        print()
        print("=" * 60)
        print(f"Summary: {updated} updated, {skipped} skipped, {errors} errors")
        print("=" * 60)
    
    if not_in_curriculum:
        print()
        print("⚠️  Courses NOT in any program term file (need to be added):")
        for course in not_in_curriculum:
            print(f"   - {course}")
        print()
        print("To add these courses to a term, edit the appropriate file in:")
        print("   docs/programs/<program>/year<N>/year<N>-term<N>.md")


if __name__ == "__main__":
    main()
