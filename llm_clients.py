from openai import OpenAI
import random
import json

class BaseLLMClient:
    def chat_completion(self, model_name, messages, **kwargs):
        raise NotImplementedError(
            "Subclasses must implement chat_completion method")


from google import genai
from google.genai import types

class GoogleGenAIClient(BaseLLMClient):
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def chat_completion(self, model_name, messages, **kwargs):
        try:
            # Convert OpenAI-style messages to Gemini content format
            # messages is list of {"role": "...", "content": "..."}
            prompt = ""
            system_instruction = None
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_instruction = msg['content']
                elif msg['role'] == 'user':
                    prompt += f"User: {msg['content']}\n"
                elif msg['role'] == 'assistant':
                    prompt += f"Model: {msg['content']}\n"
            
            # Configure generation config
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 0.95),
                max_output_tokens=kwargs.get('max_tokens', 1000),
                response_mime_type="application/json" # Force JSON output
            )

            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            
            # Mock OpenAI response structure for compatibility
            class MockMessage:
                def __init__(self, content):
                    self.content = content
            
            class MockChoice:
                def __init__(self, content):
                    self.message = MockMessage(content)
                    
            class MockResponse:
                def __init__(self, content):
                    self.choices = [MockChoice(content)]
            
            return MockResponse(response.text)

        except Exception as e:
            print(f"Google GenAI API Error: {e}")
            raise e


class OllamaClient(BaseLLMClient):
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def chat_completion(self, model_name, messages, **kwargs):
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"Ollama API Error: {e}")
            raise e


class OpenRouterClient(BaseLLMClient):
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.json_schema = {
            "type": "object",
            "properties": {
                "thoughts": {
                    "type": "string",
                    "description": "Your internal reasoning"
                },
                "say": {
                    "type": "string",
                    "description": "What you choose to say publicly (optional, can be empty string)"
                },
                "action": {
                    "type": "string",
                    "description": "Your action from the list of allowed actions below"
                }
            },
            "required": [
                "thoughts",
                "action"
            ],
            "additionalProperties": False
        }

    def chat_completion(self, model_name, messages, extra_headers=None, extra_body=None, **kwargs):
        headers = {}
        if extra_headers:
            headers.update(extra_headers)
        body = {}
        if extra_body:
            body.update(extra_body)

        # Request reasoning tokens from OpenRouter (if supported by the model)
        body["include_reasoning"] = True  # Add include_reasoning here

        # Add the response_format to the body for OpenRouter structured output
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "strict": True,  # Enforce schema strictly
                "schema": self.json_schema
            }
        }

        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                extra_headers=headers,
                extra_body=body,
                **kwargs
            )

            # Extract content, ignoring reasoning tokens if present
            message_obj = response.choices[0].message
            if "reasoning" in message_obj:  # Check if 'reasoning' field exists
                # Debug log
                print(f"Reasoning tokens found in response from {model_name}")
                llm_content = message_obj.content  # Use the regular 'content' field
            else:
                # Debug log
                # print(f"No reasoning tokens in response from {model_name}")
                llm_content = message_obj.content  # Fallback to regular 'content'

            # Replace the original response.choices[0].message.content with llm_content
            # Modify the response object
            response.choices[0].message.content = llm_content

            return response  # Return the modified response

        except Exception as e:
            print(f"OpenRouter API Error: {e}")  # Log error here as well
            raise e  # Re-raise the exception to be caught in _llm_call_with_retry

class MockClient(BaseLLMClient):
    def __init__(self, api_key=None):
        pass

    def chat_completion(self, model_name, messages, **kwargs):
        # Extract allowed actions from the prompt if possible, or just return "pass"
        # The prompt is in messages[0]['content']
        prompt = messages[0]['content']
        
        allowed_actions = []
        if "**Allowed Actions:**" in prompt:
            lines = prompt.split("**Allowed Actions:**")[1].split("\n")
            for line in lines:
                if line.strip().startswith('- "'):
                    action = line.strip()[3:-1] # Remove - " and "
                    allowed_actions.append(action)
        
        action = "pass"
        if allowed_actions:
            action = random.choice(allowed_actions)
            
        response_content = json.dumps({
            "thoughts": "I am a mock bot. Beep boop.",
            "say": "I am simulating a player.",
            "action": action
        })
        
        # Mock response object structure
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
                
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
                
        return MockResponse(response_content)
