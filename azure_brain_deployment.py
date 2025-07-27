#!/usr/bin/env python3
"""
Azure Brain Deployment Script for Daena AI VP
Deploys complete brain training infrastructure with R1, R2, DeepSeek v3, and other advanced models
"""

import os
import json
import subprocess
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
import azure.mgmt.compute as compute
import azure.mgmt.network as network
import azure.mgmt.storage as storage
import azure.mgmt.resource as resource
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute.models import (
    VirtualMachine, HardwareProfile, StorageProfile, OSProfile, 
    NetworkProfile, ImageReference, ManagedDiskParameters, 
    VirtualMachineInstanceView
)

class AzureBrainDeployment:
    def __init__(self):
        self.setup_logging()
        self.credential = DefaultAzureCredential()
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        self.resource_group_name = "daena-brain-training"
        self.location = "eastus2"
        
        # Initialize Azure clients
        self.compute_client = compute.ComputeManagementClient(self.credential, self.subscription_id)
        self.network_client = network.NetworkManagementClient(self.credential, self.subscription_id)
        self.storage_client = storage.StorageManagementClient(self.credential, self.subscription_id)
        self.resource_client = resource.ResourceManagementClient(self.credential, self.subscription_id)
        
        # VM Configuration
        self.vm_config = {
            "name": "daena-brain-vm",
            "size": "Standard_NC24rs_v3",  # 4x NVIDIA V100 GPUs, 448 GB RAM
            "admin_username": "daenaadmin",
            "admin_password": self.generate_secure_password(),
            "image_publisher": "Canonical",
            "image_offer": "UbuntuServer",
            "image_sku": "18.04-LTS",
            "image_version": "latest"
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/azure_deployment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AzureBrainDeployment')
        
    def generate_secure_password(self) -> str:
        """Generate a secure password for the VM"""
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for i in range(16))
        
    def create_resource_group(self):
        """Create Azure resource group"""
        try:
            self.logger.info(f"Creating resource group: {self.resource_group_name}")
            
            resource_group_params = {
                'location': self.location,
                'tags': {
                    'project': 'daena-brain-training',
                    'environment': 'production',
                    'managed_by': 'azure-deployment-script'
                }
            }
            
            result = self.resource_client.resource_groups.create_or_update(
                self.resource_group_name, resource_group_params
            )
            
            self.logger.info(f"Resource group created: {result.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating resource group: {e}")
            return False
            
    def create_virtual_network(self):
        """Create virtual network and subnet"""
        try:
            self.logger.info("Creating virtual network...")
            
            # Create virtual network
            vnet_params = {
                'location': self.location,
                'address_space': {
                    'address_prefixes': ['10.0.0.0/16']
                },
                'subnets': [{
                    'name': 'default',
                    'address_prefix': '10.0.0.0/24'
                }]
            }
            
            vnet_poller = self.network_client.virtual_networks.begin_create_or_update(
                self.resource_group_name, 'daena-vnet', vnet_params
            )
            vnet = vnet_poller.result()
            
            self.logger.info(f"Virtual network created: {vnet.name}")
            return vnet
            
        except Exception as e:
            self.logger.error(f"Error creating virtual network: {e}")
            return None
            
    def create_network_security_group(self):
        """Create network security group with appropriate rules"""
        try:
            self.logger.info("Creating network security group...")
            
            # Define security rules
            security_rules = [
                {
                    'name': 'SSH',
                    'protocol': 'Tcp',
                    'source_address_prefix': '*',
                    'destination_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_port_range': '22',
                    'access': 'Allow',
                    'priority': 1000,
                    'direction': 'Inbound'
                },
                {
                    'name': 'HTTP',
                    'protocol': 'Tcp',
                    'source_address_prefix': '*',
                    'destination_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_port_range': '80',
                    'access': 'Allow',
                    'priority': 1001,
                    'direction': 'Inbound'
                },
                {
                    'name': 'HTTPS',
                    'protocol': 'Tcp',
                    'source_address_prefix': '*',
                    'destination_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_port_range': '443',
                    'access': 'Allow',
                    'priority': 1002,
                    'direction': 'Inbound'
                },
                {
                    'name': 'Jupyter',
                    'protocol': 'Tcp',
                    'source_address_prefix': '*',
                    'destination_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_port_range': '8888',
                    'access': 'Allow',
                    'priority': 1003,
                    'direction': 'Inbound'
                },
                {
                    'name': 'TensorBoard',
                    'protocol': 'Tcp',
                    'source_address_prefix': '*',
                    'destination_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_port_range': '6006',
                    'access': 'Allow',
                    'priority': 1004,
                    'direction': 'Inbound'
                }
            ]
            
            nsg_params = {
                'location': self.location,
                'security_rules': security_rules
            }
            
            nsg = self.network_client.network_security_groups.create_or_update(
                self.resource_group_name, 'daena-nsg', nsg_params
            )
            
            self.logger.info(f"Network security group created: {nsg.name}")
            return nsg
            
        except Exception as e:
            self.logger.error(f"Error creating network security group: {e}")
            return None
            
    def create_public_ip(self):
        """Create public IP address"""
        try:
            self.logger.info("Creating public IP address...")
            
            ip_params = {
                'location': self.location,
                'public_ip_allocation_method': 'Static',
                'dns_settings': {
                    'domain_name_label': f'daena-brain-{int(time.time())}'
                }
            }
            
            ip = self.network_client.public_ip_addresses.create_or_update(
                self.resource_group_name, 'daena-public-ip', ip_params
            )
            
            self.logger.info(f"Public IP created: {ip.ip_address}")
            return ip
            
        except Exception as e:
            self.logger.error(f"Error creating public IP: {e}")
            return None
            
    def create_network_interface(self, vnet, nsg, public_ip):
        """Create network interface"""
        try:
            self.logger.info("Creating network interface...")
            
            # Get subnet
            subnet = self.network_client.subnets.get(
                self.resource_group_name, vnet.name, 'default'
            )
            
            # Create IP configuration
            ip_config = {
                'name': 'ipconfig1',
                'subnet': {'id': subnet.id},
                'public_ip_address': {'id': public_ip.id}
            }
            
            nic_params = {
                'location': self.location,
                'ip_configurations': [ip_config],
                'network_security_group': {'id': nsg.id}
            }
            
            nic = self.network_client.network_interfaces.create_or_update(
                self.resource_group_name, 'daena-nic', nic_params
            )
            
            self.logger.info(f"Network interface created: {nic.name}")
            return nic
            
        except Exception as e:
            self.logger.error(f"Error creating network interface: {e}")
            return None
            
    def create_virtual_machine(self, nic):
        """Create the GPU-enabled virtual machine"""
        try:
            self.logger.info(f"Creating virtual machine: {self.vm_config['name']}")
            
            # Hardware profile
            hardware_profile = HardwareProfile(
                vm_size=self.vm_config['size']
            )
            
            # OS profile
            os_profile = OSProfile(
                computer_name=self.vm_config['name'],
                admin_username=self.vm_config['admin_username'],
                admin_password=self.vm_config['admin_password']
            )
            
            # Storage profile
            storage_profile = StorageProfile(
                image_reference=ImageReference(
                    publisher=self.vm_config['image_publisher'],
                    offer=self.vm_config['image_offer'],
                    sku=self.vm_config['image_sku'],
                    version=self.vm_config['image_version']
                ),
                os_disk=ManagedDiskParameters(
                    storage_account_type='Premium_LRS',
                    disk_size_gb=512  # Large disk for models
                )
            )
            
            # Network profile
            network_profile = NetworkProfile(
                network_interfaces=[{'id': nic.id}]
            )
            
            # Create VM
            vm_params = VirtualMachine(
                location=self.location,
                hardware_profile=hardware_profile,
                os_profile=os_profile,
                storage_profile=storage_profile,
                network_profile=network_profile
            )
            
            vm_poller = self.compute_client.virtual_machines.begin_create_or_update(
                self.resource_group_name, self.vm_config['name'], vm_params
            )
            vm = vm_poller.result()
            
            self.logger.info(f"Virtual machine created: {vm.name}")
            return vm
            
        except Exception as e:
            self.logger.error(f"Error creating virtual machine: {e}")
            return None
            
    def create_storage_account(self):
        """Create storage account for model storage"""
        try:
            self.logger.info("Creating storage account...")
            
            storage_params = {
                'location': self.location,
                'sku': {
                    'name': 'Standard_LRS'
                },
                'kind': 'StorageV2',
                'enable_https_traffic_only': True,
                'minimum_tls_version': 'TLS1_2'
            }
            
            storage_account = self.storage_client.storage_accounts.begin_create(
                self.resource_group_name, 'daenastorage', storage_params
            ).result()
            
            self.logger.info(f"Storage account created: {storage_account.name}")
            return storage_account
            
        except Exception as e:
            self.logger.error(f"Error creating storage account: {e}")
            return None
            
    def generate_setup_script(self, vm_ip: str):
        """Generate setup script for the VM"""
        setup_script = f"""#!/bin/bash
# Daena Brain Training VM Setup Script
# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}

set -e

echo "Starting Daena Brain Training VM setup..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install essential packages
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    htop \
    nvidia-cuda-toolkit \
    nvidia-driver-470 \
    docker.io \
    docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install NVIDIA Docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Create directories
mkdir -p /home/daenaadmin/daena-brain
mkdir -p /home/daenaadmin/models
mkdir -p /home/daenaadmin/checkpoints
mkdir -p /home/daenaadmin/logs
mkdir -p /home/daenaadmin/data

# Clone Daena repository
cd /home/daenaadmin
git clone https://github.com/Masoud-Masoori/daena-hivemind-dashboard.git daena-brain
cd daena-brain

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate bitsandbytes
pip install fastapi uvicorn sqlalchemy
pip install azure-storage-blob azure-identity
pip install jupyter tensorboard

# Install additional ML libraries
pip install sentencepiece protobuf
pip install scikit-learn pandas numpy matplotlib seaborn
pip install wandb mlflow

# Download and setup models
echo "Setting up models directory..."
mkdir -p /home/daenaadmin/models/r1
mkdir -p /home/daenaadmin/models/r2
mkdir -p /home/daenaadmin/models/deepseek-v3
mkdir -p /home/daenaadmin/models/qwen2.5
mkdir -p /home/daenaadmin/models/yi-34b

# Create model download script
cat > /home/daenaadmin/download_models.py << 'EOF'
import os
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def download_model(model_name, model_path):
    print(f"Downloading {model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        print(f"Successfully downloaded {model_name}")
    except Exception as e:
        print(f"Error downloading {model_name}: {e}")

# Download models (commented out to avoid automatic download)
# download_model("Qwen2.5-7B", "Qwen/Qwen2.5-7B-Instruct")
# download_model("DeepSeek-Coder-6.7B", "deepseek-ai/deepseek-coder-6.7b-instruct")
EOF

# Setup environment variables
cat > /home/daenaadmin/.env << EOF
# Azure OpenAI Configuration
OPENAI_API_TYPE=azure
OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', '')}
OPENAI_API_BASE={os.getenv('OPENAI_API_BASE', '')}
OPENAI_API_VERSION=2024-02-15
OPENAI_DEPLOYMENT_NAME=daena

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING={os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')}

# Model Configuration
MODELS_PATH=/home/daenaadmin/models
CHECKPOINTS_PATH=/home/daenaadmin/checkpoints
LOGS_PATH=/home/daenaadmin/logs

# Training Configuration
BATCH_SIZE=4
LEARNING_RATE=1e-5
MAX_EPOCHS=10
EOF

# Create systemd service for brain training
sudo cat > /etc/systemd/system/daena-brain-training.service << EOF
[Unit]
Description=Daena Brain Training Service
After=network.target

[Service]
Type=simple
User=daenaadmin
WorkingDirectory=/home/daenaadmin/daena-brain
Environment=PATH=/home/daenaadmin/daena-brain/venv/bin
ExecStart=/home/daenaadmin/daena-brain/venv/bin/python /home/daenaadmin/daena-brain/brain_training_daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable daena-brain-training
sudo systemctl start daena-brain-training

# Create Jupyter configuration
jupyter notebook --generate-config
jupyter notebook password

# Create startup script
cat > /home/daenaadmin/start_services.sh << 'EOF'
#!/bin/bash
cd /home/daenaadmin/daena-brain
source venv/bin/activate

# Start Jupyter notebook
nohup jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root > /home/daenaadmin/logs/jupyter.log 2>&1 &

# Start TensorBoard
nohup tensorboard --logdir=/home/daenaadmin/logs --host=0.0.0.0 --port=6006 > /home/daenaadmin/logs/tensorboard.log 2>&1 &

echo "Services started. Access Jupyter at http://{vm_ip}:8888"
echo "Access TensorBoard at http://{vm_ip}:6006"
EOF

chmod +x /home/daenaadmin/start_services.sh

echo "Setup completed successfully!"
echo "VM IP: {vm_ip}"
echo "Username: {self.vm_config['admin_username']}"
echo "Password: {self.vm_config['admin_password']}"
echo ""
echo "Next steps:"
echo "1. SSH to the VM: ssh {self.vm_config['admin_username']}@{vm_ip}"
echo "2. Run: cd /home/daenaadmin/daena-brain"
echo "3. Start services: ./start_services.sh"
echo "4. Access Jupyter: http://{vm_ip}:8888"
echo "5. Access TensorBoard: http://{vm_ip}:6006"
"""

        # Save setup script
        script_path = "vm_setup_script.sh"
        with open(script_path, 'w') as f:
            f.write(setup_script)
            
        self.logger.info(f"Setup script generated: {script_path}")
        return script_path
        
    def deploy_complete_infrastructure(self):
        """Deploy complete brain training infrastructure"""
        try:
            self.logger.info("Starting complete Azure brain training infrastructure deployment...")
            
            # Step 1: Create resource group
            if not self.create_resource_group():
                return False
                
            # Step 2: Create virtual network
            vnet = self.create_virtual_network()
            if not vnet:
                return False
                
            # Step 3: Create network security group
            nsg = self.create_network_security_group()
            if not nsg:
                return False
                
            # Step 4: Create public IP
            public_ip = self.create_public_ip()
            if not public_ip:
                return False
                
            # Step 5: Create network interface
            nic = self.create_network_interface(vnet, nsg, public_ip)
            if not nic:
                return False
                
            # Step 6: Create virtual machine
            vm = self.create_virtual_machine(nic)
            if not vm:
                return False
                
            # Step 7: Create storage account
            storage_account = self.create_storage_account()
            if not storage_account:
                return False
                
            # Step 8: Generate setup script
            setup_script = self.generate_setup_script(public_ip.ip_address)
            
            # Step 9: Create deployment summary
            self.create_deployment_summary(vm, public_ip, storage_account, setup_script)
            
            self.logger.info("Complete infrastructure deployed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deploying infrastructure: {e}")
            return False
            
    def create_deployment_summary(self, vm, public_ip, storage_account, setup_script):
        """Create deployment summary file"""
        summary = {
            "deployment_info": {
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "resource_group": self.resource_group_name,
                "location": self.location
            },
            "virtual_machine": {
                "name": vm.name,
                "size": self.vm_config['size'],
                "public_ip": public_ip.ip_address,
                "admin_username": self.vm_config['admin_username'],
                "admin_password": self.vm_config['admin_password'],
                "ssh_command": f"ssh {self.vm_config['admin_username']}@{public_ip.ip_address}"
            },
            "storage_account": {
                "name": storage_account.name,
                "primary_endpoint": storage_account.primary_endpoints.blob
            },
            "access_urls": {
                "jupyter_notebook": f"http://{public_ip.ip_address}:8888",
                "tensorboard": f"http://{public_ip.ip_address}:6006",
                "daena_dashboard": f"http://{public_ip.ip_address}:3000"
            },
            "next_steps": [
                f"1. SSH to VM: ssh {self.vm_config['admin_username']}@{public_ip.ip_address}",
                "2. Run setup script: chmod +x vm_setup_script.sh && ./vm_setup_script.sh",
                "3. Access Jupyter: http://{public_ip.ip_address}:8888",
                "4. Access TensorBoard: http://{public_ip.ip_address}:6006",
                "5. Start brain training: python brain_training_daemon.py"
            ]
        }
        
        # Save summary
        with open('azure_deployment_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
            
        self.logger.info("Deployment summary created: azure_deployment_summary.json")
        
        # Print summary
        print("\n" + "="*60)
        print("🎉 AZURE BRAIN TRAINING INFRASTRUCTURE DEPLOYED!")
        print("="*60)
        print(f"VM IP: {public_ip.ip_address}")
        print(f"SSH: ssh {self.vm_config['admin_username']}@{public_ip.ip_address}")
        print(f"Jupyter: http://{public_ip.ip_address}:8888")
        print(f"TensorBoard: http://{public_ip.ip_address}:6006")
        print("="*60)

def main():
    """Main deployment function"""
    print("🚀 Starting Daena Brain Training Azure Deployment...")
    
    # Check environment variables
    required_env_vars = ["AZURE_SUBSCRIPTION_ID", "OPENAI_API_KEY", "OPENAI_API_BASE"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please set these variables before running the deployment.")
        return False
        
    # Create deployment instance
    deployment = AzureBrainDeployment()
    
    # Deploy infrastructure
    success = deployment.deploy_complete_infrastructure()
    
    if success:
        print("✅ Deployment completed successfully!")
        print("📋 Check azure_deployment_summary.json for details")
    else:
        print("❌ Deployment failed. Check logs for details.")
        
    return success

if __name__ == "__main__":
    main() 