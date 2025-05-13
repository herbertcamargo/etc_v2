"""
Metrics module for Prometheus monitoring.

This module sets up Prometheus metrics collection for the application.
It provides counters, histograms, and gauges for tracking application performance.
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector

# Create registry for metrics
registry = CollectorRegistry()

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total count of HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 30.0, 60.0)
)

# Business metrics
active_users_gauge = Gauge(
    'active_users',
    'Number of currently active users'
)

transcription_sessions_total = Counter(
    'transcription_sessions_total',
    'Total count of transcription sessions',
    ['status']  # status: completed, abandoned, etc.
)

transcription_accuracy_histogram = Histogram(
    'transcription_accuracy',
    'Distribution of transcription accuracy scores',
    buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0)
)

subscription_count_gauge = Gauge(
    'subscription_count',
    'Number of active subscriptions',
    ['plan']  # plan: free, monthly, yearly
)

# Database metrics
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation'],  # operation: select, insert, update, delete
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

# Function to generate metrics
def get_metrics():
    """
    Generate Prometheus metrics.
    
    Returns:
        bytes: Prometheus metrics in text format
    """
    return generate_latest(registry) 