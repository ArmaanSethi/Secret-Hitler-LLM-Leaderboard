import os
import json
print("Script started...")
from llm_clients import GoogleGenAIClient

def test_google_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Skipping Google test: GEMINI_API_KEY not found.")
        return

    print(f"Testing Google GenAI Client with key: {api_key[:5]}...")
    client = GoogleGenAIClient(api_key=api_key)
    
    messages = [{"role": "user", "content": "Say 'Hello World' in JSON format: {\"message\": \"Hello World\"}"}]
    
    try:
        response = client.chat_completion(
            model_name="gemini-2.0-flash-exp",
            messages=messages
        )
        print("Response received:")
        print(response.choices[0].message.content)
        print("Google GenAI Client Verification: SUCCESS")
    except Exception as e:
        print(f"Google GenAI Client Verification: FAILED. Error: {e}")

if __name__ == "__main__":
    test_google_client()
