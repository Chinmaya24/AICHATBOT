# web_app.py - Flask Web Application
from flask import Flask, request, render_template_string, jsonify
from ai_assistant import AIAssistant

def create_web_app():
    """Create Flask web application"""
    app = Flask(__name__)
    assistant = AIAssistant()
    
    # HTML template
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
            .header p { font-size: 1.1rem; opacity: 0.9; }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .function-selector {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
                margin-bottom: 25px;
            }
            
            .function-btn {
                padding: 15px;
                border: 2px solid #667eea;
                border-radius: 10px;
                background: white;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
            }
            
            .function-btn:hover, .function-btn.active {
                background: #667eea;
                color: white;
                transform: translateY(-2px);
            }
            
            .input-section {
                display: none;
                margin-bottom: 20px;
            }
            
            .input-section.active { display: block; }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #555;
            }
            
            input[type="text"], textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            
            input[type="text"]:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            textarea { 
                height: 120px; 
                resize: vertical; 
            }
            
            .submit-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.3s ease;
            }
            
            .submit-btn:hover { transform: translateY(-2px); }
            
            .response-section {
                background: #f8f9ff;
                border-left: 4px solid #667eea;
                padding: 20px;
                border-radius: 0 10px 10px 0;
                margin: 20px 0;
                white-space: pre-wrap;
                display: none;
            }
            
            .response-section.show { display: block; }
            
            .feedback-section {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
                display: none;
            }
            
            .feedback-section.show { display: block; }
            
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
                transition: all 0.3s ease;
            }
            
            .feedback-btn:hover { background: #f0f0f0; }
            .feedback-btn.selected { background: #667eea; color: white; }
            
            .stats-card {
                background: #e8f4fd;
                border: 1px solid #bee5eb;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
            }
            
            @media (max-width: 600px) {
                .container { padding: 10px; }
                .header h1 { font-size: 2rem; }
                .function-selector { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Assistant</h1>
                <p>Your intelligent companion for questions, summaries, and creative content</p>
            </div>
            
            <div class="card">
                <div class="function-selector">
                    <div class="function-btn" onclick="selectFunction('question')">
                        🧠 Answer Questions
                    </div>
                    <div class="function-btn" onclick="selectFunction('summary')">
                        📄 Summarize Text
                    </div>
                    <div class="function-btn" onclick="selectFunction('creative')">
                        ✨ Creative Content
                    </div>
                    <div class="function-btn" onclick="selectFunction('study')">
                        📚 Study Tips
                    </div>
                </div>
                
                <form id="assistantForm">
                    <div id="question-input" class="input-section">
                        <label for="question">Ask me anything:</label>
                        <input type="text" id="question" name="question" 
                               placeholder="e.g., What is the capital of France?">
                    </div>
                    
                    <div id="summary-input" class="input-section">
                        <label for="text">Text to summarize:</label>
                        <textarea id="text" name="text" 
                                  placeholder="Paste the text you want me to summarize..."></textarea>
                    </div>
                    
                    <div id="creative-input" class="input-section">
                        <label for="prompt">Creative prompt:</label>
                        <input type="text" id="prompt" name="prompt" 
                               placeholder="e.g., Write a story about adventure">
                    </div>
                    
                    <div id="study-input" class="input-section">
                        <label>Click submit to get effective study tips!</label>
                    </div>
                    
                    <button type="submit" class="submit-btn">Submit</button>
                </form>
                
                <div id="response" class="response-section"></div>
                
                <div id="feedback" class="feedback-section">
                    <p><strong>Was this response helpful?</strong></p>
                    <div class="feedback-buttons">
                        <button type="button" class="feedback-btn" onclick="submitFeedback(true)">👍 Yes</button>
                        <button type="button" class="feedback-btn" onclick="submitFeedback(false)">👎 No</button>
                    </div>
                    <div style="margin-top: 10px;">
                        <input type="text" id="feedbackComment" placeholder="Optional comment..." style="width: 100%;">
                    </div>
                </div>
                
                <div id="stats" class="stats-card" style="display: none;">
                    <h3>📊 Feedback Statistics</h3>
                    <div id="statsContent"></div>
                </div>
                
                <button onclick="showStats()" style="margin-top: 15px; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; background: white; cursor: pointer;">
                    View Statistics
                </button>
            </div>
        </div>
        
        <script>
            let currentFunction = null;
            let currentResponse = null;
            let currentInput = null;
            
            function selectFunction(funcType) {
                // Remove active class from all buttons
                document.querySelectorAll('.function-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Hide all input sections
                document.querySelectorAll('.input-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Activate selected function
                event.target.classList.add('active');
                document.getElementById(funcType + '-input').classList.add('active');
                currentFunction = funcType;
                
                // Hide response and feedback
                document.getElementById('response').classList.remove('show');
                document.getElementById('feedback').classList.remove('show');
            }
            
            document.getElementById('assistantForm').onsubmit = async function(e) {
                e.preventDefault();
                
                if (!currentFunction) {
                    alert('Please select a function first!');
                    return;
                }
                
                const formData = new FormData();
                formData.append('function', currentFunction);
                
                let inputValue = '';
                if (currentFunction === 'question') {
                    inputValue = document.getElementById('question').value;
                } else if (currentFunction === 'summary') {
                    inputValue = document.getElementById('text').value;
                } else if (currentFunction === 'creative') {
                    inputValue = document.getElementById('prompt').value;
                } else if (currentFunction === 'study') {
                    inputValue = 'study tips request';
                }
                
                if (!inputValue.trim() && currentFunction !== 'study') {
                    alert('Please provide input for the selected function!');
                    return;
                }
                
                formData.append('input', inputValue);
                currentInput = inputValue;
                
                try {
                    const response = await fetch('/process', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    document.getElementById('response').textContent = data.response;
                    document.getElementById('response').classList.add('show');
                    document.getElementById('feedback').classList.add('show');
                    
                    currentResponse = data.response;
                    
                } catch (error) {
                    document.getElementById('response').textContent = 'Error: ' + error.message;
                    document.getElementById('response').classList.add('show');
                }
            };
            
            async function submitFeedback(helpful) {
                const comment = document.getElementById('feedbackComment').value;
                
                const formData = new FormData();
                formData.append('helpful', helpful);
                formData.append('comment', comment);
                formData.append('function', currentFunction);
                formData.append('input', currentInput);
                formData.append('response', currentResponse);
                
                try {
                    const response = await fetch('/feedback', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        document.getElementById('feedback').innerHTML = '<p style="color: green;">✅ Thank you for your feedback!</p>';
                    }
                } catch (error) {
                    console.error('Error submitting feedback:', error);
                }
            }
            
            async function showStats() {
                try {
                    const response = await fetch('/stats');
                    const data = await response.json();
                    
                    let statsHTML = '<p><strong>Total responses:</strong> ' + data.total + '</p>';
                    if (data.total > 0) {
                        statsHTML += '<p><strong>Helpful responses:</strong> ' + data.helpful + ' (' + data.helpful_rate + '%)</p>';
                        
                        if (data.by_function && Object.keys(data.by_function).length > 0) {
                            statsHTML += '<h4 style="margin-top: 15px;">By Function:</h4>';
                            for (const [func, stats] of Object.entries(data.by_function)) {
                                const rate = ((stats.helpful / stats.total) * 100).toFixed(1);
                                statsHTML += '<p>• ' + func + ': ' + stats.helpful + '/' + stats.total + ' (' + rate + '%)</p>';
                            }
                        }
                    }
                    
                    document.getElementById('statsContent').innerHTML = statsHTML;
                    document.getElementById('stats').style.display = 'block';
                    
                } catch (error) {
                    console.error('Error fetching stats:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/process', methods=['POST'])
    def process_request():
        try:
            function_type = request.form.get('function')
            user_input = request.form.get('input', '')
            
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
            
            return jsonify({'response': response})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/feedback', methods=['POST'])
    def submit_feedback():
        try:
            helpful = request.form.get('helpful') == 'true'
            comment = request.form.get('comment', '')
            function_type = request.form.get('function', '')
            user_input = request.form.get('input', '')
            response_text = request.form.get('response', '')
            
            # Map function types to display names
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
            return jsonify({'error': str(e)}), 500
    
    @app.route('/stats')
    def get_stats():
        try:
            total_feedback = len(assistant.feedback_data)
            if total_feedback == 0:
                return jsonify({
                    'total': 0,
                    'helpful': 0,
                    'helpful_rate': 0,
                    'by_function': {}
                })
            
            helpful_count = sum(1 for f in assistant.feedback_data if f['helpful'])
            helpful_rate = round((helpful_count / total_feedback) * 100, 1)
            
            # Function breakdown
            function_stats = {}
            for f in assistant.feedback_data:
                func = f['function_type']
                if func not in function_stats:
                    function_stats[func] = {'total': 0, 'helpful': 0}
                function_stats[func]['total'] += 1
                if f['helpful']:
                    function_stats[func]['helpful'] += 1
            
            return jsonify({
                'total': total_feedback,
                'helpful': helpful_count,
                'helpful_rate': helpful_rate,
                'by_function': function_stats
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

def run_web_app():
    """Run the Flask web application"""
    app = create_web_app()
    print("Starting AI Assistant Web App...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    run_web_app()