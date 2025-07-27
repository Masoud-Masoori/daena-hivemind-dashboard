import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

class DaenaInitializer:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = self._setup_logging()
        self.configs = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("daena")
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "daena.log")
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(levelname)s: %(message)s')
        )
        logger.addHandler(console_handler)
        
        return logger
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load a configuration file."""
        config_path = self.config_dir / f"{config_name}.json"
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize the Daena system by loading all configurations."""
        try:
            # Load system configuration
            self.configs['system'] = self.load_config('system')
            
            # Create necessary directories
            self._create_directories()
            
            # Load other configurations
            self.configs['voice'] = self.load_config('voice')
            self.configs['agents'] = self.load_config('agents')
            self.configs['models'] = self.load_config('models')
            
            # Initialize components
            self._initialize_components()
            
            self.logger.info("Daena system initialized successfully")
            return self.configs
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Daena system: {e}")
            raise
    
    def _create_directories(self) -> None:
        """Create necessary directories based on system configuration."""
        dirs = [
            self.configs['system']['environment']['data_dir'],
            self.configs['system']['environment']['cache_dir'],
            self.configs['system']['environment']['logs_dir'],
            self.configs['system']['backup']['backup_dir']
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {dir_path}")
    
    def _initialize_components(self) -> None:
        """Initialize system components based on configurations."""
        # Initialize model integration
        from Core.llm.model_integration import ModelIntegration
        self.model_integration = ModelIntegration(self.configs['models'])
        
        # Initialize voice system
        from Core.voice.tts import DaenaTTS
        self.tts = DaenaTTS(self.configs['voice'])
        
        # Initialize agent system
        from Core.agents.psychological_techniques import PsychologicalTechniques
        self.psychological_techniques = PsychologicalTechniques(self.configs['agents'])
        
        # Initialize consultation system
        from Core.agents.daena_consultation import DaenaConsultation
        self.consultation = DaenaConsultation(self.configs['agents'])

def initialize_daena() -> DaenaInitializer:
    """Initialize the Daena system and return the initializer instance."""
    initializer = DaenaInitializer()
    initializer.initialize()
    return initializer

if __name__ == "__main__":
    # Initialize Daena when run directly
    daena = initialize_daena() 