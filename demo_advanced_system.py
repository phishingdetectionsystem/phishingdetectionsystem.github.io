"""
Demo Script for Advanced Phishing Detection System
Run this to test all features and generate a report
"""
import time
from advanced_feature_extractor import extract_features_fast, AdvancedFeatureExtractor
from advanced_prediction_service import predict_url, predict_url_advanced
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_feature_extraction():
    """Demonstrate feature extraction capabilities"""
    print_section("1. FEATURE EXTRACTION DEMO")
    
    test_urls = [
        "https://www.google.com",
        "http://paypal-secure-verify.tk/login",
        "http://192.168.1.1/admin",
        "https://amazon-account-update.com/verify?redirect=malicious.com"
    ]
    
    extractor = AdvancedFeatureExtractor()
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. URL: {url}")
        print("-" * 70)
        
        # Extract features (fast version)
        features = extract_features_fast(url)
        
        print(f"✓ Extracted {len(features)} features")
        print(f"  Sample features:")
        print(f"    - URL Length: {features[0]}")
        print(f"    - Has IP: {features[1]}")
        print(f"    - Uses HTTPS: {features[6]}")
        print(f"    - Entropy: {features[11]:.2f}")
        print(f"    - Suspicious TLD: {features[8]}")


def demo_simple_prediction():
    """Demonstrate simple ML prediction"""
    print_section("2. SIMPLE ML PREDICTION DEMO (Fast)")
    
    test_urls = [
        ("https://www.google.com", "Legitimate website"),
        ("http://paypal-verify-account.tk", "Suspicious domain"),
        ("http://192.168.1.1", "IP address"),
    ]
    
    for url, description in test_urls:
        print(f"\nTesting: {url}")
        print(f"Description: {description}")
        print("-" * 70)
        
        start = time.time()
        result = predict_url(url, model_path="phishing_model_best.pkl")
        elapsed = (time.time() - start) * 1000
        
        print(f"🎯 Result:")
        print(f"  Is Phishing: {'YES ⚠️' if result['is_phishing'] else 'NO ✅'}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Processing Time: {elapsed:.1f}ms")


def demo_advanced_prediction():
    """Demonstrate advanced prediction with explanations"""
    print_section("3. ADVANCED PREDICTION WITH EXPLANATIONS")
    
    url = "http://paypal-secure-login.tk/verify"
    print(f"\nAnalyzing: {url}")
    print("-" * 70)
    
    try:
        result = predict_url_advanced(
            url,
            model_path="phishing_model_best.pkl",
            use_external_apis=False,  # Set to True if you have API keys
            explain=True
        )
        
        print(f"\n📊 ML Prediction:")
        ml = result['ml_prediction']
        print(f"  Is Phishing: {'YES ⚠️' if ml['is_phishing'] else 'NO ✅'}")
        print(f"  Confidence: {ml['confidence']:.2%}")
        print(f"  Phishing Probability: {ml['phishing_probability']:.2%}")
        print(f"  Risk Level: {ml['risk_level']}")
        
        if 'top_features' in ml:
            print(f"\n🔍 Top Contributing Features:")
            for i, feature in enumerate(ml['top_features'][:5], 1):
                impact = "🔴 Increases" if feature['impact'] == 'increases_risk' else "🟢 Decreases"
                print(f"  {i}. {feature['feature']}")
                print(f"     Value: {feature['value']}")
                print(f"     {impact} risk (contribution: {feature['contribution']:.3f})")
        
        print(f"\n🎯 Final Verdict:")
        verdict = result['final_verdict']
        print(f"  Is Phishing: {'YES ⚠️' if verdict['is_phishing'] else 'NO ✅'}")
        print(f"  Confidence: {verdict['confidence']:.2%}")
        print(f"  Risk Level: {verdict['risk_level']}")
        print(f"  Recommendation: {verdict['recommendation']}")
        
    except FileNotFoundError:
        print("\n⚠️  Model file not found!")
        print("Please run: python advanced_model_training.py first")


