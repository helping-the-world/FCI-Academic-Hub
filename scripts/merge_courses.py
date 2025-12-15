#!/usr/bin/env python3
"""
Script to merge two duplicate courses into one.

This script will:
1. Copy all files from the source course to the destination course
2. Update the courses index.md (remove source course entry)
3. Update all program term files (change links from source to destination)
4. Delete the source course folder

Usage:
    python3 merge_courses.py <source-course> <destination-course>
    python3 merge_courses.py <source-course> <destination-course> --dry-run

Examples:
    python3 merge_courses.py programming-principles fundamentals-of-programming
    python3 merge_courses.py digital-circuit digital-logic-design --dry-run
"""

import os
import re
import sys
import shutil
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
COURSES_DIR = BASE_DIR / "docs" / "materials" / "courses"
PROGRAMS_DIR = BASE_DIR / "docs" / "programs"
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


def copy_files(source_dir, dest_dir, dry_run=False):
    """Copy all files from source to destination, preserving structure."""
    copied = []
    skipped = []
    
    for root, dirs, files in os.walk(source_dir):
        # Calculate relative path from source
        rel_path = Path(root).relative_to(source_dir)
        dest_path = dest_dir / rel_path
        
        # Create destination directory
        if not dry_run and not dest_path.exists():
            dest_path.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # Skip index.md - we don't want to overwrite the destination's index
            if file == "index.md" and rel_path == Path("."):
                skipped.append(f"{rel_path / file} (index.md skipped)")
                continue
            
            src_file = Path(root) / file
            dst_file = dest_path / file
            
            if dst_file.exists():
                skipped.append(f"{rel_path / file} (already exists)")
            else:
                if not dry_run:
                    shutil.copy2(src_file, dst_file)
                copied.append(str(rel_path / file))
    
    return copied, skipped


def update_courses_index(source_slug, dry_run=False):
    """Remove the source course from courses/index.md."""
    if not COURSES_INDEX.exists():
        return False, "courses/index.md not found"
    
    content = COURSES_INDEX.read_text(encoding='utf-8')
    original_content = content
    
    # Remove table row with source course
    # Pattern matches: | CODE | Name | [Open](./source-slug/index.md) |
    pattern = rf'\| [A-Z]{{2,3}}[0-9]+ \| [^|]+ \| \[Open\]\(\.\/{re.escape(source_slug)}\/index\.md\) \|\n?'
    content = re.sub(pattern, '', content)
    
    # Also remove from category lists
    # Pattern matches: - [Course Name](./source-slug/index.md)
    pattern = rf'- \[[^\]]+\]\(\.\/{re.escape(source_slug)}\/index\.md\)\n?'
    content = re.sub(pattern, '', content)
    
    if content != original_content:
        if not dry_run:
            COURSES_INDEX.write_text(content, encoding='utf-8')
        return True, "Removed from courses index"
    else:
        return False, "Not found in courses index"


def update_term_files(source_slug, dest_slug, dry_run=False):
    """Update all program term files to use destination course instead of source."""
    updated_files = []
    
    for prog_dir in PROGRAMS_DIR.iterdir():
        if not prog_dir.is_dir():
            continue
        
        for year_dir in prog_dir.glob("year*"):
            if not year_dir.is_dir():
                continue
            
            for term_file in year_dir.glob("*.md"):
                try:
                    content = term_file.read_text(encoding='utf-8')
                except Exception:
                    continue
                
                if source_slug in content:
                    # Replace course slug in links
                    new_content = content.replace(
                        f"courses/{source_slug}/",
                        f"courses/{dest_slug}/"
                    )
                    
                    if new_content != content:
                        if not dry_run:
                            term_file.write_text(new_content, encoding='utf-8')
                        rel_path = term_file.relative_to(BASE_DIR)
                        updated_files.append(str(rel_path))
    
    return updated_files


def delete_source_folder(source_dir, dry_run=False):
    """Delete the source course folder."""
    if source_dir.exists():
        if not dry_run:
            shutil.rmtree(source_dir)
        return True
    return False


