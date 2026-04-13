"""Test Monitoring Module"""

import pytest
from helix.monitoring import (
    MetricPoint,
    PerformanceMetrics,
)


class TestMetricPoint:
    """Test MetricPoint dataclass"""

    def test_metric_point_creation(self):
        """Test creating a metric point"""
        point = MetricPoint(timestamp=1234567890.0, value=100.0)
        assert point.timestamp == 1234567890.0
        assert point.value == 100.0

    def test_metric_point_with_tags(self):
        """Test with tags"""
        point = MetricPoint(timestamp=1234567890.0, value=50.0, tags={"env": "test"})
        assert point.tags["env"] == "test"


class TestPerformanceMetrics:
    """Test PerformanceMetrics dataclass"""

    def test_metrics_creation(self):
        """Test creating performance metrics"""
        metrics = PerformanceMetrics(
            total_requests=100,
            success_count=95,
            failure_count=5,
            avg_latency_ms=50.0,
            p50_latency_ms=45.0,
            p95_latency_ms=100.0,
            p99_latency_ms=150.0,
            requests_per_minute=10.0
        )
        assert metrics.total_requests == 100
        assert metrics.success_count == 95
        assert metrics.failure_count == 5