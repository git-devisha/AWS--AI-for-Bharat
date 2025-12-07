#!/usr/bin/env python3
"""
File Organizer - "I hate manually sorting my Downloads folder, so I built this."

Automatically organizes files into categorized folders based on file type.
Handles duplicates and keeps your directories clean.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import argparse
from datetime import datetime


# File type categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.heic'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.yaml', '.yml'],
    'Executables': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
    'Other': []
}


def get_category(file_extension):
    """Determine the category for a file based on its extension."""
    file_extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return 'Other'


def get_unique_filename(destination_path):
    """Generate a unique filename if a file already exists."""
    if not destination_path.exists():
        return destination_path
    
    base = destination_path.stem
    extension = destination_path.suffix
    parent = destination_path.parent
    counter = 1
    
    while True:
        new_name = f"{base}_{counter}{extension}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def organize_files(source_dir, dry_run=False, verbose=False):
    """
    Organize files in the source directory into categorized folders.
    
    Args:
        source_dir: Path to the directory to organize
        dry_run: If True, only show what would be done without moving files
        verbose: If True, print detailed information
    """
    source_path = Path(source_dir).resolve()
    
    if not source_path.exists():
        print(f"❌ Error: Directory '{source_dir}' does not exist.")
        return
    
    if not source_path.is_dir():
        print(f"❌ Error: '{source_dir}' is not a directory.")
        return
    
    # Statistics
    stats = defaultdict(int)
    files_moved = []
    
    print(f"\n{'🔍 DRY RUN - ' if dry_run else ''}Organizing files in: {source_path}\n")
    
    # Get all files (excluding directories and hidden files)
    files = [f for f in source_path.iterdir() if f.is_file() and not f.name.startswith('.')]
    
    if not files:
        print("✨ No files to organize!")
        return
    
    for file_path in files:
        # Skip the script itself
        if file_path.name == Path(__file__).name:
            continue
        
        # Determine category
        extension = file_path.suffix
        category = get_category(extension)
        
        # Create category folder
        category_folder = source_path / category
        if not dry_run and not category_folder.exists():
            category_folder.mkdir(exist_ok=True)
        
        # Determine destination
        destination = category_folder / file_path.name
        
        # Handle duplicates
        if destination.exists():
            destination = get_unique_filename(destination)
        
        # Move or simulate move
        try:
            if not dry_run:
                shutil.move(str(file_path), str(destination))
            
            stats[category] += 1
            files_moved.append((file_path.name, category))
            
            if verbose:
                print(f"  {'[DRY RUN] ' if dry_run else ''}📁 {file_path.name} → {category}/")
        
        except Exception as e:
            print(f"  ❌ Error moving {file_path.name}: {e}")
    
    # Print summary
    print(f"\n{'=' * 50}")
    print(f"{'DRY RUN ' if dry_run else ''}Summary:")
    print(f"{'=' * 50}")
    
    total_files = sum(stats.values())
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} file{'s' if count != 1 else ''}")
    
    print(f"\n✅ Total: {total_files} file{'s' if total_files != 1 else ''} {'would be ' if dry_run else ''}organized")
    
    if dry_run:
        print("\n💡 Run without --dry-run to actually move the files.")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files into categorized folders automatically.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_organizer.py ~/Downloads
  python file_organizer.py ~/Desktop --dry-run
  python file_organizer.py . --verbose
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to organize (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually moving files'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed information about each file'
    )
    
    args = parser.parse_args()
    
    organize_files(args.directory, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == '__main__':
    main()
