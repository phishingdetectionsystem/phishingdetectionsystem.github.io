"""
Advanced Model Training for Phishing Detection
Includes: Multiple algorithms, hyperparameter tuning, ensemble methods, cross-validation
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


class PhishingModelTrainer:
    """Advanced training pipeline for phishing detection models"""
    
    def __init__(self, dataset_path, model_save_path='phishing_model_advanced.pkl'):
        self.dataset_path = dataset_path
        self.model_save_path = model_save_path
        self.scaler = StandardScaler()
        self.best_model = None
        self.models_performance = {}
        
    def load_data(self):
        """Load and prepare dataset"""
        print("📁 Loading dataset...")
        df = pd.read_csv(self.dataset_path)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Separate features and target
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        
        print(f"Features: {X.shape[1]}")
        print(f"Target distribution:\n{y.value_counts()}")
        
        return X, y
    
    def preprocess_data(self, X, y, test_size=0.2, scale=True):
        """Split and optionally scale the data"""
        print("\n🔧 Preprocessing data...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        if scale:
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            print("✓ Features scaled using StandardScaler")
        
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def train_multiple_models(self, X_train, X_test, y_train, y_test):
        """Train and compare multiple ML algorithms"""
        print("\n🤖 Training multiple models...\n")
        
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
            'XGBoost': XGBClassifier(n_estimators=200, random_state=42, use_label_encoder=False, eval_metric='logloss'),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=200, random_state=42),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42),
            'Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'AdaBoost': AdaBoostClassifier(n_estimators=200, random_state=42)
        }
        
        results = []
        
        for name, model in models.items():
            print(f"Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            
            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'CV Score': cv_mean,
                'model_object': model
            })
            
            print(f"  ✓ Accuracy: {accuracy:.4f} | F1: {f1:.4f} | CV: {cv_mean:.4f}\n")
            
            self.models_performance[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'cv_score': cv_mean
            }
        
        # Create comparison DataFrame
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('Accuracy', ascending=False)
        
        print("\n📊 Model Comparison:")
        print(results_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'CV Score']].to_string(index=False))
        
        # Best model
        best_model_name = results_df.iloc[0]['Model']
        self.best_model = results_df.iloc[0]['model_object']
        
        print(f"\n🏆 Best Model: {best_model_name} with accuracy {results_df.iloc[0]['Accuracy']:.4f}")
        
        return results_df
    
    def hyperparameter_tuning(self, X_train, y_train, model_type='random_forest'):
        """Perform hyperparameter tuning using GridSearchCV"""
        print(f"\n⚙️ Hyperparameter tuning for {model_type}...")
        
        if model_type == 'random_forest':
            model = RandomForestClassifier(random_state=42, n_jobs=-1)
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2']
            }
        elif model_type == 'xgboost':
            model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
        else:
            print("Invalid model type")
            return None
        
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='accuracy',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"\n✓ Best parameters: {grid_search.best_params_}")
        print(f"✓ Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def create_ensemble_model(self, X_train, y_train):
        """Create an ensemble model combining multiple algorithms"""
        print("\n🔗 Creating ensemble model (Voting Classifier)...")
        
        # Define base models
        rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        xgb = XGBClassifier(n_estimators=200, random_state=42, use_label_encoder=False, eval_metric='logloss')
        gb = GradientBoostingClassifier(n_estimators=200, random_state=42)
        
        # Create voting classifier (soft voting for probability-based voting)
        ensemble = VotingClassifier(
            estimators=[
                ('rf', rf),
                ('xgb', xgb),
                ('gb', gb)
            ],
            voting='soft'
        )
        
        print("Training ensemble model...")
        ensemble.fit(X_train, y_train)
        print("✓ Ensemble model trained")
        
        return ensemble
    
    def evaluate_model(self, model, X_test, y_test, model_name="Model"):
        """Comprehensive model evaluation"""
        print(f"\n📈 Evaluating {model_name}...")
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"\n{model_name} Performance:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {roc_auc:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(cm)
        
        # Classification Report
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }
    
    def save_model(self, model, filename=None):
        """Save trained model and scaler"""
        if filename is None:
            filename = self.model_save_path
        
        # Save model and scaler together
        model_package = {
            'model': model,
            'scaler': self.scaler,
            'performance': self.models_performance
        }
        
        joblib.dump(model_package, filename)
        print(f"\n💾 Model saved to {filename}")
    
    def plot_feature_importance(self, model, feature_names, top_n=20):
        """Plot feature importance for tree-based models"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1][:top_n]
            
            plt.figure(figsize=(12, 8))
            plt.title(f'Top {top_n} Feature Importances')
            plt.bar(range(top_n), importances[indices])
            plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            print("\n📊 Feature importance plot saved to feature_importance.png")
        else:
            print("Model doesn't support feature importance")


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("🚀 ADVANCED PHISHING DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Initialize trainer
    dataset_path = "Dataset.csv"  # Update with your dataset path
    trainer = PhishingModelTrainer(dataset_path)
    
    # Load data
    X, y = trainer.load_data()
    
    # Preprocess
    X_train, X_test, y_train, y_test = trainer.preprocess_data(X, y, scale=True)
    
    # Option 1: Train and compare multiple models
    results_df = trainer.train_multiple_models(X_train, X_test, y_train, y_test)
    
    # Option 2: Hyperparameter tuning for best model
    print("\n" + "="*60)
    choice = input("Do you want to perform hyperparameter tuning? (y/n): ")
    if choice.lower() == 'y':
        tuned_model = trainer.hyperparameter_tuning(X_train, y_train, model_type='random_forest')
        metrics = trainer.evaluate_model(tuned_model, X_test, y_test, "Tuned Random Forest")
        trainer.save_model(tuned_model, "phishing_model_tuned.pkl")
    
    # Option 3: Create ensemble model
    print("\n" + "="*60)
    choice = input("Do you want to create an ensemble model? (y/n): ")
    if choice.lower() == 'y':
        ensemble_model = trainer.create_ensemble_model(X_train, y_train)
        metrics = trainer.evaluate_model(ensemble_model, X_test, y_test, "Ensemble Model")
        trainer.save_model(ensemble_model, "phishing_model_ensemble.pkl")
    
    # Save best basic model
    trainer.save_model(trainer.best_model, "phishing_model_best.pkl")
    
    # Feature importance (if applicable)
    if hasattr(trainer.best_model, 'feature_importances_'):
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        trainer.plot_feature_importance(trainer.best_model, feature_names)
    
    print("\n" + "="*60)
    print("✅ Training completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