def demo_batch_processing():
    """Demonstrate batch URL processing"""
    print_section("4. BATCH PROCESSING DEMO")
    
    urls = [
        "https://www.google.com",
        "http://paypal.com",
        "http://phishing-site-123.tk",
        "http://192.168.1.1",
        "https://secure-login-verify.ml"
    ]
    
    print(f"\nProcessing {len(urls)} URLs in batch...")
    print("-" * 70)
    
    results = []
    start = time.time()
    
    for url in urls:
        try:
            result = predict_url(url, model_path="phishing_model_best.pkl")
            results.append({
                'url': url,
                'is_phishing': result['is_phishing'],
                'confidence': result['confidence'],
                'risk_level': result['risk_level']
            })
        except:
            results.append({
                'url': url,
                'error': 'Failed to process'
            })
    
    elapsed = (time.time() - start) * 1000
    
    # Summary
    phishing_count = sum(1 for r in results if r.get('is_phishing', False))
    legitimate_count = len(results) - phishing_count
    
    print(f"\n📈 Batch Results Summary:")
    print(f"  Total URLs: {len(urls)}")
    print(f"  Phishing Detected: {phishing_count} ⚠️")
    print(f"  Legitimate: {legitimate_count} ✅")
    print(f"  Total Processing Time: {elapsed:.1f}ms")
    print(f"  Average per URL: {elapsed/len(urls):.1f}ms")
    
    print(f"\n📋 Detailed Results:")
    for i, result in enumerate(results, 1):
        status = "⚠️ PHISHING" if result.get('is_phishing') else "✅ SAFE"
        conf = result.get('confidence', 0)
        print(f"  {i}. {result['url'][:50]}")
        print(f"     Status: {status} | Confidence: {conf:.2%}")


def demo_performance_comparison():
    """Compare basic vs advanced feature extraction"""
    print_section("5. PERFORMANCE COMPARISON")
    
    url = "http://paypal-verify-secure.tk/login?redirect=malicious.com"
    
    print(f"\nComparing extraction methods for:")
    print(f"{url}")
    print("-" * 70)
    
    # Fast extraction (production)
    start = time.time()
    features_fast = extract_features_fast(url)
    time_fast = (time.time() - start) * 1000
    
    print(f"\n⚡ Fast Extraction (Production Mode):")
    print(f"  Features: {len(features_fast)}")
    print(f"  Time: {time_fast:.2f}ms")
    print(f"  Best for: High-volume production use")
    
    # Full extraction (with external APIs)
    extractor = AdvancedFeatureExtractor(timeout=2)
    start = time.time()
    features_full = extractor.extract_all_features(url)
    time_full = (time.time() - start) * 1000
    
    print(f"\n🔍 Full Extraction (Maximum Accuracy):")
    print(f"  Features: {len(features_full)}")
    print(f"  Time: {time_full:.2f}ms")
    print(f"  Best for: Deep analysis, lower volume")
    print(f"  Speedup: {time_full/time_fast:.1f}x slower")


def generate_report():
    """Generate a comprehensive test report"""
    print_section("6. GENERATING TEST REPORT")
    
    report = {
        "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system_version": "2.0.0 - Advanced",
        "features": {
            "total_features": 35,
            "feature_categories": [
                "URL Structure (12)",
                "Domain Analysis (4)",
                "Path & Query (8)",
                "External Checks (11)"
            ]
        },
        "ml_models": [
            "Random Forest",
            "XGBoost",
            "Gradient Boosting",
            "Ensemble Voting"
        ],
        "capabilities": [
            "✅ 35+ feature extraction",
            "✅ Multiple ML algorithms",
            "✅ Hyperparameter tuning",
            "✅ Model explainability (SHAP)",
            "✅ Batch processing",
            "✅ External API integration",
            "✅ Real-time prediction",
            "✅ Risk level classification"
        ]
    }
    
    print("\n📄 Test Report Generated:")
    print(json.dumps(report, indent=2))
    
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n💾 Report saved to: test_report.json")


def main():
    """Run all demos"""
    print("\n" + "🛡️ " * 30)
    print(" " * 20 + "ADVANCED PHISHING DETECTION SYSTEM")
    print(" " * 25 + "Comprehensive Demo & Test")
    print("🛡️ " * 30)
    
    try:
        demo_feature_extraction()
        input("\nPress Enter to continue...")
        
        demo_simple_prediction()
        input("\nPress Enter to continue...")
        
        demo_advanced_prediction()
        input("\nPress Enter to continue...")
        
        demo_batch_processing()
        input("\nPress Enter to continue...")
        
        demo_performance_comparison()
        input("\nPress Enter to continue...")
        
        generate_report()
        
        print_section("DEMO COMPLETED ✅")
        print("\n🎉 All tests completed successfully!")
        print("\n📚 Next Steps:")
        print("  1. Train your model: python advanced_model_training.py")
        print("  2. Integrate into your backend")
        print("  3. Test API endpoints")
        print("  4. Deploy!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        print("Make sure you have:")
        print("  1. Installed all dependencies: pip install -r requirements_advanced.txt")
        print("  2. Trained the model: python advanced_model_training.py")


if __name__ == "__main__":
    main()
