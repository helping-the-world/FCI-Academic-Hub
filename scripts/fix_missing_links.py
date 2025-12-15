#!/usr/bin/env python3
"""
Script to batch fix all missing course links in term files.

This script will:
1. Scan all term files in docs/programs/
2. Find rows with missing links
3. Try to match course codes to existing course folders
4. Update all links automatically

Usage:
    python3 fix_missing_links.py           # Preview changes
    python3 fix_missing_links.py --apply   # Apply changes
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

# Known course code to slug mappings
# This helps match courses when the name doesn't exactly match the folder
COURSE_MAPPINGS = {
    # Year 2
    "BSD227": "ordinary-differential-equations",
    "BSD228": "advanced-math",
    "BSD229": "advanced-math-2",  # Different from BSD228!
    "BSD232": "physics",
    "CSD230": "analysis-of-algorithms",
    "ISD229": "electronic-business",
    "BSD233": "numerical-analysis",
    
    # Year 3 CS
    "CSD331": "artificial-intelligence",
    "CSD332": "computer-architecture",
    "CSD333": "operating-systems",
    "CSD334": "digital-image-processing",
    "CSD335": "assembly-language",
    "CSD336": "compiler-design",
    "CSD337": "computer-graphics",
    "CSD341": "software-engineering",
    "CSD340": "simulation-and-modeling",
    
    # Year 3 IS
    "ISD331": "information-retrieval-systems",
    "CSD339": "mobile-computing",
    "ISD333": "decision-support-systems",
    "ISD338": "big-data-analysis",
    "ISD336": "advanced-database-systems",
    "ISD337": "information-security",
    
    # Year 4
    "ISD471": "data-mining",
    "CSC309": "computer-graphics",
    "CSC310": "advanced-database-systems",
    
    # Existing courses that might be referenced
    "BSD101": "calculus",
    "BSD102": "linear-algebra",
    "BSD103": "discrete-mathematics",
    "BSD104": "statistics-and-probabilities",
    "CSD101": "fundamentals-of-programming",
    "CSD102": "object-oriented-programming",
    "CSD103": "data-structures",
    "CSD104": "digital-logic-design",
    "ISD101": "fundamentals-of-information-systems",
    "ISD102": "introduction-to-database-system",
    "ISD103": "introduction-to-computer-networks",
    "ISD104": "web-pages-programming",
    "CSD105": "basics-of-computer-science",
    "UNI101": "technical-writing",
}


def get_existing_courses():
    """Get list of existing course folders."""
    courses = {}
    for d in COURSES_DIR.iterdir():
        if d.is_dir():
            courses[d.name] = d
    return courses


def name_to_slug(name):
    """Convert course name to potential slug."""
    # Common transformations
    name = name.lower().strip()
    name = re.sub(r'\s*\([^)]*\)\s*', '', name)  # Remove parentheses
    name = re.sub(r'[^a-z0-9\s-]', '', name)  # Keep only letters, numbers, spaces, hyphens
    name = re.sub(r'\s+', '-', name)  # Replace spaces with hyphens
    name = re.sub(r'-+', '-', name)  # Remove duplicate hyphens
    name = name.strip('-')
    return name


def find_best_match(code, name, existing_courses):
    """Find best matching course folder for a course code/name."""
    # Check direct mapping first
    if code in COURSE_MAPPINGS:
        slug = COURSE_MAPPINGS[code]
        if slug in existing_courses:
            return slug
    
    # Try converting name to slug
    slug = name_to_slug(name)
    if slug in existing_courses:
        return slug
    
    # Try partial matches
    for course_slug in existing_courses:
        if slug in course_slug or course_slug in slug:
            return course_slug
    
    return None


def scan_for_missing_links():
    """Scan all term files and find missing links."""
    missing_links = []
    existing_courses = get_existing_courses()
    
    for md_file in PROGRAMS_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # Skip non-term files
        if "year" not in md_file.name:
            continue
        
        # Pattern to match table rows with empty last column
        # Format: | CODE | Name |  |
        pattern = r'\| ([A-Z]{2,3}\d{3}) \| ([^|]+) \|\s*\|'
        
        for match in re.finditer(pattern, content):
            code = match.group(1).strip()
            name = match.group(2).strip()
            
            slug = find_best_match(code, name, existing_courses)
            
            missing_links.append({
                "file": md_file,
                "code": code,
                "name": name,
                "slug": slug,
                "exists": slug is not None
            })
    
    return missing_links


def fix_links(missing_links, apply=False):
    """Fix all missing links that have matching course folders."""
    files_to_update = {}
    
    for link in missing_links:
        if not link["exists"]:
            continue
        
        file_path = link["file"]
        if file_path not in files_to_update:
            files_to_update[file_path] = file_path.read_text(encoding='utf-8')
        
        code = link["code"]
        name = link["name"]
        slug = link["slug"]
        
        # Pattern to match this specific row
        pattern = rf'\| {re.escape(code)} \| {re.escape(name)} \|\s*\|'
        replacement = f"| {code} | {name} | [Open](../../../materials/courses/{slug}/index.md) |"
        
        files_to_update[file_path] = re.sub(
            pattern, replacement, files_to_update[file_path]
        )
    
    if apply:
        for file_path, content in files_to_update.items():
            file_path.write_text(content, encoding='utf-8')
    
    return files_to_update


def main():
    parser = argparse.ArgumentParser(
        description="Fix all missing course links in term files"
    )
    parser.add_argument("--apply", action="store_true", 
                        help="Apply changes (default is preview only)")
    
    args = parser.parse_args()
    
    print()
    print("=" * 70)
    print("  FIX MISSING COURSE LINKS")
    print("=" * 70)
    
    if not args.apply:
        print("\n  ⚠️  PREVIEW MODE - No changes will be made")
        print("      Run with --apply to make changes\n")
    
    # Scan for missing links
    print("\n[Scanning term files for missing links...]")
    print("-" * 70)
    
    missing_links = scan_for_missing_links()
    
    can_fix = [l for l in missing_links if l["exists"]]
    cannot_fix = [l for l in missing_links if not l["exists"]]
    
    print(f"\n  Found {len(missing_links)} missing links:")
    print(f"    ✅ Can fix: {len(can_fix)}")
    print(f"    ❌ Cannot fix (no matching folder): {len(cannot_fix)}")
    
    # Show links that can be fixed
    if can_fix:
        print("\n\n[Links that will be fixed]")
        print("-" * 70)
        
        by_file = {}
        for link in can_fix:
            rel_path = str(link["file"].relative_to(BASE_DIR))
            if rel_path not in by_file:
                by_file[rel_path] = []
            by_file[rel_path].append(link)
        
        for file_path, links in sorted(by_file.items()):
            print(f"\n  📁 {file_path}")
            for link in links:
                print(f"      {link['code']} -> {link['slug']}/")
    
    # Show links that cannot be fixed
    if cannot_fix:
        print("\n\n[Links that CANNOT be fixed (course folder missing)]")
        print("-" * 70)
        
        seen = set()
        for link in cannot_fix:
            key = f"{link['code']}:{link['name']}"
            if key in seen:
                continue
            seen.add(key)
            print(f"    ❌ {link['code']} - {link['name']}")
        
        print("\n  💡 Create these courses with:")
        print("     python3 scripts/create_course.py --code CODE --slug name-slug")
    
    # Apply fixes
    if can_fix:
        files_updated = fix_links(can_fix, apply=args.apply)
        
        print("\n")
        print("=" * 70)
        if args.apply:
            print(f"  ✅ DONE - Updated {len(files_updated)} files")
            print("\n  Run: python3 scripts/update_taken_at.py --force")
            print("       to update 'Taken At' sections in courses.")
        else:
            print(f"  PREVIEW COMPLETE - Would update {len(files_updated)} files")
            print("\n  Run with --apply to make changes:")
            print("       python3 scripts/fix_missing_links.py --apply")
        print("=" * 70)
    else:
        print("\n")
        print("=" * 70)
        print("  No links can be automatically fixed.")
        print("=" * 70)


if __name__ == "__main__":
    main()
