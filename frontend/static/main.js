// Daena AI VP System - Frontend JavaScript
// Sunflower Dashboard with Real-time Chat Integration

document.addEventListener('alpine:init', () => {
    
    // Main Dashboard Data
    Alpine.data('founderDashboard', () => ({
        // Chat System
        chatOpen: false,
        chatInput: '',
        chatMessages: [
            {
                id: 1,
                type: 'assistant',
                content: 'Hello! I\'m Daena, your AI VP. I\'m monitoring all your departments and projects. How can I assist you today?',
                timestamp: new Date().toISOString()
            }
        ],
        chatWebSocket: null,
        
        // Dashboard State
        selectedDepartment: null,
        selectedProject: null,
        
        // System Metrics
        metrics: {
            agents_count: 24,
            departments_count: 8, 
            projects_count: 15,
            monthly_revenue: '125K',
            uptime: '99.9%',
            active_conversations: 0
        },
        
        // Department Data - Sunflower Petals
        departments: [
            { 
                id: 'engineering', 
                name: 'Engineering', 
                icon: 'fas fa-code', 
                status: 'Active Development', 
                active: true, 
                agents: 6,
                completion: 78,
                description: 'Building core platform features and maintaining infrastructure',
                color: 'from-blue-500 to-blue-700',
                agentList: [
                    { id: 'eng1', name: 'CodeMaster AI', status: 'active', task: 'API development', efficiency: 95 },
                    { id: 'eng2', name: 'DevOps Agent', status: 'active', task: 'CI/CD pipeline', efficiency: 88 },
                    { id: 'eng3', name: 'QA Tester', status: 'active', task: 'Test automation', efficiency: 92 },
                    { id: 'eng4', name: 'Security Scanner', status: 'monitoring', task: 'Vulnerability scan', efficiency: 85 },
                    { id: 'eng5', name: 'Database AI', status: 'active', task: 'Query optimization', efficiency: 90 },
                    { id: 'eng6', name: 'Frontend Bot', status: 'active', task: 'UI components', efficiency: 87 }
                ]
            },
            { 
                id: 'marketing', 
                name: 'Marketing', 
                icon: 'fas fa-bullhorn', 
                status: 'Campaign Running', 
                active: true, 
                agents: 4,
                completion: 65,
                description: 'Managing campaigns, content creation, and brand presence',
                color: 'from-pink-500 to-red-500',
                agentList: [
                    { id: 'mkt1', name: 'Content Creator', status: 'active', task: 'Blog writing', efficiency: 91 },
                    { id: 'mkt2', name: 'Social Media AI', status: 'active', task: 'Social posting', efficiency: 94 },
                    { id: 'mkt3', name: 'SEO Optimizer', status: 'active', task: 'Keyword analysis', efficiency: 89 },
                    { id: 'mkt4', name: 'Ad Manager', status: 'active', task: 'Campaign optimization', efficiency: 86 }
                ]
            },
            { 
                id: 'sales', 
                name: 'Sales', 
                icon: 'fas fa-chart-line', 
                status: 'Lead Conversion', 
                active: true, 
                agents: 3,
                completion: 82,
                description: 'Lead generation, qualification, and deal closing',
                color: 'from-green-500 to-emerald-600',
                agentList: [
                    { id: 'sal1', name: 'Lead Hunter', status: 'active', task: 'Prospect outreach', efficiency: 88 },
                    { id: 'sal2', name: 'Deal Closer', status: 'active', task: 'Follow-up calls', efficiency: 93 },
                    { id: 'sal3', name: 'Pipeline Manager', status: 'active', task: 'CRM updates', efficiency: 91 }
                ]
            },
            { 
                id: 'finance', 
                name: 'Finance', 
                icon: 'fas fa-dollar-sign', 
                status: 'Budget Analysis', 
                active: true, 
                agents: 2,
                completion: 90,
                description: 'Financial planning, analysis, and reporting',
                color: 'from-yellow-500 to-orange-500',
                agentList: [
                    { id: 'fin1', name: 'Budget Analyzer', status: 'active', task: 'Expense tracking', efficiency: 96 },
                    { id: 'fin2', name: 'Revenue Forecaster', status: 'active', task: 'Revenue projection', efficiency: 92 }
                ]
            },
            { 
                id: 'hr', 
                name: 'Human Resources', 
                icon: 'fas fa-users', 
                status: 'Talent Acquisition', 
                active: true, 
                agents: 2,
                completion: 55,
                description: 'Talent acquisition, employee management, and culture building',
                color: 'from-purple-500 to-indigo-600',
                agentList: [
                    { id: 'hr1', name: 'Recruiter AI', status: 'active', task: 'Candidate screening', efficiency: 89 },
                    { id: 'hr2', name: 'Culture Bot', status: 'active', task: 'Employee engagement', efficiency: 85 }
                ]
            },
            { 
                id: 'customer_success', 
                name: 'Customer Success', 
                icon: 'fas fa-heart', 
                status: 'Support Active', 
                active: true, 
                agents: 3,
                completion: 88,
                description: 'Customer support, satisfaction, and retention',
                color: 'from-teal-500 to-cyan-600',
                agentList: [
                    { id: 'cs1', name: 'Support Bot', status: 'active', task: 'Ticket resolution', efficiency: 94 },
                    { id: 'cs2', name: 'Success Manager', status: 'active', task: 'Customer onboarding', efficiency: 87 },
                    { id: 'cs3', name: 'Feedback Analyzer', status: 'active', task: 'Sentiment analysis', efficiency: 91 }
                ]
            },
            { 
                id: 'product', 
                name: 'Product', 
                icon: 'fas fa-lightbulb', 
                status: 'Feature Planning', 
                active: true, 
                agents: 3,
                completion: 45,
                description: 'Product strategy, roadmap, and feature development',
                color: 'from-rose-500 to-pink-600',
                agentList: [
                    { id: 'prd1', name: 'Strategy AI', status: 'active', task: 'Roadmap planning', efficiency: 90 },
                    { id: 'prd2', name: 'UX Research', status: 'active', task: 'User interviews', efficiency: 88 },
                    { id: 'prd3', name: 'Feature Validator', status: 'active', task: 'A/B testing', efficiency: 85 }
                ]
            },
            { 
                id: 'operations', 
                name: 'Operations', 
                icon: 'fas fa-cogs', 
                status: 'Process Optimization', 
                active: true, 
                agents: 2,
                completion: 72,
                description: 'Process optimization, automation, and operational efficiency',
                color: 'from-slate-500 to-gray-600',
                agentList: [
                    { id: 'ops1', name: 'Process Optimizer', status: 'active', task: 'Workflow automation', efficiency: 93 },
                    { id: 'ops2', name: 'Efficiency Monitor', status: 'active', task: 'Performance tracking', efficiency: 89 }
                ]
            }
        ],
        
        // Active Projects
        projects: [
            { id: 'p1', name: 'Q4 Revenue Optimization', completion: 65, status: 'on-track', priority: 'high', owner: 'Marketing & Sales' },
            { id: 'p2', name: 'Team Expansion Planning', completion: 40, status: 'planning', priority: 'medium', owner: 'HR & Finance' },
            { id: 'p3', name: 'Product Launch Strategy', completion: 25, status: 'design', priority: 'high', owner: 'Product & Engineering' },
            { id: 'p4', name: 'Customer Retention Program', completion: 80, status: 'testing', priority: 'medium', owner: 'Customer Success' },
            { id: 'p5', name: 'AI Integration Enhancement', completion: 90, status: 'deployment', priority: 'high', owner: 'Engineering' },
            { id: 'p6', name: 'Market Analysis Campaign', completion: 35, status: 'research', priority: 'low', owner: 'Marketing' }
        ],
        
        // System Initialization
        init() {
            console.log('🌻 Initializing Daena AI VP Dashboard');
            this.loadSystemMetrics();
            this.connectWebSocket();
            this.startRealTimeUpdates();
        },
        
        // WebSocket Connection
        connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
            
            this.chatWebSocket = new WebSocket(wsUrl);
            
            this.chatWebSocket.onopen = () => {
                console.log('🔌 Connected to Daena VP WebSocket');
                this.addSystemMessage('Connected to Daena VP - Real-time communication active');
            };
            
            this.chatWebSocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'assistant') {
                        this.chatMessages.push({
                            id: Date.now(),
                            type: 'assistant',
                            content: data.message,
                            timestamp: data.timestamp || new Date().toISOString(),
                            insights: data.department_insights,
                            projects: data.project_updates
                        });
                        this.scrollChatToBottom();
                        
                        // Update metrics if provided
                        if (data.department_insights) {
                            this.updateDepartmentInsights(data.department_insights);
                        }
                    }
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.chatWebSocket.onclose = () => {
                console.log('❌ Disconnected from Daena VP - attempting reconnect...');
                this.addSystemMessage('Connection lost - attempting to reconnect...');
                setTimeout(() => this.connectWebSocket(), 3000);
            };
            
            this.chatWebSocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.addSystemMessage('Communication error occurred');
            };
        },
        
        // Chat Functions
        toggleDaenaChat() {
            this.chatOpen = !this.chatOpen;
            if (this.chatOpen) {
                setTimeout(() => this.scrollChatToBottom(), 100);
                this.metrics.active_conversations++;
            } else {
                this.metrics.active_conversations = Math.max(0, this.metrics.active_conversations - 1);
            }
        },
        
        sendMessage() {
            if (!this.chatInput.trim()) return;
            
            // Add user message
            this.chatMessages.push({
                id: Date.now(),
                type: 'user',
                content: this.chatInput,
                timestamp: new Date().toISOString()
            });
            
            // Send to WebSocket
            if (this.chatWebSocket && this.chatWebSocket.readyState === WebSocket.OPEN) {
                const payload = {
                    message: this.chatInput,
                    context: {
                        selectedDepartment: this.selectedDepartment?.name,
                        currentPage: 'dashboard',
                        activeProjects: this.projects.filter(p => p.status !== 'completed').length,
                        systemMetrics: this.metrics
                    }
                };
                
                this.chatWebSocket.send(JSON.stringify(payload));
            } else {
                // Fallback to REST API
                this.sendMessageViaAPI();
            }
            
            this.chatInput = '';
            this.scrollChatToBottom();
        },
        
        async sendMessageViaAPI() {
            try {
                const response = await fetch('/api/v1/daena/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: this.chatInput,
                        user_id: 'founder',
                        context: {
                            selectedDepartment: this.selectedDepartment?.name,
                            currentPage: 'dashboard'
                        }
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    this.chatMessages.push({
                        id: Date.now(),
                        type: 'assistant',
                        content: data.response,
                        timestamp: data.timestamp
                    });
                    this.scrollChatToBottom();
                }
            } catch (error) {
                console.error('API chat error:', error);
                this.addSystemMessage('Failed to send message via API');
            }
        },
        
        quickQuestion(question) {
            this.chatInput = question;
            this.sendMessage();
        },
        
        addSystemMessage(message) {
            this.chatMessages.push({
                id: Date.now(),
                type: 'system',
                content: message,
                timestamp: new Date().toISOString()
            });
            this.scrollChatToBottom();
        },
        
        scrollChatToBottom() {
            setTimeout(() => {
                if (this.$refs.chatMessages) {
                    this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
                }
            }, 100);
        },
        
        // Department Functions
        selectDepartment(dept) {
            this.selectedDepartment = dept;
            console.log(`📁 Selected department: ${dept.name}`);
        },
        
        askDaenaAboutDepartment(dept) {
            const question = `Tell me about the ${dept.name} department status, current projects, and agent performance`;
            this.chatInput = question;
            this.sendMessage();
            if (!this.chatOpen) this.toggleDaenaChat();
        },
        
        // Project Functions
        viewProject(project) {
            this.selectedProject = project;
            const question = `Show me detailed information about the "${project.name}" project including progress, blockers, and next steps`;
            this.chatInput = question;
            this.sendMessage();
            if (!this.chatOpen) this.toggleDaenaChat();
        },
        
        // Layout Functions - Sunflower Pattern
        getSunflowerPosition(index) {
            // Fibonacci spiral positioning for perfect sunflower pattern
            const goldenAngle = 137.508; // Golden angle in degrees
            const angle = index * goldenAngle;
            const radius = Math.sqrt(index + 1) * 60 + 280; // Spiral outward from center
            
            const x = Math.cos(angle * Math.PI / 180) * radius;
            const y = Math.sin(angle * Math.PI / 180) * radius;
            
            return `transform: translate(${x}px, ${y}px); animation-delay: ${index * 0.1}s;`;
        },
        
        getOrbitPosition(index, total) {
            const angle = (index / total) * 360 + (Date.now() / 50) % 360; // Slow rotation
            const radius = 320;
            const x = Math.cos(angle * Math.PI / 180) * radius;
            const y = Math.sin(angle * Math.PI / 180) * radius;
            
            return `transform: translate(calc(50vw + ${x}px), calc(50vh + ${y}px));`;
        },
        
        // Data Loading Functions
        async loadSystemMetrics() {
            try {
                // Load Daena status
                const daenaResponse = await fetch('/api/v1/daena/status');
                if (daenaResponse.ok) {
                    const daenaData = await daenaResponse.json();
                    this.metrics.agents_count = daenaData.departments_managed * 3; // Estimate
                    this.metrics.uptime = '99.9%';
                }
                
                // Load other metrics
                const promises = [
                    fetch('/api/v1/agents/').catch(() => null),
                    fetch('/api/v1/departments/').catch(() => null),
                    fetch('/api/v1/projects/').catch(() => null)
                ];
                
                const [agentsResponse, departmentsResponse, projectsResponse] = await Promise.all(promises);
                
                if (agentsResponse && agentsResponse.ok) {
                    const agentsData = await agentsResponse.json();
                    this.metrics.agents_count = agentsData.total || this.departments.reduce((sum, d) => sum + d.agents, 0);
                }
                
                if (departmentsResponse && departmentsResponse.ok) {
                    const deptsData = await departmentsResponse.json();
                    this.metrics.departments_count = deptsData.total || this.departments.length;
                }
                
                if (projectsResponse && projectsResponse.ok) {
                    const projectsData = await projectsResponse.json();
                    this.metrics.projects_count = projectsData.total || this.projects.length;
                }
                
                console.log('📊 System metrics updated');
            } catch (error) {
                console.log('📊 Using default metrics - API connection pending');
            }
        },
        
        updateDepartmentInsights(insights) {
            // Update department data with real insights from Daena
            Object.keys(insights).forEach(deptKey => {
                const dept = this.departments.find(d => d.id === deptKey);
                if (dept && insights[deptKey]) {
                    const insight = insights[deptKey];
                    dept.status = insight.status || dept.status;
                    dept.completion = insight.completion || dept.completion;
                    if (insight.team_size) dept.agents = insight.team_size;
                }
            });
        },
        
        startRealTimeUpdates() {
            // Update metrics every 30 seconds
            setInterval(() => {
                this.loadSystemMetrics();
            }, 30000);
            
            // Rotate project positions every 5 seconds for dynamic effect
            setInterval(() => {
                this.$nextTick(() => {
                    // Trigger re-render of project positions
                    this.projects = [...this.projects];
                });
            }, 5000);
        },
        
        // CMP (Consensus Management Protocol) Functions
        getCMPVote(issue) {
            const question = `I need your recommendation on: ${issue}. Please analyze this and provide your VP-level decision with reasoning.`;
            this.chatInput = question;
            this.sendMessage();
            if (!this.chatOpen) this.toggleDaenaChat();
        },
        
        // File Upload/Download Functions
        async uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/v1/files/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    this.addSystemMessage(`File uploaded successfully: ${result.filename}`);
                    this.quickQuestion(`Analyze the uploaded file: ${result.filename}`);
                }
            } catch (error) {
                console.error('Upload error:', error);
                this.addSystemMessage('File upload failed');
            }
        }
    }));
    
    // Initialize global Alpine components
    console.log('🚀 Daena AI VP System - Frontend Initialized');
});

// HTMX event handlers
document.addEventListener('htmx:beforeRequest', (event) => {
    // Show loading state
    const target = event.target;
    if (target) {
        target.classList.add('opacity-50');
    }
});

document.addEventListener('htmx:afterRequest', (event) => {
    // Hide loading state
    const target = event.target;
    if (target) {
        target.classList.remove('opacity-50');
    }
});

document.addEventListener('htmx:responseError', (event) => {
    // Handle errors gracefully
    console.error('HTMX request failed:', event.detail);
    const target = event.target;
    if (target) {
        target.innerHTML = '<div class="text-red-400 text-center p-4">Failed to load data. Please try again.</div>';
    }
});

// Utility functions
window.daenaUtils = {
    formatUptime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    },
    
    formatBytes(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    },
    
    formatPercentage(value) {
        return Math.round(value * 100) / 100 + '%';
    }
}; 