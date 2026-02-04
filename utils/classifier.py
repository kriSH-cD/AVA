"""Voice classifier using RandomForest."""
import os
import pickle
import numpy as np
from typing import Tuple, Dict
from sklearn.ensemble import RandomForestClassifier
from app.config import settings


class VoiceClassifier:
    """Classify voice as AI-generated or human."""
    
    def __init__(self):
        """Initialize classifier."""
        self.model = None
        self.feature_names = [
            'pitch_variance', 'pitch_std', 'pitch_range', 'pitch_mean',
            'energy_variance', 'energy_std', 'energy_range', 'energy_mean',
            'spectral_flatness_mean', 'spectral_flatness_std',
            'spectral_centroid_mean', 'spectral_centroid_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'zcr_mean', 'zcr_std', 'zcr_variance',
            'pause_regularity', 'avg_pause_duration', 'avg_speech_duration', 'speech_rate'
        ]
        self.load_model()
    
    def load_model(self):
        """Load trained model or create a new one."""
        model_path = settings.MODEL_PATH
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✓ Loaded trained model from {model_path}")
            except Exception as e:
                print(f"⚠ Failed to load model: {e}")
                self._create_default_model()
        else:
            self._create_default_model()
    
    def _create_default_model(self):
        """Create a default untrained model."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        print("⚠ Using untrained model. Please train with real data.")
    
    def predict(self, feature_vector: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict if voice is AI-generated or human.
        
        Args:
            feature_vector: Extracted features as numpy array
            
        Returns:
            Tuple of (classification, confidence, feature_importances)
        """
        # Reshape for single prediction
        features = feature_vector.reshape(1, -1)
        
        # If model is not trained, use heuristic-based classification
        if not hasattr(self.model, 'classes_'):
            return self._heuristic_classification(feature_vector)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(features)[0]
        
        # Assuming classes are [0: HUMAN, 1: AI_GENERATED]
        ai_probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
        
        # Classify based on threshold
        classification = "AI_GENERATED" if ai_probability >= settings.CONFIDENCE_THRESHOLD else "HUMAN"
        confidence = float(ai_probability)
        
        # Get feature importances
        feature_importances = {}
        if hasattr(self.model, 'feature_importances_'):
            for name, importance in zip(self.feature_names, self.model.feature_importances_):
                feature_importances[name] = float(importance)
        
        return classification, confidence, feature_importances
    
    def _heuristic_classification(self, feature_vector: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """
        Heuristic-based classification when model is not trained.
        
        This uses known patterns of AI voices:
        - Low pitch variance (AI is more stable)
        - Low pause regularity variance (AI pauses are consistent)
        - High spectral flatness (AI is smoother)
        
        Args:
            feature_vector: Extracted features
            
        Returns:
            Tuple of (classification, confidence, feature_scores)
        """
        features_dict = dict(zip(self.feature_names, feature_vector))
        
        # Scoring system (0-1, higher = more likely AI)
        ai_score = 0.0
        weights = {}
        
        # 1. Pitch variance (lower = more AI-like)
        pitch_var_normalized = min(features_dict['pitch_variance'] / 1000.0, 1.0)
        pitch_score = 1.0 - pitch_var_normalized
        ai_score += pitch_score * 0.25
        weights['pitch_variance'] = 0.25
        
        # 2. Pause regularity (lower = more AI-like, consistent pauses)
        pause_reg_normalized = min(features_dict['pause_regularity'] / 0.5, 1.0)
        pause_score = 1.0 - pause_reg_normalized
        ai_score += pause_score * 0.20
        weights['pause_regularity'] = 0.20
        
        # 3. Spectral flatness (higher = more AI-like, smoother spectrum)
        spectral_flat = features_dict['spectral_flatness_mean']
        spectral_score = min(spectral_flat * 2.0, 1.0)
        ai_score += spectral_score * 0.20
        weights['spectral_flatness_mean'] = 0.20
        
        # 4. Energy variance (lower = more AI-like)
        energy_var_normalized = min(features_dict['energy_variance'] / 0.01, 1.0)
        energy_score = 1.0 - energy_var_normalized
        ai_score += energy_score * 0.15
        weights['energy_variance'] = 0.15
        
        # 5. ZCR variance (lower = more AI-like)
        zcr_var_normalized = min(features_dict['zcr_variance'] / 0.01, 1.0)
        zcr_score = 1.0 - zcr_var_normalized
        ai_score += zcr_score * 0.20
        weights['zcr_variance'] = 0.20
        
        # Normalize to 0-1
        confidence = min(max(ai_score, 0.0), 1.0)
        
        # Classify
        classification = "AI_GENERATED" if confidence >= settings.CONFIDENCE_THRESHOLD else "HUMAN"
        
        return classification, confidence, weights
    
    def generate_explanation(
        self,
        classification: str,
        confidence: float,
        features: Dict[str, float],
        feature_importances: Dict[str, float]
    ) -> str:
        """
        Generate human-readable explanation for the classification.
        
        Args:
            classification: Classification result
            confidence: Confidence score
            features: Extracted features
            feature_importances: Feature importance scores
            
        Returns:
            Explanation string
        """
        # Get top 3 most important features
        sorted_features = sorted(
            feature_importances.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        explanations = []
        
        for feature_name, importance in sorted_features:
            feature_value = features.get(feature_name, 0.0)
            
            if 'pitch' in feature_name:
                if feature_value < 500:
                    explanations.append("unnaturally stable pitch")
                else:
                    explanations.append("natural pitch variation")
            
            elif 'pause' in feature_name:
                if feature_value < 0.2:
                    explanations.append("low pause variability")
                else:
                    explanations.append("natural pause patterns")
            
            elif 'spectral_flatness' in feature_name:
                if feature_value > 0.3:
                    explanations.append("smooth spectral characteristics")
                else:
                    explanations.append("natural spectral variation")
            
            elif 'energy' in feature_name:
                if feature_value < 0.005:
                    explanations.append("consistent energy levels")
                else:
                    explanations.append("natural energy fluctuation")
            
            elif 'zcr' in feature_name:
                if feature_value < 0.005:
                    explanations.append("uniform zero-crossing patterns")
                else:
                    explanations.append("natural zero-crossing variation")
        
        # Build final explanation
        if classification == "AI_GENERATED":
            base = "Analysis indicates synthetic speech patterns: "
        else:
            base = "Analysis indicates human speech patterns: "
        
        explanation = base + ", ".join(explanations) + "."
        
        # Capitalize first letter
        explanation = explanation[0].upper() + explanation[1:]
        
        return explanation
    
    def save_model(self, model_path: str = None):
        """Save trained model to disk."""
        if model_path is None:
            model_path = settings.MODEL_PATH
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"✓ Model saved to {model_path}")
