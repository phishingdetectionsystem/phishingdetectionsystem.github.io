"""
Feature Extraction Module
Used for BOTH training and prediction
"""

from urllib.parse import urlparse
import re


def has_ip(domain: str) -> int:
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return 1 if re.match(ip_pattern, domain) else 0


def extract_features(url: str):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "signin", "confirm"
    ]

    features = [
        len(url),
        len(domain),
        url.count("."),
        url.count("-"),
        1 if "@" in url else 0,
        has_ip(domain),
        1 if parsed.scheme == "https" else 0,
        sum(c.isdigit() for c in url),
        sum(word in url.lower() for word in suspicious_keywords),
        domain.count("."),
    ]

    return features
