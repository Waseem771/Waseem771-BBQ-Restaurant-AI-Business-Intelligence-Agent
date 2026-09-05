import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("="*60)
print("🧪 GROQ LLM INTEGRATION TEST")
print("="*60)

# 1. Check if Groq SDK is installed
print("\n✅ Checking Groq SDK installation...")
try:
    import groq
    print("   ✅ groq package installed: v" + groq.__version__)
except ImportError as e:
    print(f"   ❌ groq not installed: {e}")
    exit(1)

# 2. Check API key
print("\n✅ Checking GROQ_API_KEY...")
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    masked = api_key[:10] + "..." + api_key[-10:]
    print(f"   ✅ GROQ_API_KEY found: {masked}")
else:
    print("   ❌ GROQ_API_KEY not set")
    exit(1)

# 3. Check model
print("\n✅ Checking GROQ_MODEL...")
model = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
print(f"   ✅ Model: {model}")

# 4. Test Groq connection
print("\n✅ Testing Groq API connection...")
try:
    from groq import Groq
    client = Groq(api_key=api_key)
    
    # Simple test completion
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a single SQL SELECT query that sums revenue from an orders table. Only output the SQL, nothing else."}
        ],
        temperature=0.6,
        max_completion_tokens=100,
    )
    
    completion = response.choices[0].message.content
    print(f"   ✅ Groq API working!")
    print(f"   Generated SQL: {completion[:80]}...")
    
except Exception as e:
    print(f"   ❌ Groq API error: {e}")
    exit(1)

# 5. Import and test config
print("\n✅ Testing app.config...")
try:
    from app import config
    
    provider = config.llm_provider()
    llm_model = config.llm_model()
    
    print(f"   ✅ LLM Provider: {provider}")
    print(f"   ✅ LLM Model: {llm_model}")
    
    if provider != "groq":
        print(f"   ⚠️  Warning: Expected 'groq' but got '{provider}'")
    
except Exception as e:
    print(f"   ❌ Config error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ GROQ INTEGRATION TEST PASSED!")
print("="*60)
print("\nYou can now ask the AI natural language questions!")
print("The system will use Groq to generate SQL automatically.")
