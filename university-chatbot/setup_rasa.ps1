$ErrorActionPreference = "Stop"

Write-Host "--- 1. Installing pyenv-win ---"
# Install to user profile .pyenv
$pyenv_root = "$env:USERPROFILE\.pyenv"
if (-not (Test-Path $pyenv_root)) {
    pip install pyenv-win --target $pyenv_root --no-warn-script-location
}
else {
    Write-Host "pyenv directory exists, skipping install..."
}

# Recursively find pyenv.bat to confirm path
$pyenv_bat = Get-ChildItem -Path $pyenv_root -Filter "pyenv.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($pyenv_bat) {
    $pyenv_bin = $pyenv_bat.DirectoryName
    Write-Host "Found pyenv bin at: $pyenv_bin"
    # Expected: ...\.pyenv\pyenv-win\bin
    # Shims: ...\.pyenv\pyenv-win\shims
    # We construct paths based on finding the bin
    
    # We need to explicitly put these in the path for this session
    $env:PYENV_HOME = $pyenv_bin.Parent.FullName
    $env:PATH = "$($pyenv_bin);$($env:PYENV_HOME)\shims;$env:PATH"
}
else {
    Write-Error "Could not find pyenv.bat in $pyenv_root"
}

Write-Host "--- 2. Updating Pyenv and Installing Python 3.10.11 ---"
# Update pyenv database
& pyenv update

pyenv --version
# Try installing
& pyenv install 3.10.11

Write-Host "--- 3. Setting Project Python Version ---"
# Assume running in project dir
& pyenv local 3.10.11
& pyenv rehash

$target_version = python --version 2>&1
Write-Host "Current Python: $target_version"

if ($target_version -notmatch "3.10") {
    Write-Error "Failed to set Python 3.10. Current is: $target_version"
}


Write-Host "--- 4. Creating Virtual Environment ---"
if (-not (Test-Path "venv")) {
    python -m venv venv
}

Write-Host "--- 5. Installing Rasa (3.6.0) ---"
# Use venv pip directly
.\venv\Scripts\pip install rasa==3.6.0

Write-Host "--- 6. Initializing Rasa Project ---"
# Using --no-prompt to default everything
.\venv\Scripts\rasa init --no-prompt

Write-Host "=== SETUP COMPLETE ==="
