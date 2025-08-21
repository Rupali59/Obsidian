# Cleanup Daily Notes Script
# Cleans up formatting and removes unnecessary content from daily notes

param(
    [string]$Year = "2025",
    [string]$Month = "",
    [switch]$AllMonths = $false,
    [switch]$DryRun = $false,
    [switch]$RemoveEmptySections = $false
)

# Script configuration
$VaultPath = "D:\Github\Obsidian"
$CalendarPath = Join-Path $VaultPath "Calendar\$Year"

Write-Host "🧹 Cleaning up Daily Notes for Year: $Year" -ForegroundColor Green
if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}
Write-Host ""

# Function to clean up a single daily note
function Cleanup-DailyNote {
    param([string]$NotePath)
    
    if (-not (Test-Path $NotePath)) {
        Write-Host "  ❌ File not found: $NotePath" -ForegroundColor Red
        return
    }
    
    $content = Get-Content $NotePath -Raw
    $originalContent = $content
    $changes = @()
    
    # Remove multiple blank lines
    $content = $content -replace '\n\s*\n\s*\n+', "`n`n"
    
    # Remove trailing whitespace
    $content = $content -replace '[ \t]+$', '', 'Multiline'
    
    # Remove empty sections (if requested)
    if ($RemoveEmptySections) {
        $content = $content -replace '## [^`n]+\n\s*\n', ''
        $changes += "Removed empty sections"
    }
    
    # Standardize section headers
    $content = $content -replace '##\s+', '## '
    
    # Remove location-related content
    $content = $content -replace '(?m)^\s*-\s*Location:.*$', ''
    $content = $content -replace '(?m)^\s*-\s*Coordinates:.*$', ''
    
    # Clean up corrupted daily notes content
    $content = $content -replace '(?m)^\s*-\s*,\s*$', ''
    $content = $content -replace '(?m)^\s*-\s*[0-9]\s*$', ''
    
    # Check if content changed
    if ($content -ne $originalContent) {
        $changes += "Cleaned formatting"
        
        if ($DryRun) {
            Write-Host "    🔍 Would apply changes: $($changes -join ', ')" -ForegroundColor Yellow
        } else {
            Set-Content -Path $NotePath -Value $content -Encoding UTF8
            Write-Host "    ✅ Applied changes: $($changes -join ', ')" -ForegroundColor Green
        }
    } else {
        Write-Host "    ℹ️ No changes needed" -ForegroundColor Gray
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
            Write-Host "  📝 Processing: $($note.Name)" -ForegroundColor Cyan
            Cleanup-DailyNote -NotePath $note.FullName
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
Write-Host "🎉 Daily notes cleanup completed!" -ForegroundColor Green
if ($DryRun) {
    Write-Host "💡 Run without -DryRun to actually apply changes" -ForegroundColor Yellow
}
