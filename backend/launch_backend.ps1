cd "$BackendPath"
$env:LLM_API_KEY = "dummy-key"
$env:OPENAI_API_KEY = "your-openai-key"
$env:LLM_API_URL = "http://localhost:8000"
$env:OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
uvicorn main:app --reload --port=8000 --host=0.0.0.0
