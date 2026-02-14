"""
Calendar updater - updates calendar entries with collected data
"""

import re
from datetime import date
from pathlib import Path
from typing import Dict, Optional

from .formatter import CalendarFormatter


class CalendarUpdater:
    """Updates calendar entries with collected data"""
    
    def __init__(self, calendar_path: Path):
        self.calendar_path = Path(calendar_path)
        self.formatter = CalendarFormatter()
    
    def update_calendar_entry(
        self,
        target_date: date,
        github_data: Dict
    ) -> bool:
        """Update calendar entry with all collected data"""
        try:
            # Create calendar file path
            year = target_date.year
            month = target_date.strftime("%B")
            day = target_date.strftime("%d-%m-%Y")
            
            calendar_dir = self.calendar_path / str(year) / month
            calendar_file = calendar_dir / f"{day}.md"
            
            # Ensure directory exists and create file with a basic header if missing
            if not calendar_file.exists():
                calendar_dir.mkdir(parents=True, exist_ok=True)
                header = f"# {month} {target_date.strftime('%d')}, {year}\n\n"
                with open(calendar_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                print(f"🆕 Created calendar file: {calendar_file}")
            
            # Read existing content
            with open(calendar_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Generate content sections
            github_content = self.formatter.format_github_content(github_data)
            datatable_content = self.formatter.create_datatable_content(github_data)
            
            # Remove any existing sections that we'll replace
            # Remove existing sections in order: Protocol, GitHub Activity, Development Analytics
            existing_content = re.sub(
                r'\n## 🔒 Containment & Failure Protocol.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            # Also remove old format without emoji for backwards compatibility
            existing_content = re.sub(
                r'\n## Containment & Failure Protocol.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            existing_content = re.sub(
                r'\n## 🚀 GitHub Activity.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            # Also remove old format without emoji for backwards compatibility
            existing_content = re.sub(
                r'\n## GitHub Activity.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            existing_content = re.sub(
                r'\n## 📈 Development Analytics.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            # Also remove old format without emoji for backwards compatibility
            existing_content = re.sub(
                r'\n## Development Analytics.*?(?=\n## |\Z)',
                '',
                existing_content,
                flags=re.DOTALL
            )
            
            # Combine all content (GitHub first, then Analytics)
            sections = []
            if github_content:
                sections.append(github_content)
            if datatable_content:
                sections.append(datatable_content)
            
            new_content = existing_content.rstrip() + "\n\n" + "\n\n".join(sections)
            
            # Write updated content
            with open(calendar_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated calendar entry: {calendar_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update calendar entry: {e}")
            return False
