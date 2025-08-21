# Obsidian Script Manager
# Simple script launcher for Obsidian vault automation

param(
    [switch]$ListOnly = $false,
    [string]$RunScript = ""
)

# Script configuration
$ScriptsRoot = Join-Path $PSScriptRoot ".."
$VaultPath = "D:\Github\Obsidian"

# Color functions
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-ScriptMenu {
    Clear-Host
    Write-ColorOutput "========================================" "Cyan"
    Write-ColorOutput "    Obsidian Script Manager" "Cyan"
    Write-ColorOutput "========================================" "Cyan"
    Write-Host ""
    
    $scripts = Get-AllScripts
    $scriptIndex = 1
    
    foreach ($category in $scripts.Keys) {
        if ($scripts[$category].Count -gt 0) {
            Write-ColorOutput "📁 $category" "Green"
            foreach ($script in $scripts[$category]) {
                $scriptType = $script.Extension.Substring(1).ToUpper()
                Write-ColorOutput "  $scriptIndex. $($script.Name) [$scriptType]" "White"
                $scriptIndex++
            }
            Write-Host ""
        }
    }
    
    Write-ColorOutput "0. Exit" "Red"
    Write-Host ""
}

function Get-AllScripts {
    $scripts = @{
        "Calendar Scripts" = @()
        "Automation Scripts" = @()
        "Utility Scripts" = @()
    }
    
    $allScripts = Get-ChildItem -Path $ScriptsRoot -Recurse -Include "*.ps1", "*.py", "*.bat", "*.sh" | Sort-Object FullName
    
    foreach ($script in $allScripts) {
        $relativePath = $script.FullName.Replace($ScriptsRoot, "").TrimStart("\")
        $category = $relativePath.Split("\")[0]
        
        if ($scripts.ContainsKey($category)) {
            $scripts[$category] += $script
        }
    }
    
    return $scripts
}

function Run-Script {
    param([string]$ScriptPath)
    
    if (-not (Test-Path $ScriptPath)) {
        Write-ColorOutput "❌ Script not found: $ScriptPath" "Red"
        return
    }
    
    Clear-Host
    Write-ColorOutput "========================================" "Cyan"
    Write-ColorOutput "    Running Script" "Cyan"
    Write-ColorOutput "========================================" "Cyan"
    Write-Host ""
    Write-ColorOutput "Script: $($ScriptPath | Split-Path -Leaf)" "Yellow"
    Write-ColorOutput "Path: $ScriptPath" "Gray"
    Write-Host ""
    
    $scriptExtension = (Get-Item $ScriptPath).Extension.ToLower()
    
    try {
        switch ($scriptExtension) {
            ".ps1" {
                Write-ColorOutput "Executing PowerShell script..." "Green"
                Write-Host ""
                & $ScriptPath
            }
            ".py" {
                Write-ColorOutput "Executing Python script..." "Green"
                Write-Host ""
                python $ScriptPath
            }
            ".bat" {
                Write-ColorOutput "Executing Batch script..." "Green"
                Write-Host ""
                & $ScriptPath
            }
            default {
                Write-ColorOutput "Unsupported script type: $scriptExtension" "Red"
            }
        }
    } catch {
        Write-ColorOutput "Error executing script: $($_.Exception.Message)" "Red"
    }
    
    Write-Host ""
    Write-ColorOutput "Script execution completed. Press any key to continue..." "Yellow"
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Get-ScriptByIndex {
    param([int]$Index)
    
    $scripts = Get-AllScripts
    $scriptIndex = 1
    
    foreach ($category in $scripts.Keys) {
        foreach ($script in $scripts[$category]) {
            if ($scriptIndex -eq $Index) {
                return $script
            }
            $scriptIndex++
        }
    }
    
    return $null
}

# Main execution
if ($ListOnly) {
    # Just list all scripts
    $scripts = Get-AllScripts
    Write-ColorOutput "📁 Available Scripts:" "Green"
    Write-Host ""
    
    foreach ($category in $scripts.Keys) {
        if ($scripts[$category].Count -gt 0) {
            Write-ColorOutput "📁 $category" "Green"
            foreach ($script in $scripts[$category]) {
                $scriptType = $script.Extension.Substring(1).ToUpper()
                Write-ColorOutput "  📄 $($script.Name) [$scriptType]" "White"
            }
            Write-Host ""
        }
    }
} elseif ($RunScript -ne "") {
    # Run specific script by path
    Run-Script -ScriptPath $RunScript
} else {
    # Interactive menu mode
    do {
        Show-ScriptMenu
        $choice = Read-Host "Select a script to run (0-$((Get-AllScripts).Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum)"
        
        if ($choice -eq "0") {
            Write-ColorOutput "Goodbye!" "Green"
            break
        } elseif ($choice -match '^\d+$') {
            $selectedScript = Get-ScriptByIndex -Index [int]$choice
            if ($selectedScript) {
                Run-Script -ScriptPath $selectedScript.FullName
            } else {
                Write-ColorOutput "Invalid selection. Press any key to continue..." "Red"
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        } else {
            Write-ColorOutput "Invalid option. Press any key to continue..." "Red"
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    } while ($true)
}
