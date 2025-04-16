from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'diabetes_hub_secret_key'  # For session management

# Mock database for development purposes
USERS_DB = {
    'admin@example.com': {
        'username': 'Admin',
        'password_hash': generate_password_hash('admin123'),
        'role': 'admin',
    }
}

# Mock data for diabetes resources
with open('data/resources.json', 'w') as f:
    if not os.path.exists('data'):
        os.makedirs('data')
    resources = [
        {
            "id": 1,
            "title": "Understanding Type 1 Diabetes",
            "description": "A comprehensive guide to Type 1 diabetes, causes, symptoms, and management strategies.",
            "category": "Type 1",
            "resource_type": "Article",
            "provider": "American Diabetes Association",
            "rating": 4.8,
            "price": "Free",
            "difficulty": "Beginner",
            "image_url": "/static/images/placeholder.jpg"
        },
        {
            "id": 2,
            "title": "Managing Type 2 Diabetes Through Diet",
            "description": "Learn how dietary choices impact blood sugar levels and how to create a diabetes-friendly meal plan.",
            "category": "Type 2",
            "resource_type": "Video",
            "provider": "Mayo Clinic",
            "rating": 4.6,
            "price": "Free",
            "difficulty": "Beginner",
            "image_url": "/static/images/placeholder.jpg"
        },
        {
            "id": 3,
            "title": "Gestational Diabetes: What to Expect",
            "description": "Important information for pregnant women about gestational diabetes, risks, and management.",
            "category": "Gestational",
            "resource_type": "Article",
            "provider": "CDC",
            "rating": 4.7,
            "price": "Free",
            "difficulty": "Beginner",
            "image_url": "/static/images/placeholder.jpg"
        },
        {
            "id": 4,
            "title": "Advanced Insulin Therapy Techniques",
            "description": "In-depth look at modern insulin therapy approaches for better diabetes management.",
            "category": "Treatment",
            "resource_type": "Tutorial",
            "provider": "Endocrine Society",
            "rating": 4.9,
            "price": "Premium",
            "difficulty": "Advanced",
            "image_url": "/static/images/placeholder.jpg"
        },
        {
            "id": 5,
            "title": "Exercise Plans for Diabetics",
            "description": "Safe and effective exercise routines specially designed for people with diabetes.",
            "category": "Exercise",
            "resource_type": "Interactive Tool",
            "provider": "Diabetes UK",
            "rating": 4.5,
            "price": "Free",
            "difficulty": "Intermediate",
            "image_url": "/static/images/placeholder.jpg"
        },
        {
            "id": 6,
            "title": "Understanding Diabetes Complications",
            "description": "Learn about potential complications from diabetes and how to prevent them.",
            "category": "Complications",
            "resource_type": "Article",
            "provider": "National Institute of Diabetes",
            "rating": 4.7,
            "price": "Free",
            "difficulty": "Intermediate",
            "image_url": "/static/images/placeholder.jpg"
        }
    ]
    json.dump(resources, f)

# Mock news data
NEWS_DATA = [
    {
        "id": 1,
        "title": "New Study Reveals Link Between Gut Bacteria and Type 2 Diabetes",
        "date": "April 10, 2025",
        "summary": "Researchers have found a significant correlation between gut microbiome composition and Type 2 diabetes development.",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 2,
        "title": "FDA Approves New Fast-Acting Insulin for Type 1 Diabetes",
        "date": "April 5, 2025",
        "summary": "A revolutionary new insulin formula promises better blood sugar control with fewer side effects.",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 3,
        "title": "Mediterranean Diet Shows Promise in Preventing Prediabetes Progression",
        "date": "March 28, 2025",
        "summary": "A long-term study shows that adherence to a Mediterranean diet can significantly reduce the risk of prediabetes developing into Type 2 diabetes.",
        "image_url": "/static/images/placeholder.jpg"
    }
]

# Mock chatbot responses
CHATBOT_RESPONSES = {
    "food": "Foods to avoid with diabetes include sugary beverages, refined carbs, processed foods, and foods high in saturated fats. Focus instead on non-starchy vegetables, whole grains, lean proteins, and healthy fats.",
    "symptoms": "Common diabetes symptoms include frequent urination, increased thirst and hunger, fatigue, blurred vision, slow-healing sores, and unexplained weight loss. If you experience these symptoms, please consult a healthcare provider.",
    "exercise": "Regular physical activity is crucial for diabetes management. Aim for 150 minutes of moderate aerobic activity weekly, plus 2-3 sessions of strength training. Always consult your doctor before starting a new exercise program.",
    "medication": "Common diabetes medications include metformin, sulfonylureas, meglitinides, thiazolidinediones, DPP-4 inhibitors, GLP-1 receptor agonists, SGLT2 inhibitors, and various forms of insulin. Your doctor will determine the best option for you.",
    "default": "I'm your Diabetes Assistant. Please ask a specific question about diabetes management, treatment options, diet recommendations, or lifestyle adjustments."
}

