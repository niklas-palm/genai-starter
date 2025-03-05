# Bedrock API Frontend Examples

## Setup

```bash
pip install -r requirements.txt
```

## Running

### Basic Chat (Non-Streaming)
```bash
python frontend/app.py  # Available at http://127.0.0.1:7861
```

### Streaming Chat
```bash
python frontend/app_streaming.py  # Available at http://127.0.0.1:7862
```

## Examples

### app.py
- Basic chat with AWS Bedrock Converse API
- Non-streaming responses
- Returns complete responses at once

### app_streaming.py
- Identical UI to app.py
- Uses real-time token streaming
- Threaded implementation with callbacks