"""
Analytics Service — Properly tracks all metrics.
Called after every chat message.
"""

from collections import defaultdict
from datetime import datetime


class AnalyticsService:
    def __init__(self):
        self.total_messages   = 0
        self.total_sessions   = set()
        self.intent_dist      = defaultdict(int)
        self.sentiment_dist   = defaultdict(int)
        self.response_times   = []
        self.confidence_scores= []
        self.hourly_activity  = defaultdict(int)
        self.start_time       = datetime.utcnow()

    def track(
        self,
        intent:            str   = None,
        sentiment_label:   str   = None,
        processing_time_ms:float = None,
        confidence:        float = None,
        session_id:        str   = None,
    ):
        """Track one message — call this after every chat."""
        self.total_messages += 1

        if session_id:
            self.total_sessions.add(session_id)

        if intent:
            self.intent_dist[intent] += 1

        if sentiment_label:
            self.sentiment_dist[sentiment_label] += 1

        if processing_time_ms is not None:
            self.response_times.append(processing_time_ms)
            # Keep last 500 only
            if len(self.response_times) > 500:
                self.response_times = self.response_times[-500:]

        if confidence is not None:
            self.confidence_scores.append(confidence)
            if len(self.confidence_scores) > 500:
                self.confidence_scores = self.confidence_scores[-500:]

        # Track hourly
        hour = datetime.utcnow().hour
        self.hourly_activity[hour] += 1

    def get_stats(self) -> dict:
        rt = self.response_times
        cs = self.confidence_scores
        return {
            "total_messages":         self.total_messages,
            "total_sessions":         len(self.total_sessions),
            "intent_distribution":    dict(self.intent_dist),
            "sentiment_distribution": dict(self.sentiment_dist),
            "avg_response_time_ms":   round(sum(rt) / len(rt), 2) if rt else 0,
            "avg_confidence":         round(sum(cs) / len(cs), 4) if cs else 0,
            "hourly_activity":        dict(self.hourly_activity),
            "uptime_seconds":         int(
                (datetime.utcnow() - self.start_time).total_seconds()
            ),
        }


# Singleton — poore app mein yahi use hoga
analytics_service = AnalyticsService()