@app.route('/')
def index():
    # For a real application, you would render the template with dynamic data
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in USERS_DB and check_password_hash(USERS_DB[email]['password_hash'], password):
            session['user'] = {
                'email': email,
                'username': USERS_DB[email]['username'],
                'role': USERS_DB[email]['role']
            }
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/resources')
def get_resources():
    category = request.args.get('category', 'All')
    resource_type = request.args.get('type', 'All')
    rating = request.args.get('rating', 'All')
    difficulty = request.args.get('difficulty', 'All')
    
    # In a real app, you'd query a database here
    with open('data/resources.json', 'r') as f:
        resources = json.load(f)
        
    # Apply filters
    if category != 'All':
        resources = [r for r in resources if r['category'] == category]
    if resource_type != 'All':
        resources = [r for r in resources if r['resource_type'] == resource_type]
    if rating != 'All':
        min_rating = float(rating.replace('+ Stars', ''))
        resources = [r for r in resources if r['rating'] >= min_rating]
    if difficulty != 'All':
        resources = [r for r in resources if r['difficulty'] == difficulty]
    
    return jsonify(resources)

@app.route('/api/news')
def get_news():
    return jsonify(NEWS_DATA)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    query = request.json.get('query', '').lower()
    
    # Simple keyword matching for demo purposes
    response = CHATBOT_RESPONSES['default']
    for keyword, resp in CHATBOT_RESPONSES.items():
        if keyword in query:
            response = resp
            break
    
    return jsonify({'response': response})

@app.route('/api/stats')
def get_stats():
    # In a real app, these would come from a database
    stats = {
        'diabetics_count': '537M',
        'annual_deaths': '6.7M',
        'undiagnosed': '240M',
        'global_cost': '$966B'
    }
    return jsonify(stats)

@app.route('/tools/carb-calculator')
def carb_calculator():
    return render_template('tools/carb-calculator.html')

@app.route('/tools/a1c-converter')
def a1c_converter():
    return render_template('tools/a1c-converter.html')

@app.route('/tools/blood-sugar-log')
def blood_sugar_log():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('tools/blood-sugar-log.html')

@app.route('/api/calculate-carbs', methods=['POST'])
def calculate_carbs():
    food_item = request.json.get('food')
    quantity = request.json.get('quantity')
    
    # This would connect to a food database in a real app
    # Simple mock response for demo
    carbs = random.randint(5, 50)
    return jsonify({'carbs': carbs})

@app.route('/api/convert-a1c', methods=['POST'])
def convert_a1c():
    a1c = float(request.json.get('a1c'))
    # A1C to eAG (estimated average glucose) formula
    eag = (28.7 * a1c) - 46.7
    return jsonify({'eag': round(eag, 1)})

@app.route('/api/log-blood-sugar', methods=['POST'])
def log_blood_sugar():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    reading = {
        'level': request.json.get('level'),
        'time': request.json.get('time'),
        'notes': request.json.get('notes'),
        'timestamp': datetime.now().isoformat()
    }
    
    # In a real app, save to database
    # For demo, we'll pretend it was saved
    return jsonify({'success': True, 'reading': reading})

@app.route('/diabetes/<diabetes_type>')
def diabetes_info(diabetes_type):
    # This would pull content from a CMS or database in a real app
    return render_template(f'diabetes/{diabetes_type}.html')

@app.route('/diet-nutrition')
def diet_nutrition():
    return render_template('diet-nutrition.html')

@app.route('/medications')
def medications():
    return render_template('medications.html')

@app.route('/treatment-options')
def treatment_options():
    return render_template('treatment-options.html')

@app.route('/management')
def management():
    return render_template('management.html')

@app.route('/insulin-therapy')
def insulin_therapy():
    return render_template('insulin-therapy.html')

@app.route('/exercise-lifestyle')
def exercise_lifestyle():
    return render_template('exercise-lifestyle.html')

@app.route('/complications')
def complications():
    return render_template('complications.html')

@app.route('/research-news')
def research_news():
    return render_template('research-news.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/glossary')
def glossary():
    return render_template('glossary.html')

@app.route('/api/symptom-checker', methods=['POST'])
def symptom_checker():
    symptoms = request.json.get('symptoms', [])
    
    # In a real app, this would use a medical algorithm
    # Simple mock response for demo
    if 'frequent urination' in symptoms and 'increased thirst' in symptoms:
        result = "These symptoms could indicate diabetes. Please consult a healthcare professional for proper diagnosis."
    else:
        result = "Based on the symptoms provided, we cannot determine a specific condition. Please consult a healthcare professional for proper diagnosis."
    
    return jsonify({'result': result})

# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create static files directory if it doesn't exist
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    # Create a placeholder image if it doesn't exist
    if not os.path.exists('static/images/placeholder.jpg'):
        # In a real app, you'd create an actual image
        # For now, just create an empty file
        with open('static/images/placeholder.jpg', 'w') as f:
            f.write('')
    
    app.run(debug=True)