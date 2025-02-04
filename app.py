from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv  # For local development

load_dotenv()

app = Flask(__name__)

# Spoonacular API config
API_KEY = os.getenv("SPOONACULAR_API_KEY")  # Fetch API key from environment
SPOONACULAR_API_URL = "https://api.spoonacular.com/recipes/visualizePriceEstimator"

@app.route('/price-estimator', methods=['POST'])
def price_estimator():
    """
    Endpoint to estimate ingredient prices using Spoonacular's Price Estimator API
    """
    try:
        # Validate API Key
        if not API_KEY:
            return jsonify({"error": "API key is missing. Set SPOONACULAR_API_KEY in the environment."}), 500
        ingredient_list = request.form.get("ingredientList")
        servings = request.form.get("servings", 1)

        # Validate
        if not ingredient_list:
            return jsonify({"error": "ingredientList is required."}), 400

        payload = {
            "ingredientList": ingredient_list,
            "servings": servings,
            "mode": 1,  
            "defaultCss": True, 
            "showBacklink": True,  
            "language": "en",
        }
        api_url_with_key = f"{SPOONACULAR_API_URL}?apiKey={API_KEY}"

        # POST Spoonacular
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/html"}
        response = requests.post(api_url_with_key, headers=headers, data=payload)
        response.raise_for_status()

        # jQuery, CanvasJS, and Spoonacular in HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Price Estimator</title>
            <!-- Load jQuery -->
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <!-- Load CanvasJS -->
            <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
            <!-- Spoonacular script -->
            <script src="https://spoonacular.com/application/frontend/js/priceBreakdownWidget.js"></script>
        </head>
        <body>
            {response.text}
        </body>
        </html>
        """

        return html_content, 200, {"Content-Type": "text/html"}

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from Spoonacular.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        directory='static',
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/', methods=['GET'])
def health_check():
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 
