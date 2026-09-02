import os
from dotenv import load_dotenv
load_dotenv()

from app import ai_assistant, config

print("="*70)
print("🤖 GROQ AI ASSISTANT TEST — Real Business Questions")
print("="*70)

print(f"\n🔧 Configuration:")
print(f"   Provider: {config.llm_provider()}")
print(f"   Model: {config.llm_model()}")
print(f"   Enabled: {config.LLM_ENABLED}")

# Test questions
test_questions = [
    "What is our total revenue?",
    "What are the top 5 products?",
    "Which branch performs best?",
]

print(f"\n{'='*70}")
print("Testing AI Assistant with Groq LLM")
print(f"{'='*70}\n")

for i, question in enumerate(test_questions, 1):
    print(f"📝 Question {i}: {question}")
    
    try:
        result = ai_assistant.answer_question(question)
        
        print(f"✅ Answer: {result['answer'][:150]}...")
        print(f"   Engine: {result['engine']}")
        print(f"   Provider: {result.get('provider', 'N/A')}")
        print(f"   Model: {result.get('model', 'N/A')}")
        if result.get('sql'):
            print(f"   SQL: {result.get('sql', 'N/A')[:70]}...")
        print(f"   Data rows: {len(result.get('rows', []))}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)[:100]}\n")

print("="*70)
print("✅ AI ASSISTANT GROQ INTEGRATION TEST COMPLETE!")
print("="*70)
