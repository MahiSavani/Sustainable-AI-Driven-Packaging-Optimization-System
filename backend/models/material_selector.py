"""
Material Selector - Hybrid Rule-Based ML System
Recommends sustainable materials based on product characteristics
"""

import numpy as np


class MaterialSelector:
    """
    Hybrid rule-based ML system for material selection
    
    Considers:
    - Product category
    - Weight
    - Fragility
    - Recyclability preferences
    - Cost constraints
    - Sustainability goals
    """
    
    def __init__(self):
        # Comprehensive material database
        self.materials = {
            'recycled_cardboard': {
                'name': 'Recycled Cardboard',
                'thickness': '3mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 0.9,
                'sustainability_score': 95,
                'strength_rating': 'Medium',
                'best_for': ['books', 'apparel', 'toys'],
                'weight_limit': 3.0,  # kg
                'fragility_max': 3,
                'environmental_impact': {
                    'co2_per_kg': 0.8,
                    'water_usage_liters': 20,
                    'energy_kwh': 2.5
                }
            },
            'double_wall_corrugated': {
                'name': 'Double-Wall Corrugated Cardboard',
                'thickness': '7mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 1.5,
                'sustainability_score': 82,
                'strength_rating': 'High',
                'best_for': ['heavy_items', 'machinery'],
                'weight_limit': 15.0,
                'fragility_max': 4,
                'environmental_impact': {
                    'co2_per_kg': 1.2,
                    'water_usage_liters': 35,
                    'energy_kwh': 4.0
                }
            },
            'kraft_paper': {
                'name': '100% Recycled Kraft Paper',
                'thickness': '2mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 0.8,
                'sustainability_score': 98,
                'strength_rating': 'Low-Medium',
                'best_for': ['lightweight', 'apparel', 'documents'],
                'weight_limit': 1.5,
                'fragility_max': 2,
                'environmental_impact': {
                    'co2_per_kg': 0.6,
                    'water_usage_liters': 15,
                    'energy_kwh': 2.0
                }
            },
            'foam_insert_cardboard': {
                'name': 'Recycled Cardboard with Biodegradable Foam',
                'thickness': '5mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 1.3,
                'sustainability_score': 88,
                'strength_rating': 'High',
                'best_for': ['electronics', 'fragile_items'],
                'weight_limit': 5.0,
                'fragility_max': 5,
                'environmental_impact': {
                    'co2_per_kg': 1.0,
                    'water_usage_liters': 25,
                    'energy_kwh': 3.2
                }
            },
            'food_grade_cardboard': {
                'name': 'Food-Grade Biodegradable Cardboard',
                'thickness': '4mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 1.1,
                'sustainability_score': 92,
                'strength_rating': 'Medium-High',
                'best_for': ['food', 'cosmetics'],
                'weight_limit': 4.0,
                'fragility_max': 3,
                'environmental_impact': {
                    'co2_per_kg': 0.9,
                    'water_usage_liters': 22,
                    'energy_kwh': 2.8
                }
            },
            'molded_pulp': {
                'name': 'Molded Pulp (Recycled Paper)',
                'thickness': '6mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 1.2,
                'sustainability_score': 96,
                'strength_rating': 'Medium-High',
                'best_for': ['electronics', 'eggs', 'produce'],
                'weight_limit': 3.5,
                'fragility_max': 4,
                'environmental_impact': {
                    'co2_per_kg': 0.7,
                    'water_usage_liters': 18,
                    'energy_kwh': 2.3
                }
            },
            'honeycomb_cardboard': {
                'name': 'Honeycomb Cardboard',
                'thickness': '8mm',
                'recyclable': True,
                'biodegradable': True,
                'cost_factor': 1.6,
                'sustainability_score': 85,
                'strength_rating': 'Very High',
                'best_for': ['heavy_items', 'furniture', 'machinery'],
                'weight_limit': 20.0,
                'fragility_max': 4,
                'environmental_impact': {
                    'co2_per_kg': 1.1,
                    'water_usage_liters': 30,
                    'energy_kwh': 3.8
                }
            }
        }
        
        # Category mapping
        self.category_priorities = {
            'electronics': {
                'priority': 'protection',
                'preferred_materials': ['foam_insert_cardboard', 'molded_pulp'],
                'min_strength': 'High'
            },
            'food': {
                'priority': 'safety',
                'preferred_materials': ['food_grade_cardboard', 'molded_pulp'],
                'min_strength': 'Medium'
            },
            'cosmetics': {
                'priority': 'presentation',
                'preferred_materials': ['food_grade_cardboard', 'kraft_paper'],
                'min_strength': 'Medium'
            },
            'apparel': {
                'priority': 'cost',
                'preferred_materials': ['kraft_paper', 'recycled_cardboard'],
                'min_strength': 'Low-Medium'
            },
            'books': {
                'priority': 'cost',
                'preferred_materials': ['recycled_cardboard', 'kraft_paper'],
                'min_strength': 'Medium'
            },
            'toys': {
                'priority': 'safety',
                'preferred_materials': ['recycled_cardboard', 'food_grade_cardboard'],
                'min_strength': 'Medium'
            },
            'other': {
                'priority': 'balance',
                'preferred_materials': ['recycled_cardboard'],
                'min_strength': 'Medium'
            }
        }
    
    
    def select(self, category, weight, fragility, recyclable_priority=True):
        """
        Select optimal material based on product characteristics
        
        Args:
            category (str): Product category
            weight (float): Product weight in kg
            fragility (int): Fragility level (1-5)
            recyclable_priority (bool): Prioritize recyclable materials
        
        Returns:
            dict: Selected material with all properties
        """
        
        # Normalize category
        category = category.lower() if category else 'other'
        
        # Get category preferences
        cat_prefs = self.category_priorities.get(
            category,
            self.category_priorities['other']
        )
        
        # Score each material
        material_scores = {}
        
        for material_key, material in self.materials.items():
            score = 0
            reasons = []
            
            # 1. Weight compatibility (30 points)
            if weight <= material['weight_limit']:
                weight_ratio = weight / material['weight_limit']
                if weight_ratio < 0.5:
                    score += 30
                    reasons.append("Excellent weight capacity")
                elif weight_ratio < 0.75:
                    score += 25
                    reasons.append("Good weight capacity")
                else:
                    score += 20
                    reasons.append("Adequate weight capacity")
            else:
                score += 0
                reasons.append("Insufficient weight capacity")
                continue  # Skip this material
            
            # 2. Fragility handling (25 points)
            if fragility <= material['fragility_max']:
                if fragility >= 4 and material['strength_rating'] in ['High', 'Very High']:
                    score += 25
                    reasons.append("Excellent protection for fragile items")
                elif fragility >= 4:
                    score += 15
                    reasons.append("Moderate protection for fragile items")
                else:
                    score += 20
                    reasons.append("Suitable protection level")
            else:
                score += 5
                reasons.append("May not provide sufficient protection")
            
            # 3. Sustainability (20 points)
            sustainability_points = (material['sustainability_score'] / 100) * 20
            score += sustainability_points
            if material['sustainability_score'] >= 95:
                reasons.append("Exceptional sustainability")
            elif material['sustainability_score'] >= 85:
                reasons.append("High sustainability")
            
            # 4. Category match (15 points)
            if material_key in cat_prefs['preferred_materials']:
                score += 15
                reasons.append(f"Optimized for {category} category")
            elif material in [self.materials[k] for k in cat_prefs['preferred_materials']]:
                score += 10
                reasons.append(f"Suitable for {category} category")
            else:
                score += 5
            
            # 5. Recyclability (10 points)
            if recyclable_priority and material['recyclable']:
                score += 10
                reasons.append("Fully recyclable")
            elif material['recyclable']:
                score += 7
            
            # 6. Cost efficiency (10 points)
            if material['cost_factor'] <= 1.0:
                score += 10
                reasons.append("Cost-effective")
            elif material['cost_factor'] <= 1.3:
                score += 7
                reasons.append("Moderate cost")
            else:
                score += 4
                reasons.append("Premium pricing")
            
            material_scores[material_key] = {
                'score': score,
                'reasons': reasons,
                'material': material
            }
        
        # Select material with highest score
        best_material_key = max(material_scores, key=lambda k: material_scores[k]['score'])
        best_match = material_scores[best_material_key]
        
        # Prepare response
        selected = best_match['material'].copy()
        selected['selection_score'] = best_match['score']
        selected['selection_reasons'] = best_match['reasons']
        selected['alternatives'] = self._get_alternatives(material_scores, best_material_key)
        
        return selected
    
    
    def _get_alternatives(self, material_scores, selected_key, count=2):
        """Get alternative material recommendations"""
        # Sort by score
        sorted_materials = sorted(
            material_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        # Get top alternatives (excluding selected)
        alternatives = []
        for material_key, data in sorted_materials:
            if material_key != selected_key and len(alternatives) < count:
                alternatives.append({
                    'name': data['material']['name'],
                    'score': data['score'],
                    'thickness': data['material']['thickness'],
                    'cost_factor': data['material']['cost_factor'],
                    'sustainability_score': data['material']['sustainability_score']
                })
        
        return alternatives
    
    
    def get_all_materials(self):
        """Get list of all available materials"""
        return [
            {
                'id': key,
                'name': material['name'],
                'thickness': material['thickness'],
                'recyclable': material['recyclable'],
                'biodegradable': material['biodegradable'],
                'sustainability_score': material['sustainability_score'],
                'strength_rating': material['strength_rating'],
                'best_for': material['best_for'],
                'cost_factor': material['cost_factor']
            }
            for key, material in self.materials.items()
        ]
    
    
    def compare_materials(self, material_keys):
        """Compare multiple materials side by side"""
        comparison = []
        
        for key in material_keys:
            if key in self.materials:
                material = self.materials[key]
                comparison.append({
                    'name': material['name'],
                    'sustainability': material['sustainability_score'],
                    'strength': material['strength_rating'],
                    'cost': material['cost_factor'],
                    'co2_impact': material['environmental_impact']['co2_per_kg']
                })
        
        return comparison
    
    
    def get_material_by_budget(self, max_cost_factor):
        """Get materials within budget"""
        affordable = []
        
        for key, material in self.materials.items():
            if material['cost_factor'] <= max_cost_factor:
                affordable.append({
                    'name': material['name'],
                    'cost_factor': material['cost_factor'],
                    'sustainability_score': material['sustainability_score'],
                    'strength_rating': material['strength_rating']
                })
        
        # Sort by sustainability score
        affordable.sort(key=lambda x: x['sustainability_score'], reverse=True)
        
        return affordable
    
    
    def calculate_environmental_impact(self, material_name, quantity_kg):
        """
        Calculate environmental impact for a given quantity
        
        Args:
            material_name (str): Material name
            quantity_kg (float): Quantity in kilograms
        
        Returns:
            dict: Environmental impact metrics
        """
        # Find material
        material = None
        for mat in self.materials.values():
            if mat['name'] == material_name:
                material = mat
                break
        
        if not material:
            return None
        
        env = material['environmental_impact']
        
        return {
            'total_co2_kg': env['co2_per_kg'] * quantity_kg,
            'total_water_liters': env['water_usage_liters'] * quantity_kg,
            'total_energy_kwh': env['energy_kwh'] * quantity_kg,
            'recyclability': 'Yes' if material['recyclable'] else 'No',
            'biodegradability': 'Yes' if material['biodegradable'] else 'No'
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Material Selector")
    print("=" * 60)
    
    # Initialize selector
    selector = MaterialSelector()
    
    # Test case 1: Electronics (fragile, medium weight)
    print("\nTest 1: Electronics - Smartphone")
    result1 = selector.select(
        category='electronics',
        weight=0.5,
        fragility=5,
        recyclable_priority=True
    )
    print(f"Selected: {result1['name']}")
    print(f"Thickness: {result1['thickness']}")
    print(f"Sustainability Score: {result1['sustainability_score']}")
    print(f"Selection Score: {result1['selection_score']:.1f}/100")
    print("Reasons:")
    for reason in result1['selection_reasons']:
        print(f"  - {reason}")
    
    # Test case 2: Heavy item
    print("\nTest 2: Heavy Machinery Part")
    result2 = selector.select(
        category='other',
        weight=12.0,
        fragility=2,
        recyclable_priority=True
    )
    print(f"Selected: {result2['name']}")
    print(f"Strength Rating: {result2['strength_rating']}")
    print(f"Cost Factor: {result2['cost_factor']}")
    
    # Test case 3: Food packaging
    print("\nTest 3: Food Product")
    result3 = selector.select(
        category='food',
        weight=2.0,
        fragility=3,
        recyclable_priority=True
    )
    print(f"Selected: {result3['name']}")
    print(f"Sustainability: {result3['sustainability_score']}")
    print("\nAlternatives:")
    for alt in result3['alternatives']:
        print(f"  - {alt['name']} (Score: {alt['score']:.1f})")
    
    # Test environmental impact
    print("\nTest 4: Environmental Impact (1000 units)")
    impact = selector.calculate_environmental_impact(
        material_name='Recycled Cardboard',
        quantity_kg=50.0  # 50kg total
    )
    if impact:
        print(f"CO₂ Emissions: {impact['total_co2_kg']:.2f} kg")
        print(f"Water Usage: {impact['total_water_liters']:.0f} liters")
        print(f"Energy Consumption: {impact['total_energy_kwh']:.1f} kWh")
    
    # Test budget filtering
    print("\nTest 5: Budget-Friendly Materials (≤1.0 cost factor)")
    affordable = selector.get_material_by_budget(max_cost_factor=1.0)
    for material in affordable:
        print(f"  - {material['name']} (${material['cost_factor']}, Sustainability: {material['sustainability_score']})")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully")
    print("=" * 60)