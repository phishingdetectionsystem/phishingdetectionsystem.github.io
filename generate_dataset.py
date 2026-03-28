"""
Generate Phishing Detection Dataset
"""

import pandas as pd
import random
import re
from urllib.parse import urlparse


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
def has_ip(domain):
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return 1 if re.match(ip_pattern, domain) else 0


def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "signin", "confirm"
    ]

    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_symbol": 1 if "@" in url else 0,
        "has_ip": has_ip(domain),
        "https": 1 if parsed.scheme == "https" else 0,
        "digit_count": sum(c.isdigit() for c in url),
        "suspicious_words": sum(word in url.lower() for word in suspicious_keywords),
        "subdomain_count": domain.count(".")
    }


# -----------------------------
# SAMPLE SAFE URLs
# -----------------------------
safe_urls = [
    "https://www.google.com",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.github.com",
    "https://www.wikipedia.org"
]

# -----------------------------
# SAMPLE PHISHING URLs
# -----------------------------
phishing_urls = [
    "http://secure-login-bank-account-verify.com",
    "http://192.168.0.1/login",
    "http://paypal.verify-account-security.com",
    "http://update-bank-account-confirm.net",
    "http://signin-secure-user-login.com"
]


# -----------------------------
# EXPAND DATASET (AUTO GENERATE VARIANTS)
# -----------------------------
def generate_variants(base_urls, label, count=500):
    data = []
    for _ in range(count):
        url = random.choice(base_urls)

        # Add random numbers
        if label == 1:
            url = url.replace("http://", "http://secure-")
            url += str(random.randint(10, 999))

        features = extract_features(url)
        features["label"] = label
        data.append(features)

    return data


# Generate dataset
dataset = []
dataset.extend(generate_variants(safe_urls, label=0, count=1000))
dataset.extend(generate_variants(phishing_urls, label=1, count=1000))

df = pd.DataFrame(dataset)

df.to_csv("phishing_dataset.csv", index=False)

print("✅ Dataset generated successfully!")
print("Shape:", df.shape)
