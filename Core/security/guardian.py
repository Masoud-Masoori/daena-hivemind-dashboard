import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional
from memory.secure_recall import log_event

class SecurityGuardian:
    def __init__(self):
        self.security_log = "D:/Ideas/Daena/logs/security.log"
        self.audit_log = "D:/Ideas/Daena/logs/audit.log"
        self.setup_logging()

    def setup_logging(self):
        """Configure security logging."""
        logging.basicConfig(
            filename=self.security_log,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for secure storage."""
        return hashlib.sha256(data.encode()).hexdigest()

    def verify_integrity(self, file_path: str) -> bool:
        """Verify file integrity using checksums."""
        try:
            if not os.path.exists(file_path):
                return False

            with open(file_path, 'rb') as f:
                content = f.read()
                checksum = hashlib.sha256(content).hexdigest()

            # Store or verify checksum
            checksum_file = f"{file_path}.checksum"
            if os.path.exists(checksum_file):
                with open(checksum_file, 'r') as f:
                    stored_checksum = f.read().strip()
                return checksum == stored_checksum
            else:
                with open(checksum_file, 'w') as f:
                    f.write(checksum)
                return True
        except Exception as e:
            logging.error(f"Integrity check failed: {str(e)}")
            return False

    def audit_action(self, action: str, user: str, details: Dict):
        """Log security audit events."""
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "user": user,
                "details": details
            }

            with open(self.audit_log, 'a') as f:
                f.write(json.dumps(audit_entry) + '\n')

            log_event("security_guardian", {
                "action": "audit_log",
                "audit_entry": audit_entry
            })
        except Exception as e:
            logging.error(f"Audit logging failed: {str(e)}")

    def monitor_system_health(self) -> Dict:
        """Monitor system health and security metrics."""
        try:
            health_metrics = {
                "timestamp": datetime.now().isoformat(),
                "file_integrity": self.check_critical_files(),
                "memory_usage": self.get_memory_usage(),
                "active_processes": self.get_active_processes(),
                "security_alerts": self.get_security_alerts()
            }

            log_event("security_guardian", {
                "action": "health_check",
                "metrics": health_metrics
            })

            return health_metrics
        except Exception as e:
            logging.error(f"Health monitoring failed: {str(e)}")
            return {}

    def check_critical_files(self) -> List[Dict]:
        """Check integrity of critical system files."""
        critical_files = [
            "D:/Ideas/Daena/Core/cmp/cmp_brain.py",
            "D:/Ideas/Daena/Core/cmp/cmp_decision_gate.py",
            "D:/Ideas/Daena/memory/secure_recall.py"
        ]

        results = []
        for file_path in critical_files:
            results.append({
                "file": file_path,
                "integrity": self.verify_integrity(file_path)
            })
        return results

    def get_memory_usage(self) -> Dict:
        """Get system memory usage metrics."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            }
        except Exception as e:
            logging.error(f"Memory monitoring failed: {str(e)}")
            return {}

    def get_active_processes(self) -> List[Dict]:
        """Get list of active system processes."""
        try:
            import psutil
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return processes
        except Exception as e:
            logging.error(f"Process monitoring failed: {str(e)}")
            return []

    def get_security_alerts(self) -> List[Dict]:
        """Get current security alerts."""
        try:
            alerts = []
            # Implement security alert detection logic
            # This could include:
            # - Suspicious process detection
            # - Unauthorized access attempts
            # - System resource abuse
            # - Network security issues
            return alerts
        except Exception as e:
            logging.error(f"Security alert monitoring failed: {str(e)}")
            return []

    def perform_security_scan(self) -> Dict:
        """Perform comprehensive security scan."""
        try:
            scan_results = {
                "timestamp": datetime.now().isoformat(),
                "system_health": self.monitor_system_health(),
                "file_integrity": self.check_critical_files(),
                "security_alerts": self.get_security_alerts()
            }

            log_event("security_guardian", {
                "action": "security_scan",
                "results": scan_results
            })

            return scan_results
        except Exception as e:
            logging.error(f"Security scan failed: {str(e)}")
            return {} 