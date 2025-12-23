#!/usr/bin/env python3
"""
Remove Wakatime statistics from all calendar files
"""

import re
from pathlib import Path

def remove_wakatime_from_file(file_path: Path) -> bool:
    """Remove Wakatime references from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Process line by line to handle tables properly
        lines = content.split('\n')
        cleaned_lines = []
        expected_columns = None  # Track expected number of columns in current table
        
        for i, line in enumerate(lines):
            # Check if this is a table row
            if '|' in line and line.strip().startswith('|'):
                # Split by | and clean parts
                parts = [p.strip() for p in line.split('|')]
                # Remove empty strings from split (they appear at start/end)
                parts = [p for p in parts if p]
                
                # Check if this is a header row with Wakatime
                if len(parts) >= 3 and ('Wakatime' in line or (len(parts) == 3 and 'Metric' in parts[0] and 'GitHub' in parts[1])):
                    # Remove Wakatime column (third column)
                    new_line = f"| {parts[0]} | {parts[1]} |"
                    cleaned_lines.append(new_line)
                    expected_columns = 2
                    continue
                
                # Check if this is a separator row
                if len(parts) >= 2 and all(re.match(r'^[-:]+$', p) for p in parts):
                    # If previous line was a 2-column header, make this 2-column separator
                    if expected_columns == 2:
                        new_line = f"|--------|--------|"
                        cleaned_lines.append(new_line)
                        continue
                    # Otherwise, if it's a 3-column separator after a 2-column header, fix it
                    elif len(parts) == 3 and expected_columns == 2:
                        new_line = f"|--------|--------|"
                        cleaned_lines.append(new_line)
                        continue
                
                # Check if this is a Coding Time row
                if any('Coding Time' in part for part in parts):
                    # Skip this row entirely
                    continue
                
                # If we expect 2 columns but this row has 3, remove the third column
                if expected_columns == 2 and len(parts) == 3:
                    # Remove the third column (index 2)
                    new_line = f"| {parts[0]} | {parts[1]} |"
                    cleaned_lines.append(new_line)
                    continue
                
                # If header says 2 columns, update expected_columns
                if 'Metric' in parts[0] and 'GitHub' in parts[1] and len(parts) == 2:
                    expected_columns = 2
                
                # Otherwise keep the line as is
                cleaned_lines.append(line)
            else:
                # Not a table row - reset expected columns if we hit a blank line or section header
                if not line.strip() or line.strip().startswith('##'):
                    expected_columns = None
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove any remaining standalone Wakatime references (but be careful not to break words)
        # Only remove if it's a standalone word
        content = re.sub(r'\bwakatime\b|\bWakatime\b', '', content, flags=re.IGNORECASE)
        
        # Clean up multiple empty lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all calendar files"""
    obsidian_path = Path("/Users/rupali.b/Documents/GitHub/Obsidian")
    calendar_path = obsidian_path / "Calendar"
    
    if not calendar_path.exists():
        print(f"Calendar path not found: {calendar_path}")
        return
    
    # Find all markdown files in Calendar directory
    md_files = list(calendar_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files in Calendar directory")
    print("Removing Wakatime statistics...")
    
    updated_count = 0
    for md_file in md_files:
        if remove_wakatime_from_file(md_file):
            updated_count += 1
            print(f"✅ Updated: {md_file.relative_to(obsidian_path)}")
    
    print(f"\n✅ Completed! Updated {updated_count} out of {len(md_files)} files")

if __name__ == "__main__":
    main()

