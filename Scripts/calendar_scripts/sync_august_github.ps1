# Sync GitHub Commits for August 2025
# This script fetches GitHub activity for each day in August and updates daily notes

param(
    [switch]$DryRun = $false,
    [string]$RepoPath = "D:\Github\SSJK-CRM"
)

# Configuration
$VaultPath = "D:\Github\Obsidian"
$AugustPath = "Calendar\2025\August"
$FullAugustPath = Join-Path $VaultPath $AugustPath

Write-Host "Syncing GitHub Commits for August 2025" -ForegroundColor Cyan
Write-Host "Repository: $RepoPath" -ForegroundColor Yellow
Write-Host "Vault Path: $VaultPath" -ForegroundColor Yellow
Write-Host ""

# Check if repository exists
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    Write-Host "Error: Repository not found at $RepoPath" -ForegroundColor Red
    Write-Host "Please ensure the SSJK-CRM repository exists and is a git repository." -ForegroundColor Yellow
    exit 1
}

# Function to get commits for a specific date
function Get-CommitsForDate {
    param(
        [string]$Date,
        [string]$RepoPath
    )
    
    $dateObj = Get-Date $Date
    $dateStr = $dateObj.ToString("yyyy-MM-dd")
    
    try {
        # Get commits for the specific date
        $commits = git -C $RepoPath log --since="$dateStr 00:00:00" --until="$dateStr 23:59:59" --pretty=format:"%h - %an, %ar : %s" --no-merges 2>$null
        
        if ($commits) {
            return $commits -split "`n" | Where-Object { $_ -match '\S' }
        } else {
            return @()
        }
    } catch {
        Write-Host "Warning: Error fetching commits for $Date" -ForegroundColor Yellow
        return @()
    }
}

# Function to update daily note with GitHub activity
function Update-DailyNote {
    param(
        [string]$FilePath,
        [array]$Commits,
        [string]$Date
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "Warning: File not found: $FilePath" -ForegroundColor Yellow
        return $false
    }
    
    $content = Get-Content $FilePath -Raw -Encoding UTF8
    if (-not $content) {
        $content = ""
    }
    
    # Check if GitHub activity section already exists
    if ($content -match "## GitHub Activity") {
        Write-Host "Info: GitHub activity section already exists, updating..." -ForegroundColor Gray
        
        # Remove existing GitHub activity section
        $content = $content -replace "(?s)## GitHub Activity.*?(?=##|\z)", ""
    }
    
    # Add GitHub activity section
    $githubSection = "`n## GitHub Activity`n`n"
    
    if ($Commits.Count -eq 0) {
        $githubSection += "No commits on this date.`n"
    } else {
        $githubSection += "**Total Commits:** $($Commits.Count)`n`n"
        $githubSection += "### Commits`n`n"
        
        foreach ($commit in $Commits) {
            $githubSection += "- $commit`n"
        }
        
        $githubSection += "`n### Summary`n"
        $githubSection += "- **Date:** $Date`n"
        $githubSection += "- **Repository:** SSJK-CRM`n"
        $githubSection += "- **Activity:** $($Commits.Count) commits`n"
    }
    
    # Add the section to the content
    $content += $githubSection
    
    if (-not $DryRun) {
        try {
            Set-Content -Path $FilePath -Value $content -Encoding UTF8
            Write-Host "Updated: $FilePath" -ForegroundColor Green
            return $true
        } catch {
            Write-Host "Error updating $FilePath" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "[DRY RUN] Would update: $FilePath" -ForegroundColor Cyan
        return $true
    }
}

# Get all August daily note files
$dailyNotes = Get-ChildItem -Path $FullAugustPath -Filter "*.md" | Where-Object { $_.Name -match "^\d{2}-\d{2}-\d{4}\.md$" }

if ($dailyNotes.Count -eq 0) {
    Write-Host "No daily note files found in August directory" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($dailyNotes.Count) daily notes for August 2025:" -ForegroundColor Green
foreach ($note in $dailyNotes) {
    Write-Host "  - $($note.Name)" -ForegroundColor White
}
Write-Host ""

# Process each daily note
$successCount = 0
$totalCount = $dailyNotes.Count

foreach ($note in $dailyNotes) {
    $fileName = $note.Name
    $dateMatch = $fileName -match "(\d{2})-(\d{2})-(\d{4})"
    
    if ($dateMatch) {
        $day = $matches[1]
        $month = $matches[2]
        $year = $matches[3]
        $dateStr = "$year-$month-$day"
        
        Write-Host "Processing: $fileName ($dateStr)" -ForegroundColor Cyan
        
        # Get commits for this date
        $commits = Get-CommitsForDate -Date $dateStr -RepoPath $RepoPath
        
        if ($commits.Count -gt 0) {
            Write-Host "  Found $($commits.Count) commits" -ForegroundColor Green
        } else {
            Write-Host "  No commits found" -ForegroundColor Gray
        }
        
        # Update the daily note
        $updated = Update-DailyNote -FilePath $note.FullName -Commits $commits -Date $dateStr
        
        if ($updated) {
            $successCount++
        }
        
        Write-Host ""
    } else {
        Write-Host "Skipping $fileName - invalid date format" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "Sync Summary" -ForegroundColor Green
Write-Host "================" -ForegroundColor Green
Write-Host "Total daily notes processed: $totalCount" -ForegroundColor White
Write-Host "Successfully updated: $successCount" -ForegroundColor Green
Write-Host "Failed: $($totalCount - $successCount)" -ForegroundColor Red

if ($DryRun) {
    Write-Host "`nThis was a DRY RUN - no files were actually modified" -ForegroundColor Cyan
    Write-Host "Run without -DryRun to actually update the files" -ForegroundColor Yellow
} else {
    Write-Host "`nGitHub commit sync completed for August 2025!" -ForegroundColor Green
}

Write-Host "`nTip: Check your daily notes to see the updated GitHub activity sections" -ForegroundColor Yellow
