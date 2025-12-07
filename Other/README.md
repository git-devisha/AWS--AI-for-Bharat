# File Organizer 🗂️

**"I hate manually sorting my Downloads folder, so I built this."**

A Python script that automatically organizes messy directories by sorting files into categorized folders based on file type.

## Features

- 📁 Automatically categorizes files (Images, Documents, Videos, Audio, Code, etc.)
- 🔄 Handles duplicate filenames intelligently
- 🔍 Dry-run mode to preview changes before applying
- 📊 Summary statistics after organizing
- 🎯 Works on any directory (Downloads, Desktop, etc.)

## Usage

### Basic Usage

Organize the current directory:
```bash
python file_organizer.py
```

Organize a specific directory:
```bash
python file_organizer.py ~/Downloads
python file_organizer.py C:\Users\YourName\Desktop
```

### Preview Changes (Dry Run)

See what would happen without actually moving files:
```bash
python file_organizer.py ~/Downloads --dry-run
```

### Verbose Output

Get detailed information about each file being moved:
```bash
python file_organizer.py ~/Downloads --verbose
```

## File Categories

The script organizes files into these categories:

- **Images**: jpg, png, gif, svg, webp, etc.
- **Documents**: pdf, docx, txt, xlsx, pptx, csv, etc.
- **Videos**: mp4, avi, mkv, mov, etc.
- **Audio**: mp3, wav, flac, aac, etc.
- **Archives**: zip, rar, 7z, tar, gz, etc.
- **Code**: py, js, html, css, json, etc.
- **Executables**: exe, msi, dmg, app, etc.
- **Other**: Everything else

## Example

Before:
```
Downloads/
├── vacation.jpg
├── report.pdf
├── song.mp3
├── video.mp4
├── script.py
└── archive.zip
```

After running `python file_organizer.py ~/Downloads`:
```
Downloads/
├── Images/
│   └── vacation.jpg
├── Documents/
│   └── report.pdf
├── Audio/
│   └── song.mp3
├── Videos/
│   └── video.mp4
├── Code/
│   └── script.py
└── Archives/
    └── archive.zip
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Safety Features

- Skips hidden files (starting with `.`)
- Skips the script itself
- Handles duplicate filenames by adding numbers
- Dry-run mode for safe testing

## Tips

1. Always run with `--dry-run` first to preview changes
2. Use on Downloads folder regularly to keep it clean
3. Customize `FILE_CATEGORIES` in the script for your needs
4. Set up a scheduled task/cron job to run automatically
