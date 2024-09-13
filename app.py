import os
import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

# Configure the Google Gemini API
genai.configure(api_key="AIzaSyAR6m0iQlsxyNGbiUHTGeEzuohbZ1XC6Yk")

# Define the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Predefined prompts
valid_prompts = [
    'Write an article about the impact of artificial intelligence on modern education.',
    'Generate an article discussing the benefits of remote work for technology professionals.',
    'Create an article on the latest trends in renewable energy technology.',
    'Write an article about the future of space exploration and its potential impacts on society.'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form['user_input']
        hidden_prompt = request.form['hidden_prompt']
        keywords = request.form['keywords']
        
        # Use hidden_prompt if it is set
        if hidden_prompt:
            user_input = hidden_prompt

        # Check if user_input matches any valid prompts or is a custom prompt
        if hidden_prompt == '' and not any(prompt in valid_prompts for prompt in [user_input]):
            result = "Invalid prompt. Please select a valid predefined prompt or enter a custom prompt."
        else:
            # Prepare prompt with keywords for SEO optimization
            if keywords:
                user_input += f"\nKeywords for SEO: {keywords}"
            
            # Process the prompt
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            result = response.text if response else "No response from Gemini."

        return render_template('index.html', user_input=user_input, result=result)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', user_input=user_input, result="An unexpected error occurred.")

# Run the app on the specified port, or default to port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))