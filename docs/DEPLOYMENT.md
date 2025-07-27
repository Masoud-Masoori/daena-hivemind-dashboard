# 🚀 Daena AI VP - Complete Deployment Guide

**Deploy the full Daena AI VP system to GitHub and Azure with GPT-4, voice, and brain training**

## 📋 Prerequisites

### Required Accounts
- [GitHub Account](https://github.com)
- [Azure Account](https://azure.microsoft.com) (with credits)
- [Azure OpenAI Access](https://azure.microsoft.com/en-us/services/openai/)

### Required Software
- [Git](https://git-scm.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Python 3.8+](https://www.python.org/)
- [PowerShell 7+](https://docs.microsoft.com/en-us/powershell/)

## 🔧 Step 1: Environment Configuration

### Azure OpenAI Setup
1. **Create Azure OpenAI Resource**
   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name daena-ai-vp --location eastus2
   
   # Create Azure OpenAI resource
   az cognitiveservices account create \
     --name daena-openai \
     --resource-group daena-ai-vp \
     --location eastus2 \
     --kind OpenAI \
     --sku S0
   ```

2. **Deploy GPT-4 Model**
   - Go to Azure Portal → Azure OpenAI → Model deployments
   - Create deployment named "daena" with GPT-4 model
   - Note your API key and endpoint URL

3. **Configure Environment Variables**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit with your credentials
   nano .env
   ```

### Gmail Setup
1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Security → 2-Step Verification → Turn on

2. **Generate App Password**
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in your `.env` file

## 📦 Step 2: GitHub Repository Setup

### Create Repository
1. **Fork/Create Repository**
   ```bash
   # Clone the repository
   git clone https://github.com/Masoud-Masoori/daena-hivemind-dashboard.git
   cd daena-hivemind-dashboard
   
   # Add your changes
   git add .
   git commit -m "Initial Daena AI VP setup"
   git push origin main
   ```

### Configure GitHub Secrets
1. **Go to Repository Settings → Secrets and variables → Actions**
2. **Add the following secrets:**
   ```
   AZURE_CREDENTIALS: Your Azure service principal JSON
   AZURE_WEBAPP_PUBLISH_PROFILE: App Service publish profile
   OPENAI_API_KEY: Your Azure OpenAI API key
   OPENAI_API_BASE: Your Azure OpenAI endpoint
   GMAIL_USER: masoud.masoori@gmail.com
   GMAIL_APP_PASSWORD: Your Gmail app password
   VM_HOST: Your Azure VM IP address
   VM_USERNAME: azureuser
   VM_SSH_KEY: Your VM SSH private key
   ```

## 🌐 Step 3: Azure Deployment

### Option A: Automated Deployment (Recommended)

1. **Run Azure Deployment Script**
   ```powershell
   # Deploy both VM and App Service
   .\azure-deploy.ps1 -ResourceGroup "daena-ai-vp" -DeployVM -DeployAppService
   ```

2. **Verify Deployment**
   ```bash
   # Check App Service
   az webapp show --name daena-ai-vp-app --resource-group daena-ai-vp
   
   # Check VM
   az vm show --name daena-brain-vm --resource-group daena-ai-vp
   ```

### Option B: Manual Deployment

#### Deploy App Service
```bash
# Create App Service Plan
az appservice plan create \
  --resource-group daena-ai-vp \
  --name daena-app-plan \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group daena-ai-vp \
  --plan daena-app-plan \
  --name daena-ai-vp-app \
  --runtime "PYTHON:3.9"

# Configure environment variables
az webapp config appsettings set \
  --resource-group daena-ai-vp \
  --name daena-ai-vp-app \
  --settings \
  OPENAI_API_TYPE=azure \
  OPENAI_API_KEY=your_key \
  OPENAI_API_BASE=your_endpoint \
  OPENAI_API_VERSION=2024-02-15 \
  OPENAI_DEPLOYMENT_NAME=daena \
  GMAIL_USER=masoud.masoori@gmail.com \
  GMAIL_APP_PASSWORD=your_password \
  DEMO_MODE=production
```

#### Deploy GPU VM
```bash
# Create VM with GPU
az vm create \
  --resource-group daena-ai-vp \
  --name daena-brain-vm \
  --image Ubuntu2204 \
  --size Standard_NC6 \
  --admin-username azureuser \
  --generate-ssh-keys

# Get VM IP
VM_IP=$(az vm show --resource-group daena-ai-vp --name daena-brain-vm --show-details --query "publicIps" --output tsv)

# SSH to VM and setup
ssh azureuser@$VM_IP
```

## 🧠 Step 4: Brain Training Setup

### On Azure VM
```bash
# Connect to VM
ssh azureuser@your-vm-ip

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
nano .env  # Edit with your credentials

# Launch with brain training
./launch_daena.ps1 -Mode azure-vm -EnableBrainTraining -EnableVoice -EnableCMP
```

### Training Data Preparation
```bash
# Create training data directories
mkdir -p data/training
mkdir -p memory/knowledge
mkdir -p models/brain_checkpoints

# Add your training data
cp your-company-docs/* data/training/
cp investor-info/* memory/knowledge/
```

## 🎤 Step 5: Voice System Setup

### Install Voice Dependencies
```bash
# On VM or local machine
pip install TTS torch torchaudio librosa soundfile

# Download XTTS model
mkdir -p models/xtts_v2
# Download XTTS v2 model files to models/xtts_v2/
```

### Configure Voice Settings
```bash
# Edit .env file
XTTS_MODEL_PATH=./models/xtts_v2
VOICE_OUTPUT_DIR=./voice/output
VOICE_CACHE_DIR=./voice/cache
```

## 🗳️ Step 6: CMP Decision Engine

### Enable CMP System
```bash
# Edit .env file
CMP_DATABASE_PATH=./data/cmp_decisions
VOTING_ENGINE_ENABLED=true
FOUNDER_OVERRIDE_ENABLED=true

# Launch with CMP enabled
./launch_daena.ps1 -EnableCMP
```

## 🚀 Step 7: Launch Complete System

### Local Development
```powershell
# Launch with all features
.\launch_daena.ps1 -Mode local -EnableVoice -EnableCMP -EnableBrainTraining
```

### Production Deployment
```powershell
# Launch on Azure VM
.\launch_daena.ps1 -Mode azure-vm -EnableVoice -EnableCMP -EnableBrainTraining
```

### App Service Deployment
```bash
# Deploy via GitHub Actions (automatic)
git push origin main

# Or manual deployment
az webapp deployment source config-zip \
  --resource-group daena-ai-vp \
  --name daena-ai-vp-app \
  --src daena-backend.zip
```

## 📊 Step 8: Monitoring & Verification

### Health Checks
```bash
# App Service health
curl https://daena-ai-vp-app.azurewebsites.net/health

# VM health
curl http://your-vm-ip:3000/health

# Local health
curl http://localhost:3000/health
```

### Access Points
- **Production Dashboard**: https://daena-ai-vp-app.azurewebsites.net/demo
- **API Documentation**: https://daena-ai-vp-app.azurewebsites.net/docs
- **VM Dashboard**: http://your-vm-ip:3000/demo
- **Local Dashboard**: http://localhost:3000/demo

### Monitoring Setup
```bash
# Enable Application Insights
az monitor app-insights component create \
  --app daena-insights \
  --location eastus2 \
  --resource-group daena-ai-vp \
  --application-type web

# Configure monitoring
az webapp config appsettings set \
  --resource-group daena-ai-vp \
  --name daena-ai-vp-app \
  --settings \
  APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string
```

## 🔒 Step 9: Security Configuration

### Azure Key Vault Setup
```bash
# Create Key Vault
az keyvault create \
  --name daena-vault \
  --resource-group daena-ai-vp \
  --location eastus2

# Store secrets
az keyvault secret set --vault-name daena-vault --name openai-key --value "your_key"
az keyvault secret set --vault-name daena-vault --name gmail-password --value "your_password"

# Configure App Service to use Key Vault
az webapp config appsettings set \
  --resource-group daena-ai-vp \
  --name daena-ai-vp-app \
  --settings \
  OPENAI_API_KEY="@Microsoft.KeyVault(SecretUri=https://daena-vault.vault.azure.net/secrets/openai-key/)"
```

### Network Security
```bash
# Configure NSG for VM
az network nsg rule create \
  --resource-group daena-ai-vp \
  --nsg-name daena-brain-vmNSG \
  --name allow-ssh \
  --protocol tcp \
  --priority 1000 \
  --destination-port-range 22

az network nsg rule create \
  --resource-group daena-ai-vp \
  --nsg-name daena-brain-vmNSG \
  --name allow-daena \
  --protocol tcp \
  --priority 1001 \
  --destination-port-range 3000
```

## 🧪 Step 10: Testing

### Run Test Suite
```bash
# Comprehensive testing
python test_demo.py

# Individual component tests
pytest tests/ -v

# Performance testing
python -m pytest tests/test_performance.py -v
```

### Demo Scenarios
1. **Investor Outreach**
   - Ask: "Generate an email for Toronto AI investors"
   - Verify email generation and sending

2. **Voice Interaction**
   - Click microphone button
   - Say: "Hey Daena, tell me about our Series A plans"
   - Verify voice response

3. **CMP Decision Making**
   - Submit decision for voting
   - Verify consensus mechanism

## 🔧 Troubleshooting

### Common Issues

**Azure OpenAI 404 Error**
```bash
# Check deployment name
az cognitiveservices account deployment list \
  --resource-group daena-ai-vp \
  --name daena-openai

# Verify API key and endpoint
curl -H "api-key: your_key" \
  "https://your-endpoint.openai.azure.com/openai/deployments/daena/chat/completions?api-version=2024-02-15"
```

**Gmail Authentication Error**
```bash
# Verify app password
# Check 2FA is enabled
# Ensure less secure apps is disabled
```

**VM Connection Issues**
```bash
# Check VM status
az vm show --resource-group daena-ai-vp --name daena-brain-vm

# Reset VM if needed
az vm restart --resource-group daena-ai-vp --name daena-brain-vm
```

### Logs and Debugging
```bash
# App Service logs
az webapp log tail --name daena-ai-vp-app --resource-group daena-ai-vp

# VM logs
ssh azureuser@your-vm-ip "tail -f /var/log/syslog"

# Local logs
tail -f logs/daena.log
```

## 📈 Step 11: Scaling & Optimization

### Performance Optimization
```bash
# Enable auto-scaling for App Service
az monitor autoscale create \
  --resource-group daena-ai-vp \
  --resource daena-app-plan \
  --resource-type Microsoft.Web/serverfarms \
  --name daena-autoscale \
  --min-count 1 \
  --max-count 10 \
  --count 2
```

### Cost Optimization
```bash
# Use Azure Reserved Instances for VM
az vm reservation create \
  --resource-group daena-ai-vp \
  --reservation-order-id your_order_id \
  --reservation-id your_reservation_id
```

## 🎯 Success Indicators

### ✅ Working System
- Dashboard loads at all access points
- Chat responds intelligently with GPT-4
- Voice system functions properly
- Email generation and sending works
- CMP decision engine operational
- Brain training active on VM

### 📊 Performance Metrics
- Response time < 2 seconds
- Voice recognition accuracy > 90%
- Email generation success > 95%
- System uptime > 99%
- Azure OpenAI token usage tracked

## 🚀 Next Steps

1. **Set up CI/CD pipeline** with GitHub Actions
2. **Configure monitoring** with Application Insights
3. **Implement backup strategy** for models and data
4. **Set up alerting** for system health
5. **Plan scaling strategy** for production load

---

**🎉 Congratulations! Your Daena AI VP system is now fully deployed and operational!**

**🌐 [Live Demo](https://daena-ai-vp-app.azurewebsites.net/demo) | 📊 [API Docs](https://daena-ai-vp-app.azurewebsites.net/docs) | 🧪 [Run Tests](python test_demo.py)** 