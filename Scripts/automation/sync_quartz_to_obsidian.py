#!/usr/bin/env python3
"""
Quartz to Obsidian Content Synchronization
Synchronizes daily note content from Quartz calendar to Obsidian vault
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync_log.txt'),
        logging.StreamHandler()
    ]
)

class QuartzToObsidianSync:
    def __init__(self, obsidian_path, quartz_path):
        self.obsidian_path = Path(obsidian_path)
        self.quartz_path = Path(quartz_path)
        self.sync_stats = {
            'total_files': 0,
            'synced_files': 0,
            'skipped_files': 0,
            'error_files': 0
        }
        
    def sync_daily_notes(self, year, month):
        """Sync daily notes from Quartz to Obsidian for a specific month"""
        logging.info(f"🔄 Syncing daily notes for {month} {year}")
        
        obsidian_month_path = self.obsidian_path / "Calendar" / str(year) / month
        quartz_month_path = self.quartz_path / "content" / "Calendar" / str(year) / month
        
        if not obsidian_month_path.exists():
            logging.error(f"❌ Obsidian month path not found: {obsidian_month_path}")
            return
            
        if not quartz_month_path.exists():
            logging.warning(f"⚠️ Quartz month path not found: {quartz_month_path}")
            return
        
        # Get daily note files
        daily_notes = list(obsidian_month_path.glob("*-*-*.md"))
        logging.info(f"📝 Found {len(daily_notes)} daily notes in Obsidian")
        
        for note in daily_notes:
            self.sync_single_note(note, quartz_month_path)
    
    def sync_single_note(self, obsidian_note, quartz_month_path):
        """Sync content for a single daily note"""
        note_name = obsidian_note.name
        self.sync_stats['total_files'] += 1
        
        # Look for corresponding Quartz file
        quartz_note = quartz_month_path / note_name
        
        if not quartz_note.exists():
            logging.warning(f"  ⚠️ No Quartz file found for: {note_name}")
            self.sync_stats['skipped_files'] += 1
            return
            
        logging.info(f"  📝 Syncing: {note_name}")
        
        try:
            # Read content from both files
            obsidian_content = obsidian_note.read_text(encoding='utf-8')
            quartz_content = quartz_note.read_text(encoding='utf-8')
            
            # Extract non-GitHub, non-location content from Quartz
            quartz_daily_notes = self.extract_daily_notes_content(quartz_content)
            
            # Update Obsidian file
            updated_content = self.update_obsidian_content(obsidian_content, quartz_daily_notes)
            
            # Write back to Obsidian file
            obsidian_note.write_text(updated_content, encoding='utf-8')
            logging.info(f"    ✅ Updated: {note_name}")
            self.sync_stats['synced_files'] += 1
            
        except Exception as e:
            logging.error(f"    ❌ Error syncing {note_name}: {str(e)}")
            self.sync_stats['error_files'] += 1
    
    def extract_daily_notes_content(self, content):
        """Extract daily notes content, excluding GitHub activity and location info"""
        lines = content.split('\n')
        daily_notes_lines = []
        in_daily_notes = False
        
        for line in lines:
            if '## Daily Notes' in line:
                in_daily_notes = True
                daily_notes_lines.append(line)
                continue
            elif line.startswith('## ') and in_daily_notes:
                # End of daily notes section
                break
            elif in_daily_notes:
                # Skip location-related lines and GitHub activity
                if not any(keyword in line.lower() for keyword in ['location:', 'coordinates:', 'github activity']):
                    daily_notes_lines.append(line)
        
        return '\n'.join(daily_notes_lines)
    
    def update_obsidian_content(self, obsidian_content, quartz_daily_notes):
        """Update Obsidian content with Quartz daily notes"""
        # Find the Daily Notes section
        pattern = r'(## Daily Notes\s*\n)(.*?)(\n## )'
        match = re.search(pattern, obsidian_content, re.DOTALL)
        
        if match:
            # Replace the content between ## Daily Notes and next ##
            replacement = f'{match.group(1)}{quartz_daily_notes.strip()}\n{match.group(3)}'
            return re.sub(pattern, replacement, obsidian_content, flags=re.DOTALL)
        else:
            # If no Daily Notes section found, add it before GitHub Activity
            if '## GitHub Activity' in obsidian_content:
                pattern = r'(## GitHub Activity)'
                replacement = f'{quartz_daily_notes.strip()}\n\n\\1'
                return re.sub(pattern, replacement, obsidian_content)
            else:
                # Add at the end if no GitHub Activity section
                return obsidian_content + f'\n\n{quartz_daily_notes.strip()}'
    
    def print_sync_stats(self):
        """Print synchronization statistics"""
        logging.info("")
        logging.info("📊 Sync Statistics:")
        logging.info(f"   Total files processed: {self.sync_stats['total_files']}")
        logging.info(f"   Successfully synced: {self.sync_stats['synced_files']}")
        logging.info(f"   Skipped (no Quartz file): {self.sync_stats['skipped_files']}")
        logging.info(f"   Errors: {self.sync_stats['error_files']}")
        
        if self.sync_stats['error_files'] > 0:
            logging.warning("⚠️ Some files had errors during sync. Check sync_log.txt for details.")

def main():
    parser = argparse.ArgumentParser(description='Sync content from Quartz to Obsidian')
    parser.add_argument('--year', type=int, default=2025, help='Year to sync')
    parser.add_argument('--month', type=str, help='Month to sync (e.g., July)')
    parser.add_argument('--all-months', action='store_true', help='Sync all months')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be synced without making changes')
    
    args = parser.parse_args()
    
    # Paths
    obsidian_path = r"D:\Github\Obsidian"
    quartz_path = r"D:\Github\quartz"
    
    if args.dry_run:
        logging.info("🔍 DRY RUN MODE - No files will be modified")
    
    sync = QuartzToObsidianSync(obsidian_path, quartz_path)
    
    if args.all_months:
        # Sync all months
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
        for month in months:
            sync.sync_daily_notes(args.year, month)
    elif args.month:
        # Sync specific month
        sync.sync_daily_notes(args.year, args.month)
    else:
        # Sync current month
        current_month = datetime.now().strftime('%B')
        sync.sync_daily_notes(args.year, current_month)
    
    sync.print_sync_stats()
    logging.info("🎉 Content synchronization completed!")

if __name__ == "__main__":
    main()
