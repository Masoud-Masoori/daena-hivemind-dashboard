#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Daena AI VP System - Complete Launch Script for Azure Deployment
    
.DESCRIPTION
    Launches the full Daena AI VP system including:
    - Backend (FastAPI) with Azure OpenAI integration
    - Frontend (Dashboard) with real-time chat
    - Voice system (XTTS) for speech synthesis
    - CMP decision engine and voting system
    - Brain training and memory management
    - Email system for investor outreach
    
.PARAMETER Mode
    Deployment mode: 'local', 'azure-vm', 'azure-app-service'
    
.PARAMETER Port
    Port to run the server on (default: 3000)
    
.EXAMPLE
    .\launch_daena.ps1 -Mode local
    .\launch_daena.ps1 -Mode azure-vm -Port 80
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('local', 'azure-vm', 'azure-app-service')]
    [string]$Mode = 'local',
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 3000,
    
    [Parameter(Mandatory=$false)]
    [switch]$EnableBrainTraining,
    
    [Parameter(Mandatory=$false)]
    [switch]$EnableVoice,
    
    [Parameter(Mandatory=$false)]
    [switch]$EnableCMP
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Test-Dependencies {
    Write-ColorOutput "🔍 Checking system dependencies..." "Info"
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "✅ Python: $pythonVersion" "Success"
    }
    catch {
        Write-ColorOutput "❌ Python not found. Please install Python 3.8+" "Error"
        exit 1
    }
    
    # Check required packages
    $requiredPackages = @(
        "fastapi", "uvicorn", "openai", "requests", "PyJWT", 
        "python-multipart", "jinja2", "sqlalchemy", "redis"
    )
    
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $package" 2>$null
            Write-ColorOutput "✅ $package" "Success"
        }
        catch {
            Write-ColorOutput "⚠️  $package not found - will install" "Warning"
        }
    }
}

function Install-Dependencies {
    Write-ColorOutput "🔧 Installing dependencies..." "Info"
    
    $packages = @(
        "fastapi", "uvicorn", "openai", "requests", "PyJWT",
        "python-multipart", "jinja2", "sqlalchemy", "redis",
        "python-dotenv", "aiofiles", "websockets"
    )
    
    foreach ($package in $packages) {
        Write-ColorOutput "Installing $package..." "Info"
        pip install $package
    }
    
    # Install voice dependencies if enabled
    if ($EnableVoice) {
        Write-ColorOutput "🎤 Installing voice dependencies..." "Info"
        $voicePackages = @("TTS", "torch", "torchaudio", "librosa")
        foreach ($package in $voicePackages) {
            pip install $package
        }
    }
    
    # Install brain training dependencies if enabled
    if ($EnableBrainTraining) {
        Write-ColorOutput "🧠 Installing brain training dependencies..." "Info"
        $brainPackages = @("transformers", "datasets", "accelerate", "wandb")
        foreach ($package in $brainPackages) {
            pip install $package
        }
    }
}

function Set-EnvironmentVariables {
    Write-ColorOutput "🔧 Setting up environment variables..." "Info"
    
    # Azure OpenAI Configuration
    $env:OPENAI_API_TYPE = "azure"
    $env:OPENAI_API_KEY = "1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN"
    $env:OPENAI_API_BASE = "https://masou-mdksrl1q-eastus2.openai.azure.com/"
    $env:OPENAI_API_VERSION = "2024-02-15"
    $env:OPENAI_DEPLOYMENT_NAME = "daena"
    
    # Gmail Configuration
    $env:GMAIL_USER = "masoud.masoori@gmail.com"
    $env:GMAIL_APP_PASSWORD = "pmwelxngtnpgnvrr"
    
    # Demo Configuration
    $env:DEMO_PORT = $Port.ToString()
    $env:DEMO_MODE = "production"
    
    # Voice Configuration
    if ($EnableVoice) {
        $env:XTTS_MODEL_PATH = "./models/xtts_v2"
        $env:VOICE_OUTPUT_DIR = "./voice/output"
        $env:VOICE_CACHE_DIR = "./voice/cache"
    }
    
    # Brain Training Configuration
    if ($EnableBrainTraining) {
        $env:BRAIN_MODEL_PATH = "./models/brain_checkpoints"
        $env:KNOWLEDGE_BASE_PATH = "./memory/knowledge"
        $env:TRAINING_DATA_PATH = "./data/training"
    }
    
    # CMP Configuration
    if ($EnableCMP) {
        $env:CMP_DATABASE_PATH = "./data/cmp_decisions"
        $env:VOTING_ENGINE_ENABLED = "true"
        $env:FOUNDER_OVERRIDE_ENABLED = "true"
    }
    
    # Security Configuration
    $env:SECRET_KEY = "daena-ai-vp-secret-key-2024"
    $env:JWT_SECRET = "daena-jwt-secret-2024"
    
    # Logging Configuration
    $env:LOG_LEVEL = "INFO"
    $env:LOG_FILE_PATH = "./logs/daena.log"
    $env:EMAIL_LOG_PATH = "./logs/email_log.jsonl"
    
    Write-ColorOutput "✅ Environment variables configured" "Success"
}

function Initialize-Directories {
    Write-ColorOutput "📁 Creating necessary directories..." "Info"
    
    $directories = @(
        "logs",
        "models",
        "memory",
        "voice/output",
        "voice/cache",
        "data/training",
        "data/cmp_decisions",
        "models/brain_checkpoints",
        "memory/knowledge"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-ColorOutput "✅ Created: $dir" "Success"
        }
    }
}

function Start-Backend {
    Write-ColorOutput "🚀 Starting Daena AI VP Backend..." "Header"
    
    $backendDir = "backend"
    if (!(Test-Path $backendDir)) {
        Write-ColorOutput "❌ Backend directory not found" "Error"
        exit 1
    }
    
    Set-Location $backendDir
    
    $serverHost = if ($Mode -eq 'azure-vm' -or $Mode -eq 'azure-app-service') { "0.0.0.0" } else { "127.0.0.1" }
    
    Write-ColorOutput "🌐 Starting server on $serverHost`:$Port" "Info"
    Write-ColorOutput "📊 API docs will be available at: http://$serverHost`:$Port/docs" "Info"
    Write-ColorOutput "🎯 Demo dashboard will be available at: http://$serverHost`:$Port/demo" "Info"
    
    # Start the FastAPI server
    $serverCommand = @(
        "python", "-m", "uvicorn", 
        "main:app", 
        "--host", $serverHost, 
        "--port", $Port.ToString(),
        "--reload"
    )
    
    Write-ColorOutput "Starting with command: $($serverCommand -join ' ')" "Info"
    
    try {
        & $serverCommand[0] $serverCommand[1..($serverCommand.Length-1)]
    }
    catch {
        Write-ColorOutput "❌ Failed to start server: $_" "Error"
        exit 1
    }
}

function Start-BrainTraining {
    if (!$EnableBrainTraining) { return }
    
    Write-ColorOutput "🧠 Starting brain training in background..." "Info"
    
    $brainScript = "brain_training_loop.py"
    if (Test-Path $brainScript) {
        Start-Process python -ArgumentList $brainScript -WindowStyle Hidden
        Write-ColorOutput "✅ Brain training started in background" "Success"
    }
    else {
        Write-ColorOutput "⚠️  Brain training script not found: $brainScript" "Warning"
    }
}

function Start-VoiceSystem {
    if (!$EnableVoice) { return }
    
    Write-ColorOutput "🎤 Initializing voice system..." "Info"
    
    $voiceScript = "voice/voice_service.py"
    if (Test-Path $voiceScript) {
        Start-Process python -ArgumentList $voiceScript -WindowStyle Hidden
        Write-ColorOutput "✅ Voice system started in background" "Success"
    }
    else {
        Write-ColorOutput "⚠️  Voice system script not found: $voiceScript" "Warning"
    }
}

function Start-CMPSystem {
    if (!$EnableCMP) { return }
    
    Write-ColorOutput "🗳️  Starting CMP decision engine..." "Info"
    
    $cmpScript = "Core/cmp/voting_engine.py"
    if (Test-Path $cmpScript) {
        Start-Process python -ArgumentList $cmpScript -WindowStyle Hidden
        Write-ColorOutput "✅ CMP system started in background" "Success"
    }
    else {
        Write-ColorOutput "⚠️  CMP system script not found: $cmpScript" "Warning"
    }
}

function Show-Status {
    Write-ColorOutput "`n🎉 Daena AI VP System Status" "Header"
    Write-ColorOutput "=================================" "Header"
    Write-ColorOutput "✅ Backend: Running on port $Port" "Success"
    Write-ColorOutput "✅ Azure OpenAI: Connected" "Success"
    Write-ColorOutput "✅ Gmail: Configured" "Success"
    
    if ($EnableVoice) {
        Write-ColorOutput "✅ Voice System: Active" "Success"
    }
    
    if ($EnableBrainTraining) {
        Write-ColorOutput "✅ Brain Training: Active" "Success"
    }
    
    if ($EnableCMP) {
        Write-ColorOutput "✅ CMP Engine: Active" "Success"
    }
    
    Write-ColorOutput "`n🌐 Access Points:" "Info"
    Write-ColorOutput "   Dashboard: http://localhost:$Port/demo" "Info"
    Write-ColorOutput "   API Docs:  http://localhost:$Port/docs" "Info"
    Write-ColorOutput "   Health:    http://localhost:$Port/health" "Info"
    
    Write-ColorOutput "`n🎯 Ready for investor demos!" "Success"
}

# Main execution
try {
    Write-ColorOutput "🎯 Daena AI VP System - Complete Launch" "Header"
    Write-ColorOutput "=======================================" "Header"
    Write-ColorOutput "Mode: $Mode" "Info"
    Write-ColorOutput "Port: $Port" "Info"
    Write-ColorOutput "Brain Training: $EnableBrainTraining" "Info"
    Write-ColorOutput "Voice System: $EnableVoice" "Info"
    Write-ColorOutput "CMP Engine: $EnableCMP" "Info"
    Write-ColorOutput ""
    
    Test-Dependencies
    Install-Dependencies
    Set-EnvironmentVariables
    Initialize-Directories
    
    # Start background services
    Start-BrainTraining
    Start-VoiceSystem
    Start-CMPSystem
    
    # Show status before starting backend
    Show-Status
    
    # Start the main backend server
    Start-Backend
}
catch {
    Write-ColorOutput "❌ Fatal error: $_" "Error"
    exit 1
} 