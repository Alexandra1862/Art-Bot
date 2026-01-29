

import sys

print("🔍 Testing Ollama connection...")
print(f"Python version: {sys.version}")

# Test 1: Import
try:
    import ollama
    print("✅ ollama library imported successfully")
except ImportError as e:
    print(f"❌ Failed to import ollama: {e}")
    sys.exit(1)

# Test 2: List models
try:
    models = ollama.list()
    print(f"✅ Connected to Ollama")
    print(f"Available models: {models}")
except Exception as e:
    print(f"❌ Failed to connect to Ollama: {e}")
    print(f"Error type: {type(e).__name__}")
    sys.exit(1)

# Test 3: Generate response
try:
    response = ollama.generate(
        model='llama3.2:3b',
        prompt='Say hi in one word'
    )
    print(f"✅ Generation successful!")
    print(f"Response: {response['response']}")
except Exception as e:
    print(f"❌ Failed to generate: {e}")
    print(f"Error type: {type(e).__name__}")
    sys.exit(1)

print("\n🎉 All tests passed! Ollama is working correctly.")
