import sys
import os

def log(msg):
    sys.stderr.write(f"[VERIFY] {msg}\n")
    sys.stderr.flush()

log("Starting verification...")

try:
    log("Importing llm_clients...")
    from llm_clients import GoogleGenAIClient, OllamaClient, OpenRouterClient, MockClient
    log("Import successful.")
except Exception as e:
    log(f"Import FAILED: {e}")
    sys.exit(1)

def test_google():
    log("Testing Google Client...")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        log("Skipping Google: No API Key")
        return
    
    try:
        client = GoogleGenAIClient(api_key=key)
        # We won't make a network call if we want to be safe, but let's try a dry run or just init
        log("Google Client initialized.")
        # Uncomment to try real call
        # response = client.chat_completion("gemini-2.0-flash-exp", [{"role": "user", "content": "Hi"}])
        # log(f"Google Response: {response.choices[0].message.content}")
    except Exception as e:
        log(f"Google Client FAILED: {e}")

def test_ollama():
    log("Testing Ollama Client...")
    try:
        client = OllamaClient()
        log("Ollama Client initialized.")
    except Exception as e:
        log(f"Ollama Client FAILED: {e}")

if __name__ == "__main__":
    test_google()
    test_ollama()
    log("Verification Complete.")
