"""
Dimension Optimizer - Linear Regression Model
Calculates optimal box dimensions based on product specifications
"""

import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os


class DimensionOptimizer:
    """
    Uses Linear Regression to predict optimal packaging dimensions
    
    Features:
    - Product length, width, height
    - Product weight
    - Fragility level (1-5)
    
    Target:
    - Optimal box length, width, height
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.model_path = 'models/trained/dimension_model.pkl'
        
        # Try to load pre-trained model
        self._load_model()
    
    
    def _load_model(self):
        """Load pre-trained model if exists"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                print("✓ Dimension model loaded from disk")
            except Exception as e:
                print(f"✗ Error loading model: {e}")
                self._initialize_model()
        else:
            self._initialize_model()
    
    
    def _initialize_model(self):
        """Initialize a new Linear Regression model"""
        self.model = LinearRegression()
        print("✓ New dimension model initialized")
    
    
    def optimize(self, product_length, product_width, product_height, weight, fragility):
        """
        Calculate optimal packaging dimensions
        
        Args:
            product_length (float): Product length in cm
            product_width (float): Product width in cm
            product_height (float): Product height in cm
            weight (float): Product weight in kg
            fragility (int): Fragility level (1-5, where 5 is most fragile)
        
        Returns:
            dict: Optimized dimensions {'length', 'width', 'height'}
        """
        
        # Padding calculation based on fragility and weight
        # Higher fragility = more protective padding needed
        padding_multiplier = {
            1: 1.5,   # Very low fragility - minimal padding
            2: 2.0,   # Low fragility - light padding
            3: 2.5,   # Medium fragility - moderate padding
            4: 3.0,   # High fragility - substantial padding
            5: 3.5    # Very high fragility - maximum padding
        }
        
        base_padding = padding_multiplier.get(fragility, 2.5)
        
        # Weight-based adjustment
        # Heavier items need stronger boxes with more material
        if weight > 10:
            weight_factor = 2.0
        elif weight > 5:
            weight_factor = 1.5
        elif weight > 2:
            weight_factor = 1.0
        else:
            weight_factor = 0.5
        
        # Calculate total padding per dimension
        padding_length = base_padding + weight_factor
        padding_width = base_padding + weight_factor
        padding_height = base_padding + weight_factor
        
        # Calculate optimal dimensions
        # Round up to nearest cm for practical manufacturing
        optimal_length = np.ceil(product_length + padding_length)
        optimal_width = np.ceil(product_width + padding_width)
        optimal_height = np.ceil(product_height + padding_height)
        
        # Ensure minimum dimensions (at least 5cm on each side)
        optimal_length = max(optimal_length, 5.0)
        optimal_width = max(optimal_width, 5.0)
        optimal_height = max(optimal_height, 5.0)
        
        # Calculate efficiency metrics
        product_volume = product_length * product_width * product_height
        box_volume = optimal_length * optimal_width * optimal_height
        space_utilization = (product_volume / box_volume) * 100
        
        return {
            'length': float(optimal_length),
            'width': float(optimal_width),
            'height': float(optimal_height),
            'volume': float(box_volume),
            'space_utilization': float(space_utilization),
            'padding_applied': {
                'length': float(padding_length),
                'width': float(padding_width),
                'height': float(padding_height)
            }
        }
    
    
    def train(self, X_train, y_train):
        """
        Train the Linear Regression model
        
        Args:
            X_train: Training features (product dimensions, weight, fragility)
            y_train: Target values (optimal box dimensions)
        """
        print("Training dimension optimizer...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("✓ Training complete")
        
        # Calculate training metrics
        score = self.model.score(X_train, y_train)
        print(f"✓ R² Score: {score:.4f}")
        
        return score
    
    
    def predict_ml(self, product_dims, weight, fragility):
        """
        Predict using trained ML model (when available)
        
        Args:
            product_dims: [length, width, height]
            weight: Product weight
            fragility: Fragility level
        
        Returns:
            Predicted optimal dimensions
        """
        if not self.is_trained:
            print("Model not trained, using rule-based approach")
            return self.optimize(
                product_dims[0], product_dims[1], product_dims[2],
                weight, fragility
            )
        
        # Prepare features
        features = np.array([[
            product_dims[0],
            product_dims[1],
            product_dims[2],
            weight,
            fragility
        ]])
        
        # Predict
        prediction = self.model.predict(features)[0]
        
        return {
            'length': float(prediction[0]),
            'width': float(prediction[1]),
            'height': float(prediction[2])
        }
    
    
    def save_model(self):
        """Save trained model to disk"""
        if self.is_trained:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            print(f"✓ Model saved to {self.model_path}")
        else:
            print("✗ Cannot save untrained model")
    
    
    def get_feature_importance(self):
        """Get feature coefficients (for linear regression)"""
        if self.is_trained and hasattr(self.model, 'coef_'):
            features = [
                'Product Length',
                'Product Width',
                'Product Height',
                'Weight',
                'Fragility'
            ]
            coefficients = self.model.coef_
            
            importance = dict(zip(features, coefficients[0]))
            return importance
        return None
    
    
    def calculate_material_savings(self, original_dims, optimized_dims):
        """
        Calculate material savings from optimization
        
        Args:
            original_dims: Original/traditional box dimensions
            optimized_dims: Optimized dimensions
        
        Returns:
            dict: Savings metrics
        """
        # Calculate surface areas
        original_area = 2 * (
            original_dims['length'] * original_dims['width'] +
            original_dims['width'] * original_dims['height'] +
            original_dims['height'] * original_dims['length']
        )
        
        optimized_area = 2 * (
            optimized_dims['length'] * optimized_dims['width'] +
            optimized_dims['width'] * optimized_dims['height'] +
            optimized_dims['height'] * optimized_dims['length']
        )
        
        area_saved = original_area - optimized_area
        percentage_saved = (area_saved / original_area) * 100
        
        # Calculate volume savings
        original_volume = (
            original_dims['length'] *
            original_dims['width'] *
            original_dims['height']
        )
        
        optimized_volume = (
            optimized_dims['length'] *
            optimized_dims['width'] *
            optimized_dims['height']
        )
        
        volume_saved = original_volume - optimized_volume
        volume_percentage = (volume_saved / original_volume) * 100
        
        return {
            'area_saved_cm2': float(area_saved),
            'area_percentage': float(percentage_saved),
            'volume_saved_cm3': float(volume_saved),
            'volume_percentage': float(volume_percentage)
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Dimension Optimizer")
    print("=" * 60)
    
    # Initialize optimizer
    optimizer = DimensionOptimizer()
    
    # Test case 1: Electronics (Headphones)
    print("\nTest 1: Wireless Headphones")
    result1 = optimizer.optimize(
        product_length=18,
        product_width=14,
        product_height=7,
        weight=0.5,
        fragility=4
    )
    print(f"Optimal dimensions: {result1['length']} x {result1['width']} x {result1['height']} cm")
    print(f"Space utilization: {result1['space_utilization']:.2f}%")
    
    # Test case 2: Book
    print("\nTest 2: Textbook")
    result2 = optimizer.optimize(
        product_length=24,
        product_width=18,
        product_height=4,
        weight=1.2,
        fragility=2
    )
    print(f"Optimal dimensions: {result2['length']} x {result2['width']} x {result2['height']} cm")
    print(f"Space utilization: {result2['space_utilization']:.2f}%")
    
    # Test case 3: Heavy item
    print("\nTest 3: Heavy Equipment")
    result3 = optimizer.optimize(
        product_length=40,
        product_width=30,
        product_height=25,
        weight=8.5,
        fragility=3
    )
    print(f"Optimal dimensions: {result3['length']} x {result3['width']} x {result3['height']} cm")
    print(f"Space utilization: {result3['space_utilization']:.2f}%")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully")
    print("=" * 60)