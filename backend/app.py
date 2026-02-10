"""
EcoPackAI Backend - Main Flask Application
AI-Powered Packaging Optimization System
4th Semester AIML Academic Project
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

# Import our AI models
from models.dimension_optimizer import DimensionOptimizer
from models.strength_predictor import StrengthPredictor
from models.material_selector import MaterialSelector
from models.sustainability_analyzer import SustainabilityAnalyzer

# Import utilities
from utils.validators import validate_product_input
from utils.helpers import generate_response, calculate_savings

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize AI models
dimension_optimizer = DimensionOptimizer()
strength_predictor = StrengthPredictor()
material_selector = MaterialSelector()
sustainability_analyzer = SustainabilityAnalyzer()

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['JSON_SORT_KEYS'] = False


# ==================== API ENDPOINTS ====================

@app.route('/')
def home():
    """Home endpoint - API information"""
    return jsonify({
        'message': 'EcoPackAI Backend API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'POST /api/optimize': 'Get optimized packaging design',
            'GET /api/materials': 'Get available materials',
            'POST /api/report': 'Generate sustainability report',
            'GET /api/health': 'Check API health'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models': {
            'dimension_optimizer': 'ready',
            'strength_predictor': 'ready',
            'material_selector': 'ready',
            'sustainability_analyzer': 'ready'
        }
    })


@app.route('/api/optimize', methods=['POST'])
def optimize_packaging():
    """
    Main optimization endpoint
    Accepts product details and returns optimized packaging design
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_product_input(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Extract product details
        product_name = data.get('product_name')
        length = float(data.get('length'))
        width = float(data.get('width'))
        height = float(data.get('height'))
        weight = float(data.get('weight'))
        category = data.get('category')
        fragility = int(data.get('fragility', 3))
        stackable = data.get('stackable', False)
        recyclable = data.get('recyclable', True)
        
        print(f"Processing optimization for: {product_name}")
        
        # Step 1: Optimize dimensions
        optimized_dims = dimension_optimizer.optimize(
            length, width, height, weight, fragility
        )
        print(f"Optimized dimensions: {optimized_dims}")
        
        # Step 2: Select material
        material = material_selector.select(
            category, weight, fragility, recyclable
        )
        print(f"Selected material: {material['name']}")
        
        # Step 3: Predict strength
        strength_scores = strength_predictor.predict(
            optimized_dims, material['name'], weight, fragility
        )
        print(f"Strength scores: {strength_scores}")
        
        # Step 4: Calculate sustainability
        original_dims = {'length': length, 'width': width, 'height': height}
        sustainability = sustainability_analyzer.analyze(
            original_dims, optimized_dims, material, weight
        )
        print(f"Sustainability metrics: {sustainability}")
        
        # Step 5: Calculate savings
        savings = calculate_savings(
            original_dims, optimized_dims, material, weight
        )
        
        # Prepare response
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'product': {
                'name': product_name,
                'original_dimensions': original_dims,
                'category': category,
                'weight': weight,
                'fragility': fragility
            },
            'optimized_design': {
                'dimensions': optimized_dims,
                'volume': optimized_dims['length'] * optimized_dims['width'] * optimized_dims['height'],
                'material': material,
                'strength_analysis': strength_scores
            },
            'sustainability': sustainability,
            'savings': savings,
            'recommendations': [
                f"Use {material['name']} for optimal sustainability",
                f"Reduce packaging volume by {sustainability['volume_reduction']:.1f}%",
                f"Save ${savings['cost_saving_amount']:.2f} per unit",
                "Consider stackable design for efficient storage" if stackable else None
            ]
        }
        
        # Remove None recommendations
        response['recommendations'] = [r for r in response['recommendations'] if r]
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in optimize_packaging: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get list of available materials with properties"""
    materials = material_selector.get_all_materials()
    return jsonify({
        'success': True,
        'count': len(materials),
        'materials': materials
    })


@app.route('/api/report', methods=['POST'])
def generate_report():
    """Generate detailed sustainability report"""
    try:
        data = request.get_json()
        
        # This would typically generate a PDF
        # For now, return comprehensive report data
        report_data = {
            'report_id': f"REPORT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'product_details': data.get('product'),
            'optimization_results': data.get('optimization'),
            'environmental_impact': {
                'co2_saved': data.get('sustainability', {}).get('co2_reduction', 0),
                'material_saved_kg': data.get('sustainability', {}).get('material_saved_kg', 0),
                'trees_saved': round(data.get('sustainability', {}).get('material_saved_kg', 0) * 0.05, 2),
                'water_saved_liters': round(data.get('sustainability', {}).get('material_saved_kg', 0) * 15, 2)
            },
            'economic_impact': {
                'cost_per_unit': data.get('savings', {}).get('cost_saving_amount', 0),
                'annual_savings': data.get('savings', {}).get('cost_saving_amount', 0) * 10000,
                'roi_months': 3
            },
            'recommendations': [
                'Implement optimized design immediately',
                'Consider bulk ordering of sustainable materials',
                'Train packaging team on new specifications',
                'Monitor and report monthly savings'
            ]
        }
        
        return jsonify({
            'success': True,
            'report': report_data,
            'download_url': '/api/download/report/' + report_data['report_id']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dieline', methods=['POST'])
def generate_dieline():
    """Generate 2D dieline data for manufacturing"""
    try:
        data = request.get_json()
        dimensions = data.get('dimensions', {})
        
        length = dimensions.get('length', 0)
        width = dimensions.get('width', 0)
        height = dimensions.get('height', 0)
        
        # Calculate dieline coordinates
        # This creates a standard box dieline pattern
        dieline = {
            'type': 'standard_box',
            'dimensions': dimensions,
            'panels': {
                'front': {'width': width, 'height': height},
                'back': {'width': width, 'height': height},
                'left': {'width': length, 'height': height},
                'right': {'width': length, 'height': height},
                'top': {'width': width, 'height': length},
                'bottom': {'width': width, 'height': length}
            },
            'fold_lines': [
                {'type': 'horizontal', 'position': height},
                {'type': 'horizontal', 'position': height * 2},
                {'type': 'vertical', 'position': width},
                {'type': 'vertical', 'position': width + length}
            ],
            'cut_lines': {
                'total_width': width * 2 + length * 2,
                'total_height': height * 2 + length
            },
            'material_area_cm2': (width * 2 + length * 2) * (height * 2 + length)
        }
        
        return jsonify({
            'success': True,
            'dieline': dieline,
            'export_formats': ['SVG', 'PDF', 'DXF', 'AI']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/3d-data', methods=['POST'])
def generate_3d_data():
    """Generate 3D visualization data"""
    try:
        data = request.get_json()
        dimensions = data.get('dimensions', {})
        
        # Generate vertices for 3D box
        length = dimensions.get('length', 0)
        width = dimensions.get('width', 0)
        height = dimensions.get('height', 0)
        
        # Box vertices (8 corners)
        vertices = [
            [0, 0, 0],
            [length, 0, 0],
            [length, width, 0],
            [0, width, 0],
            [0, 0, height],
            [length, 0, height],
            [length, width, height],
            [0, width, height]
        ]
        
        # Box faces (6 faces)
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [2, 3, 7, 6],  # back
            [0, 3, 7, 4],  # left
            [1, 2, 6, 5]   # right
        ]
        
        return jsonify({
            'success': True,
            'model': {
                'vertices': vertices,
                'faces': faces,
                'dimensions': dimensions,
                'center': [length/2, width/2, height/2]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch-optimize', methods=['POST'])
def batch_optimize():
    """Optimize multiple products at once"""
    try:
        data = request.get_json()
        products = data.get('products', [])
        
        if not products:
            return jsonify({'error': 'No products provided'}), 400
        
        results = []
        for product in products:
            # Validate each product
            is_valid, error = validate_product_input(product)
            if not is_valid:
                results.append({'error': error, 'product': product.get('product_name')})
                continue
            
            # Optimize each product
            optimized = dimension_optimizer.optimize(
                product['length'],
                product['width'],
                product['height'],
                product['weight'],
                product.get('fragility', 3)
            )
            
            results.append({
                'product_name': product.get('product_name'),
                'optimized_dimensions': optimized,
                'status': 'success'
            })
        
        return jsonify({
            'success': True,
            'total_products': len(products),
            'successful': len([r for r in results if 'error' not in r]),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🌱 EcoPackAI Backend Server Starting...")
    print("=" * 60)
    print("✓ AI Models Loaded")
    print("✓ API Endpoints Ready")
    print("✓ CORS Enabled")
    print("=" * 60)
    print("🚀 Server running on http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/")
    print("=" * 60)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )