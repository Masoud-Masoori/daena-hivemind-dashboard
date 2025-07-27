#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Azure Deployment Script for Daena AI VP System
    
.DESCRIPTION
    Deploys Daena AI VP to Azure VM (for brain training) and App Service (for production)
    
.PARAMETER ResourceGroup
    Azure resource group name
    
.PARAMETER Location
    Azure region (default: eastus2)
    
.PARAMETER DeployVM
    Deploy GPU VM for brain training
    
.PARAMETER DeployAppService
    Deploy App Service for production
    
.EXAMPLE
    .\azure-deploy.ps1 -ResourceGroup "daena-ai-vp" -DeployVM -DeployAppService
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus2",
    
    [Parameter(Mandatory=$false)]
    [switch]$DeployVM,
    
    [Parameter(Mandatory=$false)]
    [switch]$DeployAppService
)

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

function Test-AzureCLI {
    Write-ColorOutput "🔍 Checking Azure CLI..." "Info"
    
    try {
        $azVersion = az version --output json | ConvertFrom-Json
        Write-ColorOutput "✅ Azure CLI version: $($azVersion.'azure-cli')" "Success"
        return $true
    }
    catch {
        Write-ColorOutput "❌ Azure CLI not found. Please install Azure CLI first." "Error"
        Write-ColorOutput "   Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" "Info"
        return $false
    }
}

function Test-AzureLogin {
    Write-ColorOutput "🔐 Checking Azure login..." "Info"
    
    try {
        $account = az account show --output json | ConvertFrom-Json
        Write-ColorOutput "✅ Logged in as: $($account.user.name)" "Success"
        Write-ColorOutput "   Subscription: $($account.name)" "Info"
        return $true
    }
    catch {
        Write-ColorOutput "❌ Not logged in to Azure. Please run 'az login'" "Error"
        return $false
    }
}

function New-ResourceGroup {
    Write-ColorOutput "📦 Creating resource group..." "Info"
    
    try {
        az group create --name $ResourceGroup --location $Location --output none
        Write-ColorOutput "✅ Resource group '$ResourceGroup' created in $Location" "Success"
    }
    catch {
        Write-ColorOutput "❌ Failed to create resource group: $_" "Error"
        exit 1
    }
}

function New-GPUVM {
    Write-ColorOutput "🖥️  Creating GPU VM for brain training..." "Info"
    
    $vmName = "daena-brain-vm"
    $adminUsername = "azureuser"
    
    try {
        # Create VM with GPU
        Write-ColorOutput "Creating VM with NC6 GPU..." "Info"
        az vm create `
            --resource-group $ResourceGroup `
            --name $vmName `
            --image Ubuntu2204 `
            --size Standard_NC6 `
            --admin-username $adminUsername `
            --generate-ssh-keys `
            --output none
        
        # Get VM IP
        $vmIP = az vm show --resource-group $ResourceGroup --name $vmName --show-details --query "publicIps" --output tsv
        
        Write-ColorOutput "✅ GPU VM created successfully!" "Success"
        Write-ColorOutput "   VM Name: $vmName" "Info"
        Write-ColorOutput "   IP Address: $vmIP" "Info"
        Write-ColorOutput "   SSH Command: ssh $adminUsername@$vmIP" "Info"
        
        # Create setup script for VM
        $setupScript = @"
#!/bin/bash
# Daena AI VP VM Setup Script

echo "🚀 Setting up Daena AI VP on Azure VM..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv git curl

# Clone repository
git clone https://github.com/Masoud-Masoori/daena-hivemind-dashboard.git
cd daena-hivemind-dashboard

# Create virtual environment
python3 -m venv env_merged
source env_merged/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env
echo "Please edit .env with your Azure OpenAI credentials"

# Launch Daena
echo "🎯 Launching Daena AI VP..."
./launch_daena.ps1 -Mode azure-vm -EnableBrainTraining -EnableVoice -EnableCMP
"@
        
        $setupScript | Out-File -FilePath "vm-setup.sh" -Encoding UTF8
        Write-ColorOutput "✅ VM setup script created: vm-setup.sh" "Success"
        
    }
    catch {
        Write-ColorOutput "❌ Failed to create VM: $_" "Error"
        exit 1
    }
}

function New-AppService {
    Write-ColorOutput "🌐 Creating App Service for production..." "Info"
    
    $appServiceName = "daena-ai-vp-app"
    $appServicePlan = "daena-app-plan"
    
    try {
        # Create App Service Plan
        Write-ColorOutput "Creating App Service Plan..." "Info"
        az appservice plan create `
            --resource-group $ResourceGroup `
            --name $appServicePlan `
            --sku B1 `
            --is-linux `
            --output none
        
        # Create Web App
        Write-ColorOutput "Creating Web App..." "Info"
        az webapp create `
            --resource-group $ResourceGroup `
            --plan $appServicePlan `
            --name $appServiceName `
            --runtime "PYTHON:3.9" `
            --output none
        
        # Configure environment variables
        Write-ColorOutput "Configuring environment variables..." "Info"
        az webapp config appsettings set `
            --resource-group $ResourceGroup `
            --name $appServiceName `
            --settings `
            OPENAI_API_TYPE=azure `
            OPENAI_API_BASE=https://masou-mdksrl1q-eastus2.openai.azure.com/ `
            OPENAI_API_VERSION=2024-02-15 `
            OPENAI_DEPLOYMENT_NAME=daena `
            DEMO_MODE=production `
            --output none
        
        # Get app URL
        $appUrl = az webapp show --resource-group $ResourceGroup --name $appServiceName --query "defaultHostName" --output tsv
        
        Write-ColorOutput "✅ App Service created successfully!" "Success"
        Write-ColorOutput "   App Name: $appServiceName" "Info"
        Write-ColorOutput "   URL: https://$appUrl" "Info"
        Write-ColorOutput "   Demo: https://$appUrl/demo" "Info"
        
    }
    catch {
        Write-ColorOutput "❌ Failed to create App Service: $_" "Error"
        exit 1
    }
}

function New-StorageAccount {
    Write-ColorOutput "💾 Creating storage account for models and logs..." "Info"
    
    $storageAccountName = "daena$((Get-Random -Minimum 1000 -Maximum 9999))"
    
    try {
        # Create storage account
        az storage account create `
            --resource-group $ResourceGroup `
            --name $storageAccountName `
            --location $Location `
            --sku Standard_LRS `
            --output none
        
        # Create containers
        az storage container create `
            --account-name $storageAccountName `
            --name models `
            --output none
        
        az storage container create `
            --account-name $storageAccountName `
            --name logs `
            --output none
        
        az storage container create `
            --account-name $storageAccountName `
            --name voice `
            --output none
        
        Write-ColorOutput "✅ Storage account created: $storageAccountName" "Success"
        Write-ColorOutput "   Models container: models" "Info"
        Write-ColorOutput "   Logs container: logs" "Info"
        Write-ColorOutput "   Voice container: voice" "Info"
        
    }
    catch {
        Write-ColorOutput "❌ Failed to create storage account: $_" "Error"
        exit 1
    }
}

function Show-DeploymentSummary {
    Write-ColorOutput "`n🎉 Azure Deployment Summary" "Header"
    Write-ColorOutput "=============================" "Header"
    Write-ColorOutput "Resource Group: $ResourceGroup" "Info"
    Write-ColorOutput "Location: $Location" "Info"
    
    if ($DeployVM) {
        Write-ColorOutput "✅ GPU VM: daena-brain-vm" "Success"
        Write-ColorOutput "   Purpose: Brain training and model development" "Info"
        Write-ColorOutput "   Setup: Run vm-setup.sh on the VM" "Info"
    }
    
    if ($DeployAppService) {
        Write-ColorOutput "✅ App Service: daena-ai-vp-app" "Success"
        Write-ColorOutput "   Purpose: Production deployment" "Info"
        Write-ColorOutput "   URL: https://daena-ai-vp-app.azurewebsites.net" "Info"
    }
    
    Write-ColorOutput "`n🔧 Next Steps:" "Info"
    Write-ColorOutput "1. Configure environment variables in Azure Key Vault" "Info"
    Write-ColorOutput "2. Deploy your code to the App Service" "Info"
    Write-ColorOutput "3. Set up CI/CD pipeline with GitHub Actions" "Info"
    Write-ColorOutput "4. Monitor with Azure Application Insights" "Info"
}

# Main execution
try {
    Write-ColorOutput "🚀 Daena AI VP - Azure Deployment" "Header"
    Write-ColorOutput "=================================" "Header"
    Write-ColorOutput "Resource Group: $ResourceGroup" "Info"
    Write-ColorOutput "Location: $Location" "Info"
    Write-ColorOutput "Deploy VM: $DeployVM" "Info"
    Write-ColorOutput "Deploy App Service: $DeployAppService" "Info"
    Write-ColorOutput ""
    
    # Check prerequisites
    if (!(Test-AzureCLI)) { exit 1 }
    if (!(Test-AzureLogin)) { exit 1 }
    
    # Create resource group
    New-ResourceGroup
    
    # Create storage account
    New-StorageAccount
    
    # Deploy VM if requested
    if ($DeployVM) {
        New-GPUVM
    }
    
    # Deploy App Service if requested
    if ($DeployAppService) {
        New-AppService
    }
    
    # Show summary
    Show-DeploymentSummary
    
    Write-ColorOutput "`n🎯 Deployment completed successfully!" "Success"
}
catch {
    Write-ColorOutput "❌ Deployment failed: $_" "Error"
    exit 1
} 