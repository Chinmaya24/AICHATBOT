# simple_app.py - Simplified Web App for Testing
from flask import Flask, request, render_template_string, jsonify
from ai_assistant import AIAssistant

app = Flask(__name__)
assistant = AIAssistant()

# Simplified HTML template for testing
SIMPLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Assistant - Simple Version</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        
        .function-buttons {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .function-btn {
            padding: 15px 20px;
            border: 2px solid #667eea;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .function-btn:hover, .function-btn.active {
            background: #667eea;
            color: white;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .input-group textarea {
            height: 100px;
            resize: vertical;
        }
        
        .submit-btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            display: block;
            margin: 20px auto;
        }
        
        .submit-btn:hover {
            background: #5a67d8;
        }
        
        .response-box {
            background: #f8f9ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            white-space: pre-wrap;
            display: none;
        }
        
        .response-box.show {
            display: block;
        }
        
        .feedback-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            display: none;
        }
        
        .feedback-box.show {
            display: block;
        }
        
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }
        
        .feedback-btn {
            padding: 8px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
            cursor: pointer;
        }
        
        .feedback-btn:hover {
            background: #f0f0f0;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Assistant</h1>
            <p>Choose a function and interact with the AI</p>
        </div>
        
        <div class="function-buttons">
            <button class="function-btn" onclick="selectFunction('question')">
                🧠 Answer Questions
            </button>
            <button class="function-btn" onclick="selectFunction('summary')">
                📄 Summarize Text
            </button>
            <button class="function-btn" onclick="selectFunction('creative')">
                ✨ Creative Content
            </button>
            <button class="function-btn" onclick="selectFunction('study')">
                📚 Study Tips
            </button>
        </div>
        
        <form id="mainForm">
            <div id="question-section" class="input-group hidden">
                <label for="questionInput">Ask your question:</label>
                <input type="text" id="questionInput" placeholder="e.g., Where is Taj Mahal?">
            </div>
            
            <div id="summary-section" class="input-group hidden">
                <label for="textInput">Text to summarize:</label>
                <textarea id="textInput" placeholder="Paste text here..."></textarea>
            </div>
            
            <div id="creative-section" class="input-group hidden">
                <label for="promptInput">Creative prompt:</label>
                <input type="text" id="promptInput" placeholder="e.g., Write a poem about nature">
            </div>
            
            <div id="study-section" class="input-group hidden">
                <label>Click submit to get study tips!</label>
            </div>
            
            <button type="submit" class="submit-btn" id="submitButton">Submit</button>
        </form>
        
        <div id="responseBox" class="response-box">
            <h3>AI Response:</h3>
            <div id="responseText"></div>
        </div>
        
        <div id="feedbackBox" class="feedback-box">
            <p><strong>Was this helpful?</strong></p>
            <div class="feedback-buttons">
                <button class="feedback-btn" onclick="submitFeedback(true)">👍 Yes</button>
                <button class="feedback-btn" onclick="submitFeedback(false)">👎 No</button>
            </div>
            <input type="text" id="commentInput" placeholder="Optional comment..." style="width: 100%; margin-top: 10px; padding: 8px;">
        </div>
    </div>
    
    <script>
        let selectedFunction = null;
        let lastResponse = null;
        let lastInput = null;
        
        function selectFunction(funcType) {
            selectedFunction = funcType;
            
            // Remove active class from all buttons
            document.querySelectorAll('.function-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Hide all sections
            document.querySelectorAll('.input-group').forEach(section => {
                section.classList.add('hidden');
            });
            
            // Show selected section
            const targetSection = document.getElementById(funcType + '-section');
            if (targetSection) {
                targetSection.classList.remove('hidden');
            }
            
            // Mark button as active
            event.target.classList.add('active');
            
            // Hide response and feedback
            document.getElementById('responseBox').classList.remove('show');
            document.getElementById('feedbackBox').classList.remove('show');
        }
        
        document.getElementById('mainForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!selectedFunction) {
                alert('Please select a function first!');
                return;
            }
            
            const submitBtn = document.getElementById('submitButton');
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;
            
            let userInput = '';
            
            if (selectedFunction === 'question') {
                userInput = document.getElementById('questionInput').value;
            } else if (selectedFunction === 'summary') {
                userInput = document.getElementById('textInput').value;
            } else if (selectedFunction === 'creative') {
                userInput = document.getElementById('promptInput').value;
            } else if (selectedFunction === 'study') {
                userInput = 'study tips request';
            }
            
            if (!userInput.trim() && selectedFunction !== 'study') {
                alert('Please provide input!');
                submitBtn.textContent = 'Submit';
                submitBtn.disabled = false;
                return;
            }
            
            lastInput = userInput;
            
            try {
                const formData = new FormData();
                formData.append('function', selectedFunction);
                formData.append('input', userInput);
                
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                document.getElementById('responseText').textContent = data.response;
                document.getElementById('responseBox').classList.add('show');
                document.getElementById('feedbackBox').classList.add('show');
                
                lastResponse = data.response;
                
            } catch (error) {
                document.getElementById('responseText').textContent = 'Error: ' + error.message;
                document.getElementById('responseBox').classList.add('show');
                console.error('Error:', error);
            } finally {
                submitBtn.textContent = 'Submit';
                submitBtn.disabled = false;
            }
        });
        
        async function submitFeedback(helpful) {
            try {
                const formData = new FormData();
                formData.append('helpful', helpful);
                formData.append('comment', document.getElementById('commentInput').value);
                formData.append('function', selectedFunction);
                formData.append('input', lastInput);
                formData.append('response', lastResponse);
                
                const response = await fetch('/feedback', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    document.getElementById('feedbackBox').innerHTML = '<p style="color: green;">✅ Thank you for your feedback!</p>';
                }
                
            } catch (error) {
                console.error('Feedback error:', error);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(SIMPLE_TEMPLATE)

@app.route('/process', methods=['POST'])
def process_request():
    try:
        function_type = request.form.get('function')
        user_input = request.form.get('input', '')
        
        print(f"Processing: {function_type} with input: {user_input}")  # Debug print
        
        if function_type == 'question':
            response = assistant.answer_question(user_input)
        elif function_type == 'summary':
            response = assistant.summarize_text(user_input)
        elif function_type == 'creative':
            response = assistant.generate_creative_content(user_input)
        elif function_type == 'study':
            response = assistant.get_study_advice()
        else:
            response = "Invalid function type."
        
        print(f"Response: {response[:100]}...")  # Debug print
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error in process_request: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        helpful = request.form.get('helpful') == 'true'
        comment = request.form.get('comment', '')
        function_type = request.form.get('function', '')
        user_input = request.form.get('input', '')
        response_text = request.form.get('response', '')
        
        function_names = {
            'question': 'Answer Question',
            'summary': 'Summarize Text',
            'creative': 'Generate Creative Content',
            'study': 'Study Tips'
        }
        
        display_name = function_names.get(function_type, function_type)
        assistant.save_feedback(display_name, user_input, response_text, helpful, comment)
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        print(f"Error in submit_feedback: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Simple AI Assistant Web App...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🔧 This version includes debug information in console")
    app.run(debug=True, port=5000, host='0.0.0.0')