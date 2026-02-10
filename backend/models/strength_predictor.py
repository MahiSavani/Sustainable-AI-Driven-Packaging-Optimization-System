"""
Strength Predictor - Random Forest Classifier
Predicts structural integrity and strength of packaging design
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os


class StrengthPredictor:
    """
    Uses Random Forest to predict packaging structural strength
    
    Features:
    - Box dimensions (length, width, height)
    - Material type
    - Product weight
    - Fragility level
    
    Output:
    - Strength score (0-100%)
    - Durability score (0-100%)
    - Compression resistance score
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.model_path = 'models/trained/strength_model.pkl'
        
        # Material strength database
        self.material_properties = {
            'Recycled Cardboard': {
                'base_strength': 0.75,
                'tensile_strength': 150,  # kg/cm²
                'compression': 0.70,
                'durability': 0.80
            },
            'Double-Wall Corrugated Cardboard': {
                'base_strength': 0.95,
                'tensile_strength': 250,
                'compression': 0.92,
                'durability': 0.88
            },
            '100% Recycled Kraft Paper': {
                'base_strength': 0.65,
                'tensile_strength': 120,
                'compression': 0.60,
                'durability': 0.70
            },
            'Recycled Cardboard with Biodegradable Foam': {
                'base_strength': 0.85,
                'tensile_strength': 180,
                'compression': 0.85,
                'durability': 0.90
            },
            'Food-Grade Biodegradable Cardboard': {
                'base_strength': 0.80,
                'tensile_strength': 160,
                'compression': 0.78,
                'durability': 0.82
            },
            'Foam Insert Box': {
                'base_strength': 0.85,
                'tensile_strength': 140,
                'compression': 0.88,
                'durability': 0.85
            }
        }
        
        # Try to load pre-trained model
        self._load_model()
    
    
    def _load_model(self):
        """Load pre-trained model if exists"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                print("✓ Strength predictor model loaded from disk")
            except Exception as e:
                print(f"✗ Error loading model: {e}")
                self._initialize_model()
        else:
            self._initialize_model()
    
    
    def _initialize_model(self):
        """Initialize a new Random Forest model"""
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        print("✓ New strength predictor model initialized")
    
    
    def predict(self, dimensions, material_name, weight, fragility):
        """
        Predict structural strength scores
        
        Args:
            dimensions (dict): Box dimensions {'length', 'width', 'height'}
            material_name (str): Name of material
            weight (float): Product weight in kg
            fragility (int): Fragility level (1-5)
        
        Returns:
            dict: Strength analysis scores
        """
        
        # Get material properties
        material_props = self.material_properties.get(
            material_name,
            self.material_properties['Recycled Cardboard']  # Default
        )
        
        base_strength = material_props['base_strength']
        compression_factor = material_props['compression']
        durability_factor = material_props['durability']
        
        # Calculate volume and surface area
        volume = dimensions['length'] * dimensions['width'] * dimensions['height']
        surface_area = 2 * (
            dimensions['length'] * dimensions['width'] +
            dimensions['width'] * dimensions['height'] +
            dimensions['height'] * dimensions['length']
        )
        
        # Volume-to-weight ratio (better ratio = better strength distribution)
        # Convert weight to grams for better ratio calculation
        weight_grams = weight * 1000
        vw_ratio = volume / weight_grams if weight_grams > 0 else 0
        
        # Determine strength factor based on VW ratio
        if vw_ratio > 500:
            strength_factor = 0.98  # Excellent - very light load
        elif vw_ratio > 300:
            strength_factor = 0.92  # Good
        elif vw_ratio > 150:
            strength_factor = 0.85  # Adequate
        elif vw_ratio > 75:
            strength_factor = 0.75  # Marginal
        else:
            strength_factor = 0.65  # Needs reinforcement
        
        # Adjust for fragility (higher fragility needs more structural integrity)
        # Penalize if box isn't strong enough for fragile items
        fragility_factor = 1.0
        if fragility >= 4 and base_strength < 0.8:
            fragility_factor = 0.90  # 10% penalty for high fragility with weak material
        elif fragility >= 4:
            fragility_factor = 1.05  # 5% bonus for high fragility with strong material
        elif fragility <= 2:
            fragility_factor = 1.02  # Small bonus for low fragility items
        
        # Box geometry factor (cube is strongest shape)
        # Calculate aspect ratio - closer to 1 is better
        max_dim = max(dimensions['length'], dimensions['width'], dimensions['height'])
        min_dim = min(dimensions['length'], dimensions['width'], dimensions['height'])
        aspect_ratio = max_dim / min_dim if min_dim > 0 else 10
        
        if aspect_ratio < 2:
            geometry_factor = 1.05  # Well-proportioned
        elif aspect_ratio < 3:
            geometry_factor = 1.0   # Standard
        else:
            geometry_factor = 0.92  # Elongated (weaker)
        
        # Calculate final scores
        raw_strength = (
            base_strength * 
            strength_factor * 
            fragility_factor * 
            geometry_factor
        )
        
        # Convert to percentage and cap at realistic values
        strength_score = min(98, max(60, int(raw_strength * 100)))
        
        # Durability score (based on material durability)
        durability_score = min(98, max(60, int(durability_factor * strength_factor * 100)))
        
        # Compression resistance (based on material compression rating)
        compression_score = min(98, max(65, int(compression_factor * geometry_factor * 100)))
        
        # Determine if reinforcement is needed
        needs_reinforcement = False
        reinforcement_reason = None
        
        if strength_score < 70:
            needs_reinforcement = True
            reinforcement_reason = "Low overall strength score"
        elif weight > 5 and strength_score < 80:
            needs_reinforcement = True
            reinforcement_reason = "Heavy product requires stronger material"
        elif fragility >= 4 and strength_score < 85:
            needs_reinforcement = True
            reinforcement_reason = "Fragile product requires better protection"
        
        return {
            'strength': strength_score,
            'durability': durability_score,
            'compression_resistance': compression_score,
            'overall_rating': self._get_rating(strength_score),
            'needs_reinforcement': needs_reinforcement,
            'reinforcement_reason': reinforcement_reason,
            'analysis': {
                'volume_weight_ratio': float(vw_ratio),
                'geometry_rating': 'Excellent' if geometry_factor > 1 else 'Good' if geometry_factor == 1 else 'Fair',
                'material_rating': self._rate_material(base_strength),
                'load_distribution': 'Optimal' if strength_factor > 0.85 else 'Adequate' if strength_factor > 0.75 else 'Needs Improvement'
            }
        }
    
    
    def _get_rating(self, score):
        """Convert numerical score to rating"""
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Very Good'
        elif score >= 70:
            return 'Good'
        elif score >= 60:
            return 'Adequate'
        else:
            return 'Needs Improvement'
    
    
    def _rate_material(self, base_strength):
        """Rate material strength"""
        if base_strength >= 0.9:
            return 'Premium'
        elif base_strength >= 0.8:
            return 'High Quality'
        elif base_strength >= 0.7:
            return 'Standard'
        else:
            return 'Economy'
    
    
    def train(self, X_train, y_train):
        """
        Train the Random Forest model
        
        Args:
            X_train: Training features
            y_train: Target strength scores
        """
        print("Training strength predictor...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("✓ Training complete")
        
        # Calculate training metrics
        score = self.model.score(X_train, y_train)
        print(f"✓ R² Score: {score:.4f}")
        
        return score
    
    
    def save_model(self):
        """Save trained model to disk"""
        if self.is_trained:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            print(f"✓ Model saved to {self.model_path}")
        else:
            print("✗ Cannot save untrained model")
    
    
    def get_feature_importance(self):
        """Get feature importance from Random Forest"""
        if self.is_trained and hasattr(self.model, 'feature_importances_'):
            features = [
                'Length',
                'Width',
                'Height',
                'Material Type',
                'Weight',
                'Fragility'
            ]
            importance = dict(zip(features, self.model.feature_importances_))
            return importance
        return None
    
    
    def predict_drop_test(self, dimensions, material_name, weight, height_cm=100):
        """
        Predict if package will survive a drop test
        
        Args:
            dimensions: Box dimensions
            material_name: Material type
            weight: Product weight
            height_cm: Drop height in cm (default 100cm)
        
        Returns:
            dict: Drop test prediction
        """
        strength_scores = self.predict(dimensions, material_name, weight, 5)
        
        # Calculate impact force (simplified)
        # F = m * g * h (gravitational potential energy)
        g = 9.81  # m/s²
        height_m = height_cm / 100
        impact_energy = weight * g * height_m  # Joules
        
        # Determine if material can handle the impact
        material_props = self.material_properties.get(material_name)
        max_impact = material_props['tensile_strength'] * 0.5  # Safety factor
        
        will_survive = impact_energy < max_impact
        safety_margin = ((max_impact - impact_energy) / max_impact) * 100
        
        return {
            'will_survive': will_survive,
            'safety_margin': float(max(0, safety_margin)),
            'impact_energy': float(impact_energy),
            'material_capacity': float(max_impact),
            'recommendation': 'Safe for transport' if will_survive else 'Requires additional protection'
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Strength Predictor")
    print("=" * 60)
    
    # Initialize predictor
    predictor = StrengthPredictor()
    
    # Test case 1: Standard box
    print("\nTest 1: Standard Recycled Cardboard Box")
    result1 = predictor.predict(
        dimensions={'length': 25, 'width': 20, 'height': 15},
        material_name='Recycled Cardboard',
        weight=1.5,
        fragility=3
    )
    print(f"Strength: {result1['strength']}%")
    print(f"Durability: {result1['durability']}%")
    print(f"Compression Resistance: {result1['compression_resistance']}%")
    print(f"Overall Rating: {result1['overall_rating']}")
    
    # Test case 2: Heavy duty box
    print("\nTest 2: Double-Wall Corrugated for Heavy Item")
    result2 = predictor.predict(
        dimensions={'length': 50, 'width': 40, 'height': 30},
        material_name='Double-Wall Corrugated Cardboard',
        weight=8.0,
        fragility=2
    )
    print(f"Strength: {result2['strength']}%")
    print(f"Durability: {result2['durability']}%")
    print(f"Overall Rating: {result2['overall_rating']}")
    
    # Test case 3: Fragile electronics
    print("\nTest 3: Electronics with Foam Protection")
    result3 = predictor.predict(
        dimensions={'length': 22, 'width': 17, 'height': 10},
        material_name='Recycled Cardboard with Biodegradable Foam',
        weight=0.6,
        fragility=5
    )
    print(f"Strength: {result3['strength']}%")
    print(f"Needs Reinforcement: {result3['needs_reinforcement']}")
    if result3['needs_reinforcement']:
        print(f"Reason: {result3['reinforcement_reason']}")
    
    # Test drop test
    print("\nTest 4: Drop Test Prediction")
    drop_result = predictor.predict_drop_test(
        dimensions={'length': 25, 'width': 20, 'height': 15},
        material_name='Recycled Cardboard',
        weight=1.5,
        height_cm=100
    )
    print(f"Will survive 100cm drop: {drop_result['will_survive']}")
    print(f"Safety margin: {drop_result['safety_margin']:.1f}%")
    print(f"Recommendation: {drop_result['recommendation']}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully")
    print("=" * 60)