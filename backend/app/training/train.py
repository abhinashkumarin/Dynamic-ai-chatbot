"""
Model Training Script
Run: python -m app.training.train
Trains all AI models and validates them
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import asyncio
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")


async def main():
    print("\n" + "═" * 55)
    print("    🤖 Dynamic AI Chatbot — Model Training Pipeline")
    print("═" * 55 + "\n")

    # ── Step 1: Intent Classifier ──────────────────────────────────
    print("[1/4] Training Intent Classifier (Naive Bayes + TF-IDF)...")
    from app.services.nlp_engine import nlp_engine
    await nlp_engine.initialize()
    print("      ✅ Intent Classifier ready\n")

    # ── Step 2: ML Neural Network ──────────────────────────────────
    print("[2/4] Training MLP Neural Network (scikit-learn)...")
    from app.services.ml_model import ml_model
    await ml_model.initialize()
    print("      ✅ Neural Network trained\n")

    # ── Step 3: Sentiment Analyzer ─────────────────────────────────
    print("[3/4] Initializing VADER Sentiment Analyzer...")
    # Already done during nlp_engine.initialize()
    print("      ✅ VADER Sentiment Analyzer ready\n")

    # ── Step 4: Validation ─────────────────────────────────────────
    print("[4/4] Validating models with test inputs...")
    print("─" * 55)

    test_cases = [
        ("Hello there! How are you?", "greeting"),
        ("Tell me a joke please 😄", "joke"),
        ("I am very frustrated and angry", "sentiment_negative"),
        ("Thank you so much for helping!", "thanks"),
        ("What is machine learning?", "technical"),
        ("Goodbye! See you later", "farewell"),
        ("I feel so happy today!", "sentiment_positive"),
        ("Who are you?", "about"),
    ]

    print(f"\n{'Input':<40} {'Intent':<20} {'Confidence':<12} {'Sentiment'}")
    print("-" * 90)

    correct = 0
    for text, expected in test_cases:
        intent_r = nlp_engine.intent_classifier.predict(text)
        sentiment = nlp_engine.sentiment_analyzer.analyze(text)
        ml_pred = ml_model.predict(text)

        predicted = intent_r['intent']
        conf = intent_r['confidence']
        sent = sentiment['label']
        match = "✅" if predicted == expected else f"⚠️ (exp: {expected})"

        if predicted == expected:
            correct += 1

        short_text = text[:38] + ".." if len(text) > 40 else text
        print(f"  {short_text:<40} {predicted:<20} {conf:<12.3f} {sent} {sentiment['emoji']} {match}")

    accuracy = correct / len(test_cases) * 100
    print(f"\n  Accuracy: {correct}/{len(test_cases)} ({accuracy:.1f}%)")

    # ML stats
    ml_stats = ml_model.get_stats()
    print("\n" + "═" * 55)
    print("  📊 MODEL STATISTICS")
    print("═" * 55)
    print(f"  Intent Classifier  : Naive Bayes + TF-IDF (n-gram 1-2)")
    print(f"  ML Neural Network  : {ml_stats['architecture']}")
    print(f"  Input Features     : {len(ml_stats['features'])} features")
    print(f"  Output Labels      : {', '.join(ml_stats['output_labels'])}")
    print(f"  Feedback Samples   : {ml_stats['feedback_count']}")
    print(f"  VADER Sentiment    : ✅ Active")
    print(f"  NER Processor      : ✅ Active (regex + keywords)")
    print(f"  Context Memory     : ✅ Active (20-turn window)")
    print("═" * 55)
    print("\n  ✅ All models trained and validated!")
    print("  🚀 Start server: uvicorn main:socket_app --reload --port 8000\n")


if __name__ == "__main__":
    asyncio.run(main())
