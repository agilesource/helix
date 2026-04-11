"""
Helix Performance Monitor

Performance tracking and metrics:
- Request latency tracking
- Skill execution metrics
- Resource usage monitoring
- Performance trends
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import threading


@dataclass
class MetricPoint:
    """Metric data point"""
    timestamp: float
    value: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics summary"""
    total_requests: int
    success_count: int
    failure_count: int
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    requests_per_minute: float


class PerformanceMonitor:
    """
    Performance Monitoring System

    Tracks:
    - Request latency
    - Success/failure rates
    - Resource usage
    - Historical trends
    """

    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self._lock = threading.Lock()

        # Request metrics
        self._request_times: deque = deque(maxlen=max_history)
        self._request_success: deque = deque(maxlen=max_history)
        self._request_latencies: deque = deque(maxlen=max_history)

        # Skill-specific metrics
        self._skill_metrics: Dict[str, Dict[str, Any]] = {}

        # Start time
        self._start_time = time.time()

    def record_request(self, skill: str, latency_ms: float, success: bool) -> None:
        """Record a request"""
        with self._lock:
            timestamp = time.time()

            self._request_times.append(timestamp)
            self._request_success.append(success)
            self._request_latencies.append(latency_ms)

            # Update skill-specific metrics
            if skill not in self._skill_metrics:
                self._skill_metrics[skill] = {
                    "count": 0,
                    "success": 0,
                    "failure": 0,
                    "total_latency": 0,
                    "latencies": deque(maxlen=1000),
                }

            metrics = self._skill_metrics[skill]
            metrics["count"] += 1
            metrics["total_latency"] += latency_ms
            metrics["latencies"].append(latency_ms)

            if success:
                metrics["success"] += 1
            else:
                metrics["failure"] += 1

    def get_metrics(self) -> PerformanceMetrics:
        """Get overall performance metrics"""
        with self._lock:
            if not self._request_latencies:
                return PerformanceMetrics(
                    total_requests=0,
                    success_count=0,
                    failure_count=0,
                    avg_latency_ms=0,
                    p50_latency_ms=0,
                    p95_latency_ms=0,
                    p99_latency_ms=0,
                    requests_per_minute=0,
                )

            latencies = sorted(self._request_latencies)
            n = len(latencies)

            # Calculate percentiles
            p50 = latencies[int(n * 0.5)] if n > 0 else 0
            p95 = latencies[int(n * 0.95)] if n > 0 else 0
            p99 = latencies[int(n * 0.99)] if n > 0 else 0

            # Requests per minute
            uptime = time.time() - self._start_time
            rpm = (len(self._request_times) / uptime * 60) if uptime > 0 else 0

            return PerformanceMetrics(
                total_requests=len(self._request_times),
                success_count=sum(1 for s in self._request_success if s),
                failure_count=sum(1 for s in self._request_success if not s),
                avg_latency_ms=sum(latencies) / n if n > 0 else 0,
                p50_latency_ms=p50,
                p95_latency_ms=p95,
                p99_latency_ms=p99,
                requests_per_minute=rpm,
            )

    def get_skill_metrics(self, skill: str) -> Optional[Dict[str, Any]]:
        """Get metrics for specific skill"""
        with self._lock:
            if skill not in self._skill_metrics:
                return None

            metrics = self._skill_metrics[skill]
            latencies = sorted(metrics["latencies"])
            n = len(latencies)

            return {
                "skill": skill,
                "total_requests": metrics["count"],
                "success_count": metrics["success"],
                "failure_count": metrics["failure"],
                "success_rate": metrics["success"] / metrics["count"] if metrics["count"] > 0 else 0,
                "avg_latency_ms": metrics["total_latency"] / metrics["count"] if metrics["count"] > 0 else 0,
                "p50_latency_ms": latencies[int(n * 0.5)] if n > 0 else 0,
                "p95_latency_ms": latencies[int(n * 0.95)] if n > 0 else 0,
            }

    def get_all_skill_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics for all skills"""
        with self._lock:
            return [
                self.get_skill_metrics(skill)
                for skill in self._skill_metrics.keys()
            ]

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        metrics = self.get_metrics()

        # Determine health
        if metrics.total_requests == 0:
            status = "starting"
        elif metrics.failure_count / metrics.total_requests > 0.1:
            status = "degraded"
        elif metrics.p95_latency_ms > 5000:
            status = "degraded"
        else:
            status = "healthy"

        return {
            "status": status,
            "uptime_seconds": time.time() - self._start_time,
            "total_requests": metrics.total_requests,
            "success_rate": metrics.success_count / metrics.total_requests if metrics.total_requests > 0 else 0,
            "avg_latency_ms": metrics.avg_latency_ms,
            "p95_latency_ms": metrics.p95_latency_ms,
        }

    def reset(self) -> None:
        """Reset all metrics"""
        with self._lock:
            self._request_times.clear()
            self._request_success.clear()
            self._request_latencies.clear()
            self._skill_metrics.clear()
            self._start_time = time.time()


# Global instance
_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor
