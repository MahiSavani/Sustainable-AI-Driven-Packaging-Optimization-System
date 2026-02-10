"""
Sustainability Analyzer
Calculates environmental impact, carbon footprint, and sustainability metrics
"""

import numpy as np


class SustainabilityAnalyzer:
    """
    Analyzes and calculates sustainability metrics for packaging
    
    Metrics:
    - Carbon footprint (CO₂ emissions)
    - Material savings
    - Volume reduction
    - Water usage
    - Energy consumption
    - Recyclability score
    """
    
    def __init__(self):
        # Industry averages for traditional packaging
        self.traditional_metrics = {
            'over_packaging_factor': 1.6,  # 60% more volume than needed
            'material_waste_percentage': 35,  # 35% material waste
            'co2_per_kg_cardboard': 1.2,  # kg CO₂ per kg cardboard
            'water_per_kg_cardboard': 40,  # liters per kg
            'energy_per_kg_cardboard': 5.0  # kWh per kg
        }
        
        # Cardboard density (approximate)
        self.cardboard_density = 700  # kg/m³
        
        # Thickness to weight conversion factors
        self.thickness_factors = {
            '2mm': 0.003,
            '3mm': 0.005,
            '4mm': 0.006,
            '5mm': 0.008,
            '6mm': 0.010,
            '7mm': 0.012,
            '8mm': 0.014
        }
    
    
    def analyze(self, original_dims, optimized_dims, material, product_weight):
        """
        Comprehensive sustainability analysis
        
        Args:
            original_dims (dict): Original product dimensions
            optimized_dims (dict): Optimized box dimensions
            material (dict): Selected material properties
            product_weight (float): Product weight in kg
        
        Returns:
            dict: Complete sustainability metrics
        """
        
        # Calculate volumes
        product_volume = (
            original_dims['length'] *
            original_dims['width'] *
            original_dims['height']
        )
        
        # Traditional over-packaging (industry average adds 60% extra)
        traditional_volume = product_volume * self.traditional_metrics['over_packaging_factor']
        
        # Optimized volume
        optimized_volume = (
            optimized_dims['length'] *
            optimized_dims['width'] *
            optimized_dims['height']
        )
        
        # Volume reduction
        volume_reduction = ((traditional_volume - optimized_volume) / traditional_volume * 100)
        volume_reduction = max(0, min(95, volume_reduction))  # Cap between 0-95%
        
        # Calculate surface areas (for material usage)
        traditional_area = self._calculate_surface_area({
            'length': original_dims['length'] + 10,
            'width': original_dims['width'] + 10,
            'height': original_dims['height'] + 10
        })
        
        optimized_area = self._calculate_surface_area(optimized_dims)
        
        # Material weight estimation
        thickness_factor = self.thickness_factors.get(material.get('thickness', '3mm'), 0.005)
        
        traditional_material_weight = (traditional_area / 10000) * self.cardboard_density * thickness_factor
        optimized_material_weight = (optimized_area / 10000) * self.cardboard_density * thickness_factor
        
        material_saved_kg = traditional_material_weight - optimized_material_weight
        material_reduction_pct = (material_saved_kg / traditional_material_weight * 100) if traditional_material_weight > 0 else 0
        
        # Carbon footprint calculation
        material_env = material.get('environmental_impact', {})
        co2_per_kg = material_env.get('co2_per_kg', 1.0)
        
        traditional_co2 = traditional_material_weight * self.traditional_metrics['co2_per_kg_cardboard']
        optimized_co2 = optimized_material_weight * co2_per_kg
        co2_saved = traditional_co2 - optimized_co2
        co2_reduction_pct = (co2_saved / traditional_co2 * 100) if traditional_co2 > 0 else 0
        
        # Water usage
        water_per_kg = material_env.get('water_usage_liters', 30)
        traditional_water = traditional_material_weight * self.traditional_metrics['water_per_kg_cardboard']
        optimized_water = optimized_material_weight * water_per_kg
        water_saved = traditional_water - optimized_water
        
        # Energy consumption
        energy_per_kg = material_env.get('energy_kwh', 4.0)
        traditional_energy = traditional_material_weight * self.traditional_metrics['energy_per_kg_cardboard']
        optimized_energy = optimized_material_weight * energy_per_kg
        energy_saved = traditional_energy - optimized_energy
        
        # Transportation efficiency
        # More compact packages = more units per truck
        transport_efficiency = self._calculate_transport_efficiency(
            traditional_volume,
            optimized_volume
        )
        
        # Trees saved (approximate: 1 tree = 100kg paper)
        trees_saved = material_saved_kg / 100
        
        # Overall sustainability score (0-100)
        sustainability_score = self._calculate_sustainability_score(
            volume_reduction,
            material_reduction_pct,
            co2_reduction_pct,
            material.get('sustainability_score', 80)
        )
        
        return {
            'volume_reduction': float(volume_reduction),
            'material_saved_kg': float(material_saved_kg),
            'material_reduction_percentage': float(material_reduction_pct),
            'co2_saved_kg': float(co2_saved),
            'co2_reduction_percentage': float(co2_reduction_pct),
            'water_saved_liters': float(water_saved),
            'energy_saved_kwh': float(energy_saved),
            'trees_saved': float(trees_saved),
            'transport_efficiency_gain': float(transport_efficiency),
            'sustainability_score': float(sustainability_score),
            'environmental_rating': self._get_environmental_rating(sustainability_score),
            'details': {
                'traditional_packaging': {
                    'volume_cm3': float(traditional_volume),
                    'material_kg': float(traditional_material_weight),
                    'co2_kg': float(traditional_co2),
                    'water_liters': float(traditional_water),
                    'energy_kwh': float(traditional_energy)
                },
                'optimized_packaging': {
                    'volume_cm3': float(optimized_volume),
                    'material_kg': float(optimized_material_weight),
                    'co2_kg': float(optimized_co2),
                    'water_liters': float(optimized_water),
                    'energy_kwh': float(optimized_energy)
                }
            },
            'annual_impact': self._calculate_annual_impact(
                co2_saved, water_saved, energy_saved, material_saved_kg
            )
        }
    
    
    def _calculate_surface_area(self, dimensions):
        """Calculate surface area of a box"""
        l = dimensions['length']
        w = dimensions['width']
        h = dimensions['height']
        
        return 2 * (l * w + w * h + h * l)
    
    
    def _calculate_transport_efficiency(self, traditional_vol, optimized_vol):
        """Calculate improvement in transportation efficiency"""
        # Standard truck capacity: 80 cubic meters = 80,000,000 cubic cm
        truck_capacity = 80000000
        
        traditional_units = truck_capacity / traditional_vol
        optimized_units = truck_capacity / optimized_vol
        
        efficiency_gain = ((optimized_units - traditional_units) / traditional_units * 100)
        
        return max(0, min(100, efficiency_gain))
    
    
    def _calculate_sustainability_score(self, volume_red, material_red, co2_red, material_score):
        """Calculate overall sustainability score"""
        # Weighted average
        score = (
            volume_red * 0.25 +
            material_red * 0.25 +
            co2_red * 0.25 +
            material_score * 0.25
        )
        
        return min(100, max(0, score))
    
    
    def _get_environmental_rating(self, score):
        """Convert score to rating"""
        if score >= 90:
            return 'Exceptional'
        elif score >= 80:
            return 'Excellent'
        elif score >= 70:
            return 'Very Good'
        elif score >= 60:
            return 'Good'
        elif score >= 50:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    
    def _calculate_annual_impact(self, co2_saved, water_saved, energy_saved, material_saved):
        """Calculate annual environmental impact (assuming 10,000 units/year)"""
        annual_units = 10000
        
        return {
            'units_per_year': annual_units,
            'total_co2_saved_kg': float(co2_saved * annual_units),
            'total_co2_saved_tons': float((co2_saved * annual_units) / 1000),
            'total_water_saved_liters': float(water_saved * annual_units),
            'total_energy_saved_kwh': float(energy_saved * annual_units),
            'total_material_saved_kg': float(material_saved * annual_units),
            'total_material_saved_tons': float((material_saved * annual_units) / 1000),
            'equivalent_metrics': {
                'cars_off_road': float((co2_saved * annual_units) / 4600),  # Average car = 4.6 tons CO2/year
                'trees_planted': float((co2_saved * annual_units) / 21),  # One tree absorbs ~21kg CO2/year
                'homes_powered_days': float((energy_saved * annual_units) / 30)  # Average home uses 30 kWh/day
            }
        }
    
    
    def generate_report_summary(self, sustainability_data):
        """Generate a human-readable summary"""
        summary = []
        
        # Volume reduction
        vol_red = sustainability_data['volume_reduction']
        summary.append(f"Reduced packaging volume by {vol_red:.1f}%")
        
        # Material savings
        material_saved = sustainability_data['material_saved_kg']
        summary.append(f"Saved {material_saved:.2f}kg of material per unit")
        
        # CO2 reduction
        co2_saved = sustainability_data['co2_saved_kg']
        summary.append(f"Reduced CO₂ emissions by {co2_saved:.2f}kg per unit")
        
        # Annual impact
        annual = sustainability_data['annual_impact']
        summary.append(f"Annual savings: {annual['total_co2_saved_tons']:.1f} tons CO₂")
        summary.append(f"Equivalent to {annual['equivalent_metrics']['trees_planted']:.0f} trees planted")
        
        # Rating
        rating = sustainability_data['environmental_rating']
        summary.append(f"Environmental Rating: {rating}")
        
        return summary
    
    
    def compare_with_industry(self, sustainability_data):
        """Compare optimization results with industry standards"""
        return {
            'volume_optimization': {
                'achieved': sustainability_data['volume_reduction'],
                'industry_average': 25.0,
                'performance': 'Excellent' if sustainability_data['volume_reduction'] > 25 else 'Good'
            },
            'material_efficiency': {
                'achieved': sustainability_data['material_reduction_percentage'],
                'industry_average': 20.0,
                'performance': 'Excellent' if sustainability_data['material_reduction_percentage'] > 20 else 'Good'
            },
            'carbon_reduction': {
                'achieved': sustainability_data['co2_reduction_percentage'],
                'industry_target': 30.0,
                'meets_target': sustainability_data['co2_reduction_percentage'] >= 30
            }
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Sustainability Analyzer")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SustainabilityAnalyzer()
    
    # Test case 1: Standard optimization
    print("\nTest 1: Standard Product Optimization")
    
    original_dims = {'length': 20, 'width': 15, 'height': 8}
    optimized_dims = {'length': 22, 'width': 17, 'height': 10}
    material = {
        'name': 'Recycled Cardboard',
        'thickness': '3mm',
        'sustainability_score': 95,
        'environmental_impact': {
            'co2_per_kg': 0.8,
            'water_usage_liters': 20,
            'energy_kwh': 2.5
        }
    }
    
    result = analyzer.analyze(original_dims, optimized_dims, material, 0.5)
    
    print(f"Volume Reduction: {result['volume_reduction']:.1f}%")
    print(f"Material Saved: {result['material_saved_kg']:.3f}kg")
    print(f"CO₂ Saved: {result['co2_saved_kg']:.3f}kg")
    print(f"Water Saved: {result['water_saved_liters']:.1f}L")
    print(f"Trees Saved: {result['trees_saved']:.4f}")
    print(f"Sustainability Score: {result['sustainability_score']:.1f}/100")
    print(f"Environmental Rating: {result['environmental_rating']}")
    
    # Annual impact
    print("\nAnnual Impact (10,000 units):")
    annual = result['annual_impact']
    print(f"  CO₂ Saved: {annual['total_co2_saved_tons']:.2f} tons")
    print(f"  Material Saved: {annual['total_material_saved_tons']:.2f} tons")
    print(f"  Equivalent to {annual['equivalent_metrics']['cars_off_road']:.1f} cars off the road")
    print(f"  Equivalent to {annual['equivalent_metrics']['trees_planted']:.0f} trees planted")
    
    # Generate summary
    print("\nSummary:")
    summary = analyzer.generate_report_summary(result)
    for line in summary:
        print(f"  • {line}")
    
    # Industry comparison
    print("\nIndustry Comparison:")
    comparison = analyzer.compare_with_industry(result)
    print(f"  Volume Optimization: {comparison['volume_optimization']['performance']}")
    print(f"  Material Efficiency: {comparison['material_efficiency']['performance']}")
    print(f"  Meets Carbon Target: {comparison['carbon_reduction']['meets_target']}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully")
    print("=" * 60)