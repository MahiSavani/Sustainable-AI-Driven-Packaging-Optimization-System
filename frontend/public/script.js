// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Active navigation link
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Smooth scroll to optimizer
function scrollToOptimizer() {
    document.getElementById('optimizer').scrollIntoView({ behavior: 'smooth' });
}

// Fragility slider
const fragilitySlider = document.getElementById('fragility');
const fragilityValue = document.getElementById('fragilityValue');

const fragilityLevels = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];

fragilitySlider.addEventListener('input', (e) => {
    const value = parseInt(e.target.value);
    fragilityValue.textContent = fragilityLevels[value - 1];
});

// Form submission and optimization
document.getElementById('optimizerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form values
    const productName = document.getElementById('productName').value;
    const length = parseFloat(document.getElementById('length').value);
    const width = parseFloat(document.getElementById('width').value);
    const height = parseFloat(document.getElementById('height').value);
    const weight = parseFloat(document.getElementById('weight').value);
    const category = document.getElementById('category').value;
    const fragility = parseInt(document.getElementById('fragility').value);
    const stackable = document.getElementById('stackable').checked;
    const recyclable = document.getElementById('recyclable').checked;
    
    // Show loading state
    const outputDiv = document.getElementById('optimizerOutput');
    outputDiv.innerHTML = `
        <div class="output-loading">
            <div class="loading-spinner"></div>
            <p>AI is optimizing your packaging...</p>
        </div>
    `;
    
    // Add loading spinner styles
    const style = document.createElement('style');
    style.textContent = `
        .output-loading {
            text-align: center;
        }
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(45, 80, 22, 0.2);
            border-top-color: #2D5016;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1.5rem;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    // Simulate AI processing (in real implementation, this would call your Flask API)
    setTimeout(() => {
        // Calculate optimized dimensions (simplified algorithm)
        const padding = fragility * 2; // More fragile = more padding
        const optLength = Math.ceil(length + padding);
        const optWidth = Math.ceil(width + padding);
        const optHeight = Math.ceil(height + padding);
        
        // Calculate volume reduction
        const originalVolume = (length + 10) * (width + 10) * (height + 10);
        const optimizedVolume = optLength * optWidth * optHeight;
        const volumeReduction = ((originalVolume - optimizedVolume) / originalVolume * 100).toFixed(1);
        
        // Material recommendation based on category and weight
        let material = 'Recycled Cardboard';
        let thickness = '3mm';
        
        if (weight > 5) {
            material = 'Double-Wall Corrugated Cardboard';
            thickness = '5mm';
        } else if (category === 'electronics' && fragility >= 4) {
            material = 'Recycled Cardboard with Biodegradable Foam';
            thickness = '4mm';
        } else if (recyclable) {
            material = '100% Recycled Kraft Paper';
            thickness = '3mm';
        }
        
        // Calculate cost savings
        const costSaving = (volumeReduction * 0.8).toFixed(1);
        const co2Reduction = (volumeReduction * 1.2).toFixed(1);
        
        // Display results
        outputDiv.innerHTML = `
            <div class="optimization-results">
                <div class="result-header">
                    <div class="result-badge">✓ Optimized</div>
                    <h3>${productName}</h3>
                </div>
                
                <div class="result-section">
                    <h4>📦 Optimal Dimensions</h4>
                    <div class="dimension-grid">
                        <div class="dimension-item">
                            <span class="dim-label">Length</span>
                            <span class="dim-value">${optLength} cm</span>
                            <span class="dim-change">-${(length + 10 - optLength).toFixed(1)} cm</span>
                        </div>
                        <div class="dimension-item">
                            <span class="dim-label">Width</span>
                            <span class="dim-value">${optWidth} cm</span>
                            <span class="dim-change">-${(width + 10 - optWidth).toFixed(1)} cm</span>
                        </div>
                        <div class="dimension-item">
                            <span class="dim-label">Height</span>
                            <span class="dim-value">${optHeight} cm</span>
                            <span class="dim-change">-${(height + 10 - optHeight).toFixed(1)} cm</span>
                        </div>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>🌱 Recommended Material</h4>
                    <div class="material-card">
                        <div class="material-name">${material}</div>
                        <div class="material-details">
                            <span>Thickness: ${thickness}</span>
                            <span>100% Recyclable</span>
                            <span>Bio-degradable</span>
                        </div>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>💰 Savings & Impact</h4>
                    <div class="savings-grid">
                        <div class="saving-item">
                            <div class="saving-icon">📉</div>
                            <div class="saving-value">${volumeReduction}%</div>
                            <div class="saving-label">Volume Reduction</div>
                        </div>
                        <div class="saving-item">
                            <div class="saving-icon">💵</div>
                            <div class="saving-value">${costSaving}%</div>
                            <div class="saving-label">Cost Savings</div>
                        </div>
                        <div class="saving-item">
                            <div class="saving-icon">🌍</div>
                            <div class="saving-value">${co2Reduction}%</div>
                            <div class="saving-label">CO₂ Reduction</div>
                        </div>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>🔍 Structural Analysis</h4>
                    <div class="analysis-bars">
                        <div class="analysis-item">
                            <span class="analysis-label">Strength</span>
                            <div class="analysis-bar">
                                <div class="analysis-fill" style="width: ${fragility >= 4 ? '95' : '85'}%"></div>
                            </div>
                            <span class="analysis-value">${fragility >= 4 ? '95' : '85'}%</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">Durability</span>
                            <div class="analysis-bar">
                                <div class="analysis-fill" style="width: 92%"></div>
                            </div>
                            <span class="analysis-value">92%</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">Sustainability</span>
                            <div class="analysis-bar">
                                <div class="analysis-fill" style="width: ${recyclable ? '98' : '85'}%"></div>
                            </div>
                            <span class="analysis-value">${recyclable ? '98' : '85'}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="result-actions">
                    <button class="btn-download">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 12L6 8M10 12L14 8M10 12V2M2 16H18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        Download 2D Dieline
                    </button>
                    <button class="btn-view-3d">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 2L18 7V13L10 18L2 13V7L10 2Z" stroke="currentColor" stroke-width="2"/>
                        </svg>
                        View 3D Model
                    </button>
                    <button class="btn-report">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <rect x="4" y="2" width="12" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                            <path d="M7 7H13M7 11H13M7 15H10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        Full Report
                    </button>
                </div>
            </div>
        `;
        
        // Add result styles
        const resultStyle = document.createElement('style');
        resultStyle.textContent = `
            .optimization-results {
                width: 100%;
                animation: fadeInUp 0.5s ease;
            }
            
            .result-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .result-badge {
                display: inline-block;
                background: #10B981;
                color: white;
                padding: 0.5rem 1.5rem;
                border-radius: 50px;
                font-size: 0.875rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            
            .result-header h3 {
                font-size: 1.75rem;
                color: #1A1A1A;
            }
            
            .result-section {
                background: #F5F5F4;
                padding: 1.5rem;
                border-radius: 16px;
                margin-bottom: 1.5rem;
            }
            
            .result-section h4 {
                margin-bottom: 1rem;
                font-size: 1.125rem;
                color: #1A1A1A;
            }
            
            .dimension-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
            }
            
            .dimension-item {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                background: white;
                padding: 1rem;
                border-radius: 12px;
                text-align: center;
            }
            
            .dim-label {
                font-size: 0.75rem;
                color: #666;
                text-transform: uppercase;
                font-weight: 600;
            }
            
            .dim-value {
                font-size: 1.5rem;
                font-weight: 800;
                color: #2D5016;
            }
            
            .dim-change {
                font-size: 0.875rem;
                color: #10B981;
                font-weight: 600;
            }
            
            .material-card {
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
            }
            
            .material-name {
                font-size: 1.25rem;
                font-weight: 700;
                color: #2D5016;
                margin-bottom: 1rem;
            }
            
            .material-details {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
            }
            
            .material-details span {
                background: #2D5016;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 50px;
                font-size: 0.75rem;
                font-weight: 600;
            }
            
            .savings-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
            }
            
            .saving-item {
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
            }
            
            .saving-icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            
            .saving-value {
                display: block;
                font-size: 2rem;
                font-weight: 800;
                color: #2D5016;
                margin-bottom: 0.5rem;
            }
            
            .saving-label {
                font-size: 0.875rem;
                color: #666;
            }
            
            .analysis-bars {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .analysis-item {
                display: grid;
                grid-template-columns: 100px 1fr 60px;
                align-items: center;
                gap: 1rem;
            }
            
            .analysis-label {
                font-size: 0.875rem;
                font-weight: 600;
                color: #666;
            }
            
            .analysis-bar {
                height: 24px;
                background: white;
                border-radius: 12px;
                overflow: hidden;
            }
            
            .analysis-fill {
                height: 100%;
                background: linear-gradient(90deg, #2D5016, #4A7C2C);
                transition: width 1s ease;
            }
            
            .analysis-value {
                font-weight: 700;
                color: #2D5016;
            }
            
            .result-actions {
                display: flex;
                gap: 1rem;
                margin-top: 2rem;
            }
            
            .result-actions button {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 1rem;
                border: 2px solid #2D5016;
                background: white;
                color: #2D5016;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.25s ease;
                font-family: 'Outfit', sans-serif;
            }
            
            .result-actions button:hover {
                background: #2D5016;
                color: white;
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(45, 80, 22, 0.2);
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(resultStyle);
        
    }, 2000); // Simulate 2 second processing time
});

// Counter animation for impact metrics
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.3,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Animate counters
            const counters = entry.target.querySelectorAll('.metric-number[data-target]');
            counters.forEach(counter => {
                if (!counter.classList.contains('animated')) {
                    counter.classList.add('animated');
                    animateCounter(counter);
                }
            });
            
            // Add fade-in animation to feature cards
            if (entry.target.classList.contains('feature-card')) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        }
    });
}, observerOptions);

// Observe elements
document.addEventListener('DOMContentLoaded', () => {
    const impactSection = document.querySelector('.impact');
    const featureCards = document.querySelectorAll('.feature-card');
    
    if (impactSection) {
        observer.observe(impactSection);
    }
    
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
});

// Add parallax effect to hero visual
window.addEventListener('scroll', () => {
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.3;
        heroVisual.style.transform = `translateY(${rate}px)`;
    }
});

// Button click handlers (placeholders for actual functionality)
document.addEventListener('click', (e) => {
    if (e.target.closest('.btn-download')) {
        alert('2D Dieline download feature - Connect to your Flask backend API endpoint');
    }
    if (e.target.closest('.btn-view-3d')) {
        alert('3D Model viewer feature - Integrate Three.js 3D visualization');
    }
    if (e.target.closest('.btn-report')) {
        alert('Full sustainability report - Generate PDF with detailed analysis');
    }
});

console.log('🌱 EcoPackAI - Sustainable Packaging Optimization System');
console.log('Ready to optimize your packaging!');