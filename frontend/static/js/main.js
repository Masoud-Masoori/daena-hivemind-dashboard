/**
 * Daena AI VP System - Main JavaScript
 * Production-ready utilities and HTMX enhancements
 */

// Global configuration
const DAENA_CONFIG = {
    API_BASE_URL: '/api/v1',
    REFRESH_INTERVAL: 30000, // 30 seconds
    WEBSOCKET_URL: 'ws://localhost:8000/ws',
    DEBUG: false
};

// Utility functions
const DaenaUtils = {
    /**
     * Format date to human-readable format
     */
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    /**
     * Format relative time (e.g., "2 hours ago")
     */
    formatRelativeTime(date) {
        const now = new Date();
        const diff = now - new Date(date);
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    },

    /**
     * Show notification
     */
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, duration);
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Make API request with error handling
     */
    async apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${DAENA_CONFIG.API_BASE_URL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': localStorage.getItem('daena_api_key') || 'test-api-key',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            DaenaUtils.showNotification(`API Error: ${error.message}`, 'error');
            throw error;
        }
    },

    /**
     * Update system status
     */
    async updateSystemStatus() {
        try {
            const status = await DaenaUtils.apiRequest('/system/metrics');
            this.updateStatusDisplay(status);
        } catch (error) {
            console.error('Failed to update system status:', error);
        }
    },

    /**
     * Update status display
     */
    updateStatusDisplay(status) {
        const statusElements = document.querySelectorAll('[data-status]');
        statusElements.forEach(element => {
            const key = element.dataset.status;
            if (status[key] !== undefined) {
                element.textContent = status[key];
            }
        });
    }
};

// HTMX Enhancements
document.addEventListener('htmx:beforeRequest', function(event) {
    // Show loading state
    const target = event.target;
    if (target) {
        target.classList.add('loading');
    }
});

document.addEventListener('htmx:afterRequest', function(event) {
    // Hide loading state
    const target = event.target;
    if (target) {
        target.classList.remove('loading');
    }

    // Handle errors
    if (event.detail.xhr.status >= 400) {
        DaenaUtils.showNotification(`Request failed: ${event.detail.xhr.statusText}`, 'error');
    }
});

document.addEventListener('htmx:responseError', function(event) {
    DaenaUtils.showNotification(`Server error: ${event.detail.xhr.statusText}`, 'error');
});

// Agent Management
const AgentManager = {
    /**
     * Toggle agent voice
     */
    async toggleVoice(agentId, enabled) {
        try {
            const response = await DaenaUtils.apiRequest(`/agents/${agentId}/voice-toggle`, {
                method: 'POST',
                body: JSON.stringify({ enabled })
            });
            
            DaenaUtils.showNotification(
                `Agent voice ${enabled ? 'enabled' : 'disabled'}`, 
                'success'
            );
            
            // Refresh agents list
            htmx.trigger('#agents-list', 'refreshAgents');
        } catch (error) {
            console.error('Failed to toggle agent voice:', error);
        }
    },

    /**
     * Update agent task
     */
    async updateTask(agentId, task) {
        try {
            const response = await DaenaUtils.apiRequest(`/agents/${agentId}/update-task`, {
                method: 'POST',
                body: JSON.stringify({ task })
            });
            
            DaenaUtils.showNotification('Agent task updated', 'success');
            
            // Refresh agents list
            htmx.trigger('#agents-list', 'refreshAgents');
        } catch (error) {
            console.error('Failed to update agent task:', error);
        }
    }
};

// CMP Voting System
const CMPVoting = {
    /**
     * Submit CMP vote
     */
    async submitVote(proposalId, vote, reasoning = '') {
        try {
            const response = await DaenaUtils.apiRequest('/cmp-voting/vote', {
                method: 'POST',
                body: JSON.stringify({
                    proposal_id: proposalId,
                    vote: vote,
                    reasoning: reasoning
                })
            });
            
            DaenaUtils.showNotification('Vote submitted successfully', 'success');
            
            // Refresh CMP list
            htmx.trigger('#cmp-list', 'refreshCMP');
        } catch (error) {
            console.error('Failed to submit vote:', error);
        }
    },

    /**
     * Get voting results
     */
    async getResults(proposalId) {
        try {
            const results = await DaenaUtils.apiRequest(`/cmp-voting/results/${proposalId}`);
            return results;
        } catch (error) {
            console.error('Failed to get voting results:', error);
            return null;
        }
    }
};

