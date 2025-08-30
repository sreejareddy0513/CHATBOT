from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

GOOGLE_API_KEY = 'AIzaSyDoi7HuuE3NDlrBSXErzAO3f35KfU4HJlo'   # or load from .env
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])   # <-- fix here

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json(silent=True) or {}
    user_input = (data.get('message') or '').strip()
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = chat.send_message(user_input).text
        return jsonify({'response': response})
    except Exception as e:
        print('Error:', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
