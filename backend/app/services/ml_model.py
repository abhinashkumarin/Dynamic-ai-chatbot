"""
ML Model — Self-Learning Neural Network
scikit-learn MLPClassifier + feedback-based retraining
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path

import numpy as np
from loguru import logger

from app.core.config import settings

MODEL_PATH    = Path(settings.MODEL_PATH) / "ml_model.json"
FEEDBACK_PATH = Path("app/data/feedback_data.json")

FEATURE_NAMES = [
    "has_greeting", "has_question", "has_negative", "has_positive",
    "has_thanks", "has_tech", "msg_length", "word_count", "has_emotion"
]
OUTPUT_LABELS = [
    "greeting", "question", "negative", "positive",
    "farewell", "technical", "thanks"
]

KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "bye", "goodbye"],
    "question": ["what", "how", "why", "when", "where", "who", "which", "explain", "define"],
    "negative": ["bad", "terrible", "hate", "awful", "wrong", "error", "not", "worst"],
    "positive": ["good", "great", "amazing", "love", "excellent", "wonderful", "perfect", "happy"],
    "thanks":   ["thank", "thanks", "appreciate", "grateful", "cheers"],
    "tech":     ["python", "java", "code", "api", "database", "algorithm", "neural", "ml", "ai"],
    "emotion":  ["feel", "feeling", "i am", "sad", "happy", "angry", "excited", "worried"],
}


def encode_input(text: str) -> list:
    lower = text.lower()
    words = lower.split()
    return [
        1.0 if any(k in lower for k in KEYWORDS["greeting"]) else 0.0,
        1.0 if any(k in lower for k in KEYWORDS["question"]) else 0.0,
        1.0 if any(k in lower for k in KEYWORDS["negative"]) else 0.0,
        1.0 if any(k in lower for k in KEYWORDS["positive"]) else 0.0,
        1.0 if any(k in lower for k in KEYWORDS["thanks"])   else 0.0,
        1.0 if any(k in lower for k in KEYWORDS["tech"])     else 0.0,
        min(len(text) / 200.0, 1.0),
        min(len(words) / 50.0, 1.0),
        1.0 if any(k in lower for k in KEYWORDS["emotion"])  else 0.0,
    ]


# ─── Training Data (every label has 3+ rows) ─────────────────────────────────
BASE_TRAINING = [
    # [features 9]                                   , [output 7: greet,quest,neg,pos,farewell,tech,thanks]

    # greeting (col 0) — 3 rows
    ([1, 0, 0, 1, 0, 0, 0.1, 0.1, 0], [1, 0, 0, 1, 0, 0, 0]),
    ([1, 1, 0, 0, 0, 0, 0.3, 0.2, 0], [1, 1, 0, 0, 0, 0, 0]),
    ([1, 0, 0, 1, 1, 0, 0.2, 0.2, 0], [1, 0, 0, 1, 0, 0, 1]),

    # question (col 1) — 3 rows
    ([0, 1, 0, 0, 0, 0, 0.4, 0.3, 0], [0, 1, 0, 0, 0, 0, 0]),
    ([0, 1, 0, 1, 0, 0, 0.5, 0.4, 0], [0, 1, 0, 1, 0, 0, 0]),
    ([0, 1, 1, 0, 0, 0, 0.6, 0.5, 1], [0, 1, 1, 0, 0, 0, 0]),

    # negative (col 2) — 3 rows
    ([0, 0, 1, 0, 0, 0, 0.2, 0.2, 1], [0, 0, 1, 0, 0, 0, 0]),
    ([0, 0, 1, 0, 0, 0, 0.7, 0.5, 1], [0, 0, 1, 0, 0, 0, 0]),
    ([0, 0, 1, 0, 0, 1, 0.8, 0.6, 1], [0, 0, 1, 0, 0, 1, 0]),

    # positive (col 3) — 3 rows
    ([0, 0, 0, 1, 1, 0, 0.1, 0.1, 0], [0, 0, 0, 1, 0, 0, 1]),
    ([0, 0, 0, 1, 0, 0, 0.3, 0.2, 0], [0, 0, 0, 1, 0, 0, 0]),
    ([0, 0, 0, 1, 0, 1, 0.5, 0.3, 0], [0, 0, 0, 1, 0, 1, 0]),

    # farewell (col 4) — 3 rows
    ([1, 0, 0, 0, 0, 0, 0.1, 0.1, 0], [0, 0, 0, 0, 1, 0, 0]),
    ([1, 0, 0, 1, 0, 0, 0.1, 0.1, 0], [0, 0, 0, 0, 1, 0, 0]),
    ([1, 0, 0, 0, 1, 0, 0.1, 0.1, 0], [0, 0, 0, 0, 1, 0, 0]),

    # technical (col 5) — 3 rows
    ([0, 1, 0, 0, 0, 1, 0.6, 0.4, 0], [0, 1, 0, 0, 0, 1, 0]),
    ([0, 0, 1, 0, 0, 1, 0.8, 0.6, 1], [0, 0, 1, 0, 0, 1, 0]),
    ([0, 0, 0, 1, 0, 1, 0.5, 0.3, 0], [0, 0, 0, 1, 0, 1, 0]),

    # thanks (col 6) — 3 rows
    ([0, 0, 0, 0, 1, 0, 0.2, 0.2, 0], [0, 0, 0, 0, 0, 0, 1]),
    ([0, 0, 0, 1, 1, 0, 0.1, 0.1, 0], [0, 0, 0, 1, 0, 0, 1]),
    ([1, 0, 0, 1, 1, 0, 0.2, 0.2, 0], [1, 0, 0, 1, 0, 0, 1]),

    # extra mixed
    ([0, 0, 0, 0, 0, 0, 0.5, 0.4, 1], [0, 0, 0, 0, 0, 0, 0]),
    ([0, 1, 1, 0, 0, 0, 0.6, 0.5, 1], [0, 1, 1, 0, 0, 0, 0]),
    ([0, 1, 0, 0, 0, 1, 0.4, 0.3, 0], [0, 1, 0, 0, 0, 1, 0]),
]


class MLModel:
    def __init__(self):
        self.model          = None
        self.feedback_data: list = []
        self.is_ready       = False
        self._retrain_count = 0

    async def initialize(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._load_and_train)

    def _load_feedback(self):
        try:
            FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
            if FEEDBACK_PATH.exists():
                with open(FEEDBACK_PATH) as f:
                    self.feedback_data = json.load(f)
                logger.info(f"📂 Loaded {len(self.feedback_data)} feedback samples")
        except Exception as e:
            logger.warning(f"Could not load feedback: {e}")
            self.feedback_data = []

    def _save_feedback(self):
        try:
            FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(FEEDBACK_PATH, "w") as f:
                json.dump(self.feedback_data, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Could not save feedback: {e}")

    def _load_and_train(self):
        self._load_feedback()
        self._train()

    def _train(self):
        try:
            from sklearn.neural_network import MLPClassifier
            from sklearn.multioutput import MultiOutputClassifier
            from sklearn.preprocessing import StandardScaler
            from sklearn.pipeline import Pipeline

            X = [row[0] for row in BASE_TRAINING]
            y = [row[1] for row in BASE_TRAINING]

            for fb in self.feedback_data:
                if "input" in fb and "output" in fb:
                    X.append(fb["input"])
                    y.append(fb["output"])

            X_arr = np.array(X, dtype=float)
            y_arr = np.array(y, dtype=float)

            total = len(X_arr)
            # Only use early_stopping when enough samples
            use_early_stop = total >= 20

            self.model = Pipeline([
                ("scaler", StandardScaler()),
                ("mlp", MultiOutputClassifier(
                    MLPClassifier(
                        hidden_layer_sizes = (64, 32, 16),
                        activation         = "relu",
                        solver             = "adam",
                        max_iter           = 1000,
                        random_state       = 42,
                        learning_rate_init = 0.001,
                        early_stopping     = use_early_stop,
                        validation_fraction= 0.15,
                        n_iter_no_change   = 20,
                    )
                ))
            ])
            self.model.fit(X_arr, y_arr)
            self.is_ready       = True
            self._retrain_count += 1
            logger.info(
                f"✅ ML Model trained: {total} samples, "
                f"early_stopping={use_early_stop}, #{self._retrain_count}"
            )
        except ImportError as e:
            logger.warning(f"scikit-learn not available: {e}")
        except Exception as e:
            logger.error(f"ML training error: {e}")

    def predict(self, text: str):
        if not self.is_ready or self.model is None:
            return None
        try:
            features   = encode_input(text)
            X          = np.array([features])
            proba_list = self.model.predict_proba(X)
            result     = {}
            for i, label in enumerate(OUTPUT_LABELS):
                if i < len(proba_list):
                    prob = proba_list[i][0]
                    result[label] = round(
                        float(prob[1]) if len(prob) > 1 else float(prob[0]), 4
                    )
            dominant = max(result, key=result.get) if result else "unknown"
            return {
                "scores":        result,
                "dominant":      dominant,
                "confidence":    result.get(dominant, 0.0),
                "retrain_count": self._retrain_count,
            }
        except Exception as e:
            logger.debug(f"ML predict error: {e}")
            return None

    def add_feedback(self, text: str, correct_label: str, was_helpful: bool):
        label_map = {
            "greeting":  [1, 0, 0, 0, 0, 0, 0],
            "question":  [0, 1, 0, 0, 0, 0, 0],
            "negative":  [0, 0, 1, 0, 0, 0, 0],
            "positive":  [0, 0, 0, 1, 0, 0, 0],
            "farewell":  [0, 0, 0, 0, 1, 0, 0],
            "technical": [0, 0, 0, 0, 0, 1, 0],
            "thanks":    [0, 0, 0, 0, 0, 0, 1],
        }
        if correct_label not in label_map:
            return
        entry = {
            "input":         encode_input(text),
            "output":        label_map[correct_label],
            "timestamp":     datetime.utcnow().isoformat(),
            "was_helpful":   was_helpful,
            "correct_label": correct_label,
        }
        self.feedback_data.append(entry)
        self._save_feedback()

        if len(self.feedback_data) % 10 == 0:
            logger.info(f"🔄 Retraining ML with {len(self.feedback_data)} feedback samples...")
            import threading
            threading.Thread(target=self._train, daemon=True).start()

    def get_stats(self) -> dict:
        return {
            "is_ready":      self.is_ready,
            "feedback_count":self.feedback_data.__len__(),
            "retrain_count": self._retrain_count,
            "architecture":  "MLP [9 → 64 → 32 → 16 → 7] (MultiOutput)",
            "features":      FEATURE_NAMES,
            "output_labels": OUTPUT_LABELS,
        }


ml_model = MLModel()