def run_taken_at_update(dry_run=False):
    """Run the update_taken_at.py script to refresh Taken At sections."""
    if dry_run:
        return True, "Would run update_taken_at.py --force"
    
    import subprocess
    script_path = BASE_DIR / "update_taken_at.py"
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
    """Main function to merge courses."""
    # Parse arguments
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nError: Please provide source and destination course slugs.")
        print("\nAvailable courses:")
        for course_dir in sorted(COURSES_DIR.iterdir()):
            if course_dir.is_dir():
                print(f"  - {course_dir.name}")
        sys.exit(1)
    
    source_slug = sys.argv[1]
    dest_slug = sys.argv[2]
    dry_run = "--dry-run" in sys.argv
    
    source_dir = COURSES_DIR / source_slug
    dest_dir = COURSES_DIR / dest_slug
    
    # Validate courses exist
    if not source_dir.exists():
        print(f"Error: Source course '{source_slug}' not found!")
        sys.exit(1)
    
    if not dest_dir.exists():
        print(f"Error: Destination course '{dest_slug}' not found!")
        sys.exit(1)
    
    if source_slug == dest_slug:
        print("Error: Source and destination cannot be the same!")
        sys.exit(1)
    
    # Print header
    print_header("MERGE COURSES")
    print(f"\n  Source:      {source_slug}")
    print(f"  Destination: {dest_slug}")
    if dry_run:
        print("\n  ⚠️  DRY RUN MODE - No changes will be made")
    
    # Confirmation
    if not dry_run:
        print(f"\n⚠️  This will DELETE '{source_slug}' after merging!")
        response = input("\nAre you sure? (yes/no): ").strip().lower()
        if response != "yes":
            print("Aborted.")
            sys.exit(0)
    
    # Step 1: Copy files
    print_step(1, "Copying files from source to destination")
    copied, skipped = copy_files(source_dir, dest_dir, dry_run)
    
    if copied:
        print(f"  ✅ Copied {len(copied)} files:")
        for f in copied[:10]:
            print(f"     - {f}")
        if len(copied) > 10:
            print(f"     ... and {len(copied) - 10} more")
    else:
        print("  ⚠️  No new files to copy")
    
    if skipped:
        print(f"  ⏭️  Skipped {len(skipped)} files:")
        for f in skipped[:5]:
            print(f"     - {f}")
        if len(skipped) > 5:
            print(f"     ... and {len(skipped) - 5} more")
    
    # Step 2: Update courses index
    print_step(2, "Updating courses/index.md")
    success, message = update_courses_index(source_slug, dry_run)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⚠️  {message}")
    
    # Step 3: Update term files
    print_step(3, "Updating program term files")
    updated_files = update_term_files(source_slug, dest_slug, dry_run)
    if updated_files:
        print(f"  ✅ Updated {len(updated_files)} term files:")
        for f in updated_files:
            print(f"     - {f}")
    else:
        print("  ⚠️  No term files referenced the source course")
    
    # Step 4: Delete source folder
    print_step(4, "Deleting source course folder")
    if delete_source_folder(source_dir, dry_run):
        print(f"  ✅ {'Would delete' if dry_run else 'Deleted'}: {source_slug}/")
    else:
        print(f"  ⚠️  Source folder not found")
    
    # Step 5: Update Taken At sections
    print_step(5, "Updating 'Taken At' sections in all courses")
    success, message = run_taken_at_update(dry_run)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⚠️  {message}")
    
    # Summary
    print_header("MERGE COMPLETE" if not dry_run else "DRY RUN COMPLETE")
    
    if dry_run:
        print("\n  No changes were made. Run without --dry-run to apply changes.")
    else:
        print(f"\n  ✅ '{source_slug}' has been merged into '{dest_slug}'")
        print(f"\n  Next steps:")
        print(f"    1. Review {dest_slug}/index.md and update if needed")
        print(f"    2. Run: mkdocs build  (to verify no errors)")
        print(f"    3. Commit your changes")


if __name__ == "__main__":
    main()
