!pip install flask==2.0.1 transformers==4.40.0 pytest==7.4.0

# Commented out IPython magic to ensure Python compatibility.
# # Guardar main.py
# %%writefile main.py
# from flask import Flask, request, jsonify
# from transformers import pipeline
# import logging
# import sys
# 
# # Configure logging to output to Colab console
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler(sys.stdout)]
# )
# logger = logging.getLogger(__name__)
# 
# app = Flask(__name__)
# 
# try:
#     logger.info("Loading distilgpt2 model...")
#     generator = pipeline('text-generation', model='distilgpt2')
#     logger.info("Modelo distilgpt2 cargado exitosamente")
# except Exception as e:
#     logger.error(f"Error al cargar el modelo: {str(e)}")
#     raise
# 
# @app.route('/generate', methods=['POST'])
# def generate_text():
#     try:
#         data = request.get_json()
#         if not data or 'prompt' not in data:
#             logger.warning("Solicitud inválida: falta el campo 'prompt'")
#             return jsonify({'error': 'El campo "prompt" es requerido'}), 400
# 
#         prompt = data['prompt']
#         max_length = data.get('max_length', 50)
# 
#         if not isinstance(prompt, str) or not prompt.strip():
#             logger.warning("Prompt inválido recibido")
#             return jsonify({'error': 'El prompt debe ser un texto no vacío'}), 400
#         if not isinstance(max_length, int) or max_length < 10 or max_length > 500:
#             logger.warning(f"max_length inválido: {max_length}")
#             return jsonify({'error': 'max_length debe ser un entero entre 10 y 500'}), 400
# 
#         logger.info(f"Generating text for prompt: {prompt[:50]}...")
#         result = generator(prompt, max_length=max_length, num_return_sequences=1)
#         generated_text = result[0]['generated_text']
# 
#         logger.info(f"Texto generado exitosamente")
#         return jsonify({
#             'generated_text': generated_text,
#             'prompt': prompt,
#             'max_length': max_length
#         }), 200
# 
#     except Exception as e:
#         logger.error(f"Error en /generate: {str(e)}")
#         return jsonify({'error': 'Error interno del servidor'}), 500
# 
# @app.route('/health', methods=['GET'])
# def health_check():
#     logger.info("Health check endpoint called")
#     return jsonify({'status': 'healthy'}), 200
# 
# if __name__ == '__main__':
#     logger.info("Starting Flask server on port 5000...")
#     app.run(host='0.0.0.0', port=5000, debug=False)

# Commented out IPython magic to ensure Python compatibility.
# # Guardar test_api.py
# %%writefile test_api.py
# import pytest
# import json
# from main import app
# 
# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client
# 
# def test_generate_text_success(client):
#     response = client.post('/generate',
#                          json={'prompt': 'Hola, soy una IA', 'max_length': 50})
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert 'generated_text' in data
#     assert 'prompt' in data
#     assert data['prompt'] == 'Hola, soy una IA'
#     assert isinstance(data['generated_text'], str)
#     assert len(data['generated_text']) > 0
# 
# def test_generate_text_missing_prompt(client):
#     response = client.post('/generate', json={})
#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'error' in data
#     assert data['error'] == 'El campo "prompt" es requerido'
# 
# def test_generate_text_invalid_max_length(client):
#     response = client.post('/generate',
#                          json={'prompt': 'Test', 'max_length': 600})
#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'error' in data
#     assert 'max_length debe ser un entero entre 10 y 500' in data['error']
# 
# def test_health_check(client):
#     response = client.get('/health')
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data['status'] == 'healthy'

# Commented out IPython magic to ensure Python compatibility.
# # Guardar requirements.txt
# %%writefile requirements.txt
# flask==2.0.1 transformers==4.40.0 pytest==7.4.0

# Commented out IPython magic to ensure Python compatibility.
# # Guardar colab_setup.sh
# %%writefile colab_setup.sh
# #!/bin/bash
# pip install -r requirements.txt

# Commented out IPython magic to ensure Python compatibility.
# # Guardar run_tests.sh
# %%writefile run_tests.sh
# #!/bin/bash
# pytest test_api.py -v

!pip install pyngrok flask werkzeug==2.0.3

# Start Flask server in a separate thread
import threading
import time
import requests
from pyngrok import ngrok
from flask import Flask

# Import app from main.py
from main import app

def run_flask():
    print("Starting Flask server in thread...")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Flask server failed: {e}")

# Start Flask in a background thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Wait to ensure the server starts
print("Waiting for Flask server to start...")
time.sleep(15)  # Increased to account for model loading

# Verify Flask server is running
try:
    response = requests.get("http://localhost:5000/health", timeout=5)
    if response.status_code == 200:
        print("Flask server is running:", response.json())
    else:
        print(f"Flask server returned unexpected status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Error: Flask server is not running on port 5000")
    raise Exception("Flask server failed to start. Check logs above for errors.")

# Set ngrok authtoken
ngrok.set_auth_token("2yEL9XjHPlteDUAr0h8dewXeP7M_3Yx6Woe44vKgCoXff89WL")

# Create ngrok tunnel
try:
    public_url = ngrok.connect(5000, bind_tls=True)
    print(f"API available at: {public_url}")
except Exception as e:
    print(f"Error starting ngrok: {e}")
    raise

# Test the API
try:
    url = f"{public_url}/generate"
    payload = {"prompt": "Hola, soy una IA", "max_length": 50}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    print("API Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error testing API: {e}")
    print("Response content:", response.text if 'response' in locals() else "No response")

# Run automated tests
!bash run_tests.sh

!lsof -i :5000

import requests
try:
    response = requests.get("http://localhost:5000/health", timeout=5)
    print("Health check:", response.json())
except requests.exceptions.ConnectionError:
    print("Flask server is not running on port 5000")

!ngrok diagnose

!bash run_tests.sh

!curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt":"Hola, soy una IA","max_length":50}'
