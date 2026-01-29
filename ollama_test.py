

import ollama

try:
    response = ollama.generate(
        model='llama3.2:3b',
        prompt='Say hello in one word'
    )
    print("✅ Ollama connection successful!")
    print(f"Response: {response['response']}")
except Exception as e:
    print(f"❌ Error: {e}")