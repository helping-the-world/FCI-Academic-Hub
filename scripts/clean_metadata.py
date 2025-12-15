#!/usr/bin/env python3
"""
Clean metadata from files before contributing.

This script removes identifying metadata from:
- PDF files (author, creator, producer, timestamps)
- Images (EXIF data, GPS, camera info)
- Office documents (author, company, revision history)

Usage:
    python3 clean_metadata.py <file1> [file2] ...
    python3 clean_metadata.py *.pdf
    python3 clean_metadata.py --all docs/materials/courses/

Requirements:
    - exiftool: sudo apt install libimage-exiftool-perl
               brew install exiftool (macOS)
    - ghostscript (optional, for corrupted PDFs): sudo apt install ghostscript
    - zip (for Office documents): usually pre-installed
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF Document',
    '.jpg': 'JPEG Image',
    '.jpeg': 'JPEG Image',
    '.png': 'PNG Image',
    '.gif': 'GIF Image',
    '.webp': 'WebP Image',
    '.tiff': 'TIFF Image',
    '.bmp': 'BMP Image',
    '.docx': 'Word Document',
    '.xlsx': 'Excel Spreadsheet',
    '.pptx': 'PowerPoint Presentation',
    '.doc': 'Word Document (Legacy)',
    '.xls': 'Excel Spreadsheet (Legacy)',
    '.ppt': 'PowerPoint (Legacy)',
}


def check_exiftool():
    """Check if exiftool is installed."""
    if shutil.which('exiftool') is None:
        print("❌ exiftool is not installed!")
        print()
        print("Install it with:")
        print("  Linux (Debian/Ubuntu): sudo apt install libimage-exiftool-perl")
        print("  Linux (Fedora):        sudo dnf install perl-Image-ExifTool")
        print("  macOS:                 brew install exiftool")
        print("  Windows:               Download from https://exiftool.org/")
        return False
    return True


def check_ghostscript():
    """Check if ghostscript is installed."""
    return shutil.which('gs') is not None


def get_metadata(filepath):
    """Get current metadata from file."""
    try:
        result = subprocess.run(
            ['exiftool', str(filepath)],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error reading metadata: {e}"


def clean_pdf_with_ghostscript(filepath):
    """Clean PDF using Ghostscript (handles corrupted files)."""
    path = Path(filepath)
    temp_output = path.parent / f".tmp_{path.name}"
    
    try:
        result = subprocess.run([
            'gs',
            '-dNOPAUSE',
            '-dBATCH',
            '-dQUIET',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/prepress',
            f'-sOutputFile={temp_output}',
            str(path)
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and temp_output.exists():
            # Replace original with cleaned version
            temp_output.replace(path)
            return True
        else:
            if temp_output.exists():
                temp_output.unlink()
            return False
    except Exception as e:
        if temp_output.exists():
            temp_output.unlink()
        return False


def clean_office_document(filepath):
    """Clean metadata from Office documents (docx, xlsx, pptx) using ZIP manipulation."""
    path = Path(filepath)
    ext = path.suffix.lower()
    
    if ext not in ['.docx', '.xlsx', '.pptx']:
        return False
    
    # Office documents are ZIP files with XML inside
    temp_dir = tempfile.mkdtemp()
    temp_output = Path(temp_dir) / path.name
    
    try:
        # Extract the document
        with zipfile.ZipFile(path, 'r') as zip_in:
            zip_in.extractall(temp_dir)
        
        # Files that contain metadata
        metadata_files = [
            'docProps/core.xml',
            'docProps/app.xml',
            'docProps/custom.xml',
        ]
        
        # Clean or remove metadata files
        for meta_file in metadata_files:
            meta_path = Path(temp_dir) / meta_file
            if meta_path.exists():
                if meta_file == 'docProps/core.xml':
                    # Clean core.xml - remove identifying info but keep structure
                    clean_core_xml(meta_path)
                elif meta_file == 'docProps/app.xml':
                    # Clean app.xml - remove app-specific info
                    clean_app_xml(meta_path)
                else:
                    # Remove custom.xml entirely
                    meta_path.unlink()
        
        # Repack the document
        with zipfile.ZipFile(temp_output, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    if str(arcname) != path.name:  # Don't include the output file
                        zip_out.write(file_path, arcname)
        
        # Replace original
        shutil.copy2(temp_output, path)
        return True
        
    except Exception as e:
        print(f"      Error: {e}")
        return False
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def clean_core_xml(filepath):
    """Clean core.xml metadata file."""
    try:
        # Define namespaces
        namespaces = {
            'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'dcterms': 'http://purl.org/dc/terms/',
            'dcmitype': 'http://purl.org/dc/dcmitype/',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }
        
        # Register namespaces
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix, uri)
        
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Fields to clear (keep tags but empty content)
        fields_to_clear = [
            '{http://purl.org/dc/elements/1.1/}creator',
            '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy',
            '{http://purl.org/dc/elements/1.1/}title',
            '{http://purl.org/dc/elements/1.1/}subject',
            '{http://purl.org/dc/elements/1.1/}description',
            '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}keywords',
            '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}category',
        ]
        
        for field in fields_to_clear:
            elem = root.find(field)
            if elem is not None:
                elem.text = ''
        
        tree.write(filepath, xml_declaration=True, encoding='UTF-8')
        return True
    except Exception:
        return False


def clean_app_xml(filepath):
    """Clean app.xml metadata file."""
    try:
        # Define namespace
        ns = {'ep': 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
        ET.register_namespace('', ns['ep'])
        
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Fields to clear
        fields_to_clear = ['Application', 'Company', 'Manager', 'AppVersion']
        
        for field in fields_to_clear:
            elem = root.find(f'{{{ns["ep"]}}}{field}')
            if elem is not None:
                elem.text = ''
        
        tree.write(filepath, xml_declaration=True, encoding='UTF-8')
        return True
    except Exception:
        return False


def clean_file(filepath, verbose=False):
    """Remove metadata from a file."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return False
    
    ext = path.suffix.lower()
    
    if ext not in SUPPORTED_EXTENSIONS:
        print(f"⚠️  Unsupported format: {ext} ({filepath})")
        return False
    
    if verbose:
        print(f"\n📄 Processing: {filepath}")
        print(f"   Type: {SUPPORTED_EXTENSIONS[ext]}")
    
    # Handle Office documents with ZIP method
    if ext in ['.docx', '.xlsx', '.pptx']:
        if clean_office_document(filepath):
            print(f"✅ Cleaned: {filepath}")
            return True
        else:
            print(f"❌ Failed to clean Office document: {filepath}")
            return False
    
    # Handle legacy Office formats (doc, xls, ppt)
    if ext in ['.doc', '.xls', '.ppt']:
        print(f"⚠️  Legacy Office format not supported: {filepath}")
        print(f"      💡 Convert to {ext}x format first (e.g., .doc → .docx)")
        return False
    
    # Try exiftool first for PDFs and images
    try:
        result = subprocess.run(
            ['exiftool', '-all=', '-overwrite_original', str(path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Cleaned: {filepath}")
            return True
        
        # If exiftool fails on PDF, try Ghostscript
        if ext == '.pdf':
            if 'Format error' in result.stderr or 'Error' in result.stderr:
                if check_ghostscript():
                    print(f"⚠️  Exiftool failed, trying Ghostscript: {filepath}")
                    if clean_pdf_with_ghostscript(filepath):
                        print(f"✅ Cleaned (via Ghostscript): {filepath}")
                        return True
                    else:
                        print(f"❌ Ghostscript also failed: {filepath}")
                        return False
                else:
                    print(f"❌ Error: {result.stderr.strip()}")
                    print(f"      💡 Install ghostscript for corrupted PDFs:")
                    print(f"         sudo dnf install ghostscript  # Fedora")
                    print(f"         sudo apt install ghostscript  # Ubuntu")
                    return False
        
        print(f"❌ Error: {result.stderr.strip()}")
        return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error cleaning {filepath}: {e}")
        return False


def find_files(directory, recursive=True):
    """Find all supported files in a directory."""
    path = Path(directory)
    files = []
    
    if recursive:
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(path.rglob(f"*{ext}"))
    else:
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(path.glob(f"*{ext}"))
    
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Clean metadata from files for anonymous contribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 clean_metadata.py document.pdf
    python3 clean_metadata.py *.pdf
    python3 clean_metadata.py --all docs/materials/courses/
    python3 clean_metadata.py --info document.pdf
    
Supported Formats:
    PDF, JPEG, PNG, GIF, WebP, TIFF, BMP
    DOCX, XLSX, PPTX, DOC, XLS, PPT
        """
    )
    
    parser.add_argument('files', nargs='*', help='Files to clean')
    parser.add_argument('--all', '-a', metavar='DIR', 
                        help='Clean all supported files in directory')
    parser.add_argument('--info', '-i', metavar='FILE',
                        help='Show metadata of a file (without cleaning)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be cleaned without making changes')
    
    args = parser.parse_args()
    
    # Check exiftool installation
    if not check_exiftool():
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("  METADATA CLEANER - Anonymous Contribution Tool")
    print("=" * 60)
    
    # Show file info
    if args.info:
        print(f"\n📄 Metadata for: {args.info}")
        print("-" * 60)
        print(get_metadata(args.info))
        sys.exit(0)
    
    # Collect files to process
    files_to_clean = []
    
    if args.all:
        print(f"\n🔍 Scanning directory: {args.all}")
        files_to_clean = find_files(args.all)
        print(f"   Found {len(files_to_clean)} files")
    elif args.files:
        files_to_clean = [Path(f) for f in args.files if Path(f).exists()]
    else:
        parser.print_help()
        sys.exit(1)
    
    if not files_to_clean:
        print("\n⚠️  No files to clean!")
        sys.exit(0)
    
    # Dry run
    if args.dry_run:
        print("\n📋 Files that would be cleaned (dry run):")
        print("-" * 60)
        for f in files_to_clean:
            ext = f.suffix.lower()
            print(f"   {f} ({SUPPORTED_EXTENSIONS.get(ext, 'Unknown')})")
        print(f"\n   Total: {len(files_to_clean)} files")
        print("\n   Run without --dry-run to clean files.")
        sys.exit(0)
    
    # Clean files
    print("\n🧹 Cleaning metadata...")
    print("-" * 60)
    
    success = 0
    failed = 0
    
    for filepath in files_to_clean:
        if clean_file(filepath, verbose=args.verbose):
            success += 1
        else:
            failed += 1
    
    # Summary
    print()
    print("=" * 60)
    print(f"  ✅ Cleaned: {success}")
    print(f"  ❌ Failed:  {failed}")
    print("=" * 60)
    
    if success > 0:
        print("\n💡 Verify with: exiftool <filename>")
        print("   Metadata should now be minimal/empty.")


if __name__ == "__main__":
    main()
