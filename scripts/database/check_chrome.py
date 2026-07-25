import urllib.request
import json

def get_tabs():
    try:
        req = urllib.request.urlopen('http://127.0.0.1:9222/json')
        tabs = json.loads(req.read().decode('utf-8'))
        for tab in tabs:
            print(f"Title: {tab.get('title')}")
            print(f"URL: {tab.get('url')}")
            print(f"WebSocket URL: {tab.get('webSocketDebuggerUrl')}")
            print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_tabs()
