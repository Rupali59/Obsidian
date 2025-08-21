# Update GitHub Activity in Daily Notes
# This script updates GitHub activity sections in daily note files

param(
    [string]$Year = "2025",
    [string]$Month = "",
    [switch]$AllMonths = $false,
    [switch]$DryRun = $false
)

# Script configuration
$VaultPath = "D:\Github\Obsidian"
$CalendarPath = Join-Path $VaultPath "Calendar\$Year"
$GitRepoPath = "D:\Github\SSJK-CRM"

Write-Host "🔍 Updating GitHub Activity for Year: $Year" -ForegroundColor Green
if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}
Write-Host ""

# Function to get GitHub commits for a specific date
function Get-GitHubCommits {
    param([string]$Date)
    
    $dateParam = $Date.ToString("yyyy-MM-dd")
    $gitLog = git -C $GitRepoPath log --oneline --since="$dateParam 00:00" --until="$dateParam 23:59" --pretty=format:"%h %s (%an, %ad)" --date=short 2>$null
    
    if ($gitLog) {
        return $gitLog -split "`n" | Where-Object { $_ -match '\S' }
    }
    return @()
}

# Function to update GitHub activity in a daily note
function Update-DailyNoteGitHubActivity {
    param([string]$NotePath, [string]$Date)
    
    if (-not (Test-Path $NotePath)) {
        Write-Host "  ❌ File not found: $NotePath" -ForegroundColor Red
        return
    }
    
    $content = Get-Content $NotePath -Raw
    $commits = Get-GitHubCommits -Date $Date
    
    if ($commits.Count -eq 0) {
        Write-Host "  📝 No commits found for $Date" -ForegroundColor Gray
        return
    }
    
    Write-Host "  📝 Found $($commits.Count) commits for $Date" -ForegroundColor Cyan
    
    # Create GitHub activity section
    $githubSection = @"
## GitHub Activity

**Repository:** [SSJK-CRM](https://github.com/Rupali59/SSJK-CRM)

**Commits on $Date**
"@
    
    foreach ($commit in $commits) {
        $githubSection += "`n- $commit"
    }
    
    $githubSection += "`n`n"
    
    # Check if GitHub Activity section already exists
    if ($content -match '## GitHub Activity') {
        if ($DryRun) {
            Write-Host "    🔍 Would update existing GitHub Activity section" -ForegroundColor Yellow
        } else {
            # Replace existing section
            $pattern = '(## GitHub Activity.*?)(?=\n## |$)'
            $newContent = $content -replace $pattern, $githubSection
            Set-Content -Path $NotePath -Value $newContent -Encoding UTF8
            Write-Host "    ✅ Updated GitHub Activity section" -ForegroundColor Green
        }
    } else {
        if ($DryRun) {
            Write-Host "    🔍 Would add new GitHub Activity section" -ForegroundColor Yellow
        } else {
            # Add new section before the end of file
            $newContent = $content.TrimEnd() + "`n`n" + $githubSection
            Set-Content -Path $NotePath -Value $newContent -Encoding UTF8
            Write-Host "    ✅ Added new GitHub Activity section" -ForegroundColor Green
        }
    }
}

# Function to process a single month
function Process-Month {
    param([string]$MonthPath)
    
    if (Test-Path $MonthPath) {
        $monthName = Split-Path $MonthPath -Leaf
        Write-Host "📅 Processing month: $monthName" -ForegroundColor Yellow
        
        $dailyNotes = Get-ChildItem -Path $MonthPath -Filter "*-*-*.md" | Sort-Object Name
        
        foreach ($note in $dailyNotes) {
            # Extract date from filename (DD-MM-YYYY.md)
            if ($note.Name -match '(\d{2})-(\d{2})-(\d{4})\.md') {
                $day = $matches[1]
                $month = $matches[2]
                $year = $matches[3]
                $date = Get-Date "$year-$month-$day"
                
                Write-Host "  📝 Processing: $($note.Name)" -ForegroundColor Cyan
                Update-DailyNoteGitHubActivity -NotePath $note.FullName -Date $date
            }
        }
        
        Write-Host "  ✅ Completed: $($dailyNotes.Count) daily notes" -ForegroundColor Green
    }
}

# Main execution
if ($AllMonths) {
    # Process all months
    $monthFolders = Get-ChildItem -Path $CalendarPath -Directory | Sort-Object Name
    
    foreach ($month in $monthFolders) {
        Process-Month -MonthPath $month.FullName
    }
} elseif ($Month -ne "") {
    # Process specific month
    $monthPath = Join-Path $CalendarPath $Month
    Process-Month -MonthPath $monthPath
} else {
    # Process current month
    $currentMonth = (Get-Date).ToString("MMMM")
    $monthPath = Join-Path $CalendarPath $currentMonth
    Process-Month -MonthPath $monthPath
}

Write-Host ""
Write-Host "🎉 GitHub Activity update completed!" -ForegroundColor Green
if ($DryRun) {
    Write-Host "💡 Run without -DryRun to actually update files" -ForegroundColor Yellow
}
