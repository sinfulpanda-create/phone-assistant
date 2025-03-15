# Phone Model Assistant 🤖📱

An AI-powered assistant system that combines DeepSeek's natural language understanding with mock/manufacturer APIs to provide information about latest smartphone models.

## System Architecture 🏗️
1. User query ➡️ 2. Intent detection (DeepSeek R1) ➡️ 3. API data fetch ➡️ 4. Response formatting

## Core Components 🔧
- **Natural Language Understanding**: `deepseek/deepseek-r1:free` via OpenRouter
- **Mock API Server**: Flask-based mock data server (`mock_api.py`)
- **Caching System**: SQLite database (`phone_cache.db`) with 24-hour expiry
- **Error Handling**: Automatic fallback to cached data on API failures

## Key Features ✨
- Intent detection for phone-related queries
- Local mock API with sample phone data
- Rate limiting (5 requests/minute)
- Response caching for offline use
- Error simulation capabilities
- Automated cache invalidation

## Setup Instructions 💻

### 1. Clone Repository
```bash
git clone https://github.com/sinfulpanda-create/phone-assistant.git
cd phone-assistant
```

### 2. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create `.env` file with your OpenRouter API key:
```bash
echo OPENROUTER_API_KEY=your_api_key_here > .env
```

### 4. Start the System

#### For Production Mode:
```bash
python phone_assistant.py
```

#### For Development Mode:
1. Start mock API server:
```bash
python mock_api.py
```
2. In a new terminal (with activated venv):
```bash
python phone_assistant.py --mock
```

## Mock API Endpoints 🔌
- `GET /new-phones`: Returns sample phone data
  - Parameters:
    - `delay` (0-2 seconds)
    - `error` (0-1 error probability)
    - `status` (HTTP status code)

## Usage Example 💬
```bash
I specialize in information about new smartphone models. Ask me about latest releases:
what are latest models
📱 Latest Phone Models:

1. 🌟 Pixel 9 Pro
Brand: Google
Released: 2024-10-01
Features: ['Tensor G4 chip', '200MP camera', '6.7', 'LTPO OLED']

2. 🌟 iPhone 16 Ultra
Brand: Apple
Released: 2024-09-15
Features: ['A18 Bionic', 'Under-display Face ID', '10x optical zoom']

3. 🌟 Galaxy S25
Brand: Samsung
Released: 2025-01-28
Features: ['Snapdragon 8 Gen 4', '200W fast charging', 'AI Camera Suite']
