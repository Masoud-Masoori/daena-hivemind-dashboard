# 🚀 Daena AI VP Demo - Launch Instructions

**Enhanced Demo with Azure OpenAI Integration & Real-time Analytics**

## 🎯 Quick Start

### Option 1: One-Click Launch (Windows)
```bash
.\launch_demo.bat
```

### Option 2: Python Launch
```bash
python launch_demo.py
```

### Option 3: Manual Launch
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## 🌐 Access Points

- **Demo Dashboard**: `http://localhost:3000/demo/`
- **API Documentation**: `http://localhost:3000/docs`
- **Health Check**: `http://localhost:3000/demo/health`
- **System Status**: `http://localhost:3000/demo/system-status`

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_demo.py
```

## ✨ Enhanced Features

### 🎨 **Live Demo Dashboard**
- **Real-time Chat**: Interactive conversation with Daena AI VP
- **Voice Integration**: Speech-to-text and text-to-speech
- **Usage Analytics**: Live token usage, email count, session duration
- **System Status**: Real-time monitoring of all services

### 🤖 **Azure OpenAI Integration**
- **Model**: `daena` deployment on Azure
- **Endpoint**: `https://canadacentral.api.cognitive.microsoft.com/`
- **Features**: 
  - Intelligent chat responses
  - Personalized email generation
  - Token usage tracking
  - Real-time cost monitoring

### 📧 **Investor Outreach System**
- **Pre-configured Investors**: 4 major Canadian funds
- **Email Tones**: Professional, Friendly, Confident, Innovative
- **Custom Messages**: Personalized content
- **Email History**: Complete audit trail
- **Simulated Sending**: Safe demo environment

### 🎤 **Voice Features**
- **Wake Word**: "Hey Daena" or "Hello Daena"
- **Voice Input**: Click microphone button
- **Voice Output**: Automatic speech for investor-related queries
- **Real-time Processing**: Instant voice recognition

### 📊 **Real-time Analytics**
- **Token Usage**: Azure OpenAI consumption tracking
- **Email Metrics**: Sent count and success rates
- **Voice Interactions**: Usage statistics
- **Session Duration**: Active time tracking
- **System Health**: Service status monitoring

## 🔧 Configuration

### Environment Variables
```env
# Gmail Configuration
GMAIL_USER=masoud.masoori@gmail.com
GMAIL_APP_PASSWORD=demo_password_for_testing

# Azure OpenAI Configuration
OPENAI_API_TYPE=azure
OPENAI_API_KEY=1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN
OPENAI_API_BASE=https://canadacentral.api.cognitive.microsoft.com/
OPENAI_API_VERSION=2024-02-15
OPENAI_DEPLOYMENT_NAME=daena

# Demo Configuration
DEMO_PORT=3000
DEMO_MODE=production
```

### Dependencies
```bash
pip install fastapi uvicorn openai requests PyJWT python-multipart jinja2
```

## 🎮 Demo Flow

### 1. **Initial Setup**
- Launch demo server
- Open dashboard at `http://localhost:3000/demo/`
- Verify all services are online

### 2. **Chat with Daena**
- Type messages or use voice input
- Ask about investor outreach capabilities
- Experience intelligent responses

### 3. **Investor Email Generation**
- Select investor type (Toronto AI, Canadian Tech, etc.)
- Choose email tone
- Add custom message
- Generate personalized email

### 4. **Email Sending**
- Preview generated email
- Send (simulated) to investor
- View in email history
- Track usage analytics

### 5. **Voice Interaction**
- Click microphone button
- Say "Hey Daena, generate an investor email"
- Experience voice-activated workflow

## 📈 Usage Analytics

### Real-time Metrics
- **Azure OpenAI Tokens**: Live consumption tracking
- **Emails Sent**: Campaign success metrics
- **Voice Interactions**: Voice feature usage
- **Session Duration**: Active demo time

### Cost Monitoring
- Token usage displayed in real-time
- Azure OpenAI API consumption
- Demo session cost tracking

## 🔍 API Endpoints

### Core Demo Routes
- `GET /demo/` - Main dashboard
- `POST /demo/chat` - Chat with Daena
- `POST /demo/generate-email` - Generate investor email
- `POST /demo/send-email` - Send email (simulated)
- `GET /demo/email-history` - Email history
- `GET /demo/usage-stats` - Real-time analytics
- `GET /demo/system-status` - Service health
- `GET /demo/demo-data` - Demo configuration

### Health & Monitoring
- `GET /demo/health` - Service health check
- `POST /demo/voice-interaction` - Voice usage tracking

## 🎯 Demo Scenarios

### Scenario 1: Investor Outreach
1. Ask Daena: "Generate an email for Toronto AI investors"
2. Select investor type and tone
3. Generate personalized email
4. Send and track results

### Scenario 2: Business Strategy
1. Ask Daena: "What's our market position?"
2. Get strategic analysis
3. Discuss funding strategy
4. Explore growth opportunities

### Scenario 3: Voice Interaction
1. Click microphone button
2. Say: "Hey Daena, tell me about our Series A plans"
3. Get voice response
4. Continue voice conversation

## 🚨 Troubleshooting

### Common Issues

**Port 3000 in use:**
```bash
# Check what's using the port
netstat -ano | findstr :3000
# Kill the process or use different port
```

**Azure OpenAI not connecting:**
```bash
# Check API key and endpoint
echo %OPENAI_API_KEY%
echo %OPENAI_API_BASE%
# Verify in Azure portal
```

**Dependencies missing:**
```bash
pip install -r requirements.txt
# Or install individually
pip install fastapi uvicorn openai requests PyJWT
```

**Voice not working:**
- Check microphone permissions
- Ensure browser supports Web Speech API
- Try different browser (Chrome recommended)

### Error Messages

**"Azure OpenAI client not available"**
- Check API key configuration
- Verify endpoint URL
- Ensure deployment name is correct

**"Template not found"**
- Ensure you're in the correct directory
- Check file paths in demo routes

**"Module not found"**
- Install missing dependencies
- Activate virtual environment

## 📞 Support

### Quick Help
- **Demo Issues**: Check browser console for errors
- **Server Issues**: Review terminal output
- **API Issues**: Check `/demo/health` endpoint

### Logs
- **Server Logs**: Terminal output
- **Email Logs**: `logs/email_log.jsonl`
- **Error Logs**: Browser console

## 🎉 Success Indicators

### ✅ Working Demo
- Dashboard loads at `http://localhost:3000/demo/`
- Chat responds intelligently
- Email generation works
- Voice features function
- Analytics display real-time data

### 📊 Performance Metrics
- Response time < 2 seconds
- Voice recognition accuracy > 90%
- Email generation success > 95%
- System uptime > 99%

---

**🚀 Ready to experience the future of AI leadership? Launch the demo now!**

**🌐 [Launch Demo](http://localhost:3000/demo) | 📊 [API Docs](http://localhost:3000/docs) | 🧪 [Run Tests](python test_demo.py)** 