// Strategic Meetings
const StrategicMeetings = {
    /**
     * Create new meeting
     */
    async createMeeting(title, description, participants = []) {
        try {
            const response = await DaenaUtils.apiRequest('/strategic-meetings', {
                method: 'POST',
                body: JSON.stringify({
                    title,
                    description,
                    participants
                })
            });
            
            DaenaUtils.showNotification('Meeting created successfully', 'success');
            
            // Refresh meetings list
            htmx.trigger('#strategic-list', 'refreshStrategic');
        } catch (error) {
            console.error('Failed to create meeting:', error);
        }
    },

    /**
     * Join meeting
     */
    async joinMeeting(meetingId) {
        try {
            const response = await DaenaUtils.apiRequest(`/strategic-meetings/${meetingId}/join`, {
                method: 'POST'
            });
            
            DaenaUtils.showNotification('Joined meeting successfully', 'success');
        } catch (error) {
            console.error('Failed to join meeting:', error);
        }
    }
};

// Real-time Updates
class RealTimeManager {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }

    /**
     * Initialize WebSocket connection
     */
    connect() {
        try {
            this.ws = new WebSocket(DAENA_CONFIG.WEBSOCKET_URL);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
                DaenaUtils.showNotification('Real-time updates connected', 'success');
            };
            
            this.ws.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.reconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
        }
    }

    /**
     * Handle incoming messages
     */
    handleMessage(data) {
        switch (data.type) {
            case 'agent_update':
                htmx.trigger('#agents-list', 'refreshAgents');
                break;
            case 'department_update':
                htmx.trigger('#departments-list', 'refreshDepartments');
                break;
            case 'project_update':
                htmx.trigger('#projects-list', 'refreshProjects');
                break;
            case 'cmp_update':
                htmx.trigger('#cmp-list', 'refreshCMP');
                break;
            case 'meeting_update':
                htmx.trigger('#strategic-list', 'refreshStrategic');
                break;
            case 'system_status':
                DaenaUtils.updateStatusDisplay(data.data);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    /**
     * Reconnect with exponential backoff
     */
    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            return;
        }

        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        setTimeout(() => {
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            this.connect();
        }, delay);
    }

    /**
     * Send message
     */
    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        }
    }

    /**
     * Disconnect
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize real-time updates
    if (DAENA_CONFIG.WEBSOCKET_URL) {
        window.realTimeManager = new RealTimeManager();
        window.realTimeManager.connect();
    }

    // Set up auto-refresh
    setInterval(() => {
        DaenaUtils.updateSystemStatus();
    }, DAENA_CONFIG.REFRESH_INTERVAL);

    // Initialize tooltips and other UI enhancements
    initializeUI();
});

// UI Initialization
function initializeUI() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });

    // Initialize modals
    const modalTriggers = document.querySelectorAll('[data-modal]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', openModal);
    });

    // Initialize voice toggles
    const voiceToggles = document.querySelectorAll('.voice-toggle');
    voiceToggles.forEach(toggle => {
        toggle.addEventListener('click', toggleVoice);
    });
}

// Tooltip functions
function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.dataset.tooltip;
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        document.body.removeChild(tooltip);
    }
}

// Modal functions
function openModal(event) {
    const modalId = event.target.dataset.modal;
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Voice toggle function
function toggleVoice(event) {
    const toggle = event.target;
    const agentId = toggle.dataset.agentId;
    const enabled = !toggle.classList.contains('active');
    
    AgentManager.toggleVoice(agentId, enabled);
    toggle.classList.toggle('active', enabled);
}

// Export for global access
window.DaenaUtils = DaenaUtils;
window.AgentManager = AgentManager;
window.CMPVoting = CMPVoting;
window.StrategicMeetings = StrategicMeetings; 