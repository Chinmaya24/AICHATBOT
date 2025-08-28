# app.py - Complete Web Application with Attractive UI
from flask import Flask, request, render_template_string, jsonify
from ai_assistant import AIAssistant

app = Flask(__name__)
assistant = AIAssistant()

# Modern, attractive HTML template with advanced styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Assistant - Smart & Beautiful</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }
        
        /* Animated background particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 10;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: slideDown 1s ease-out;
        }
        
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .main-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: slideUp 1s ease-out;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .function-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 35px;
        }
        
        .function-card {
            background: linear-gradient(145deg, #f8f9ff, #e8f0fe);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 25px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .function-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.5s;
        }
        
        .function-card:hover::before {
            left: 100%;
        }
        
        .function-card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: #667eea;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
            background: linear-gradient(145deg, #667eea, #764ba2);
            color: white;
        }
        
        .function-card.active {
            background: linear-gradient(145deg, #667eea, #764ba2);
            color: white;
            border-color: #5a67d8;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .function-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            display: block;
        }
        
        .function-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .function-desc {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .input-section {
            display: none;
            margin-bottom: 30px;
            animation: fadeIn 0.5s ease-out;
        }
        
        .input-section.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #555;
            font-size: 1.1rem;
        }
        
        input[type="text"], textarea {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #fff;
            font-family: inherit;
        }
        
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-1px);
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
            position: relative;
            overflow: hidden;
            min-width: 150px;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .submit-btn:active {
            transform: translateY(0);
        }
        
        .submit-btn.loading {
            pointer-events: none;
        }
        
        .submit-btn.loading::after {
            content: '';
            position: absolute;
            width: 16px;
            height: 16px;
            margin: auto;
            border: 2px solid transparent;
            border-top-color: #ffffff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        
        @keyframes spin {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .response-section {
            background: linear-gradient(135deg, #f8f9ff, #e8f4fd);
            border-left: 5px solid #667eea;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            display: none;
            white-space: pre-wrap;
            line-height: 1.6;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .response-section.show {
            display: block;
        }
        
        .response-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            color: #667eea;
            font-weight: 600;
        }
        
        .response-header i {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        .feedback-section {
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            border: 1px solid #ffd93d;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            display: none;
            animation: bounceIn 0.6s ease-out;
        }
        
        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .feedback-section.show {
            display: block;
        }
        
        .feedback-title {
            font-weight: 600;
            margin-bottom: 15px;
            color: #856404;
        }
        
        .feedback-buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .feedback-btn {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #ffd93d;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .feedback-btn:hover {
            background: #ffd93d;
            transform: translateY(-2px);
        }
        
        .feedback-btn.selected {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .stats-section {
            background: linear-gradient(135deg, #e8f4fd, #d1ecf1);
            border: 1px solid #bee5eb;
            border-radius: 15px;
            padding: 20px;
            margin-top: 25px;
            display: none;
        }
        
        .stats-section.show {
            display: block;
            animation: fadeIn 0.5s ease-out;
        }
        
        .stats-title {
            color: #0c5460;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .view-stats-btn {
            background: linear-gradient(135deg, #17a2b8, #138496);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
            font-weight: 600;
        }
        
        .view-stats-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(23, 162, 184, 0.3);
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .container { padding: 15px; }
            .header h1 { font-size: 2.2rem; }
            .main-card { padding: 25px; }
            .function-grid { grid-template-columns: 1fr; gap: 15px; }
            .feedback-buttons { flex-direction: column; }
        }
        
        /* Success message */
        .success-message {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.5s ease-out;
        }
    </style>
</head>
<body>
    <!-- Animated background particles -->
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> AI Assistant</h1>
            <p>Your intelligent companion for questions, summaries, and creative content</p>
        </div>
        
        <div class="main-card">
            <!-- Function Selection Grid -->
            <div class="function-grid">
                <div class="function-card" onclick="selectFunction('question')">
                    <i class="fas fa-brain function-icon"></i>
                    <div class="function-title">Answer Questions</div>
                    <div class="function-desc">Get answers to your queries</div>
                </div>
                
                <div class="function-card" onclick="selectFunction('summary')">
                    <i class="fas fa-file-alt function-icon"></i>
                    <div class="function-title">Summarize Text</div>
                    <div class="function-desc">Extract key points from text</div>
                </div>
                
                <div class="function-card" onclick="selectFunction('creative')">
                    <i class="fas fa-magic function-icon"></i>
                    <div class="function-title">Creative Content</div>
                    <div class="function-desc">Generate stories and poems</div>
                </div>
                
                <div class="function-card" onclick="selectFunction('study')">
                    <i class="fas fa-graduation-cap function-icon"></i>
                    <div class="function-title">Study Tips</div>
                    <div class="function-desc">Effective learning strategies</div>
                </div>
            </div>
            
            <!-- Input Forms -->
            <form id="assistantForm">
                <div id="question-input" class="input-section">
                    <label for="question"><i class="fas fa-question-circle"></i> Ask me anything:</label>
                    <input type="text" id="question" name="question" 
                           placeholder="e.g., Where is Taj Mahal? What is 15 + 27?">
                </div>
                
                <div id="summary-input" class="input-section">
                    <label for="text"><i class="fas fa-align-left"></i> Text to summarize:</label>
                    <textarea id="text" name="text" 
                              placeholder="Paste the text you want me to summarize..."></textarea>
                </div>
                
                <div id="creative-input" class="input-section">
                    <label for="prompt"><i class="fas fa-lightbulb"></i> Creative prompt:</label>
                    <input type="text" id="prompt" name="prompt" 
                           placeholder="e.g., Write a story about adventure, Create a poem about nature">
                </div>
                
                <div id="study-input" class="input-section">
                    <label><i class="fas fa-book"></i> Ready to get effective study tips!</label>
                    <p style="color: #666; margin-top: 10px;">Click submit below to receive comprehensive study strategies and learning techniques.</p>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    <span id="submitText">Submit</span>
                </button>
            </form>
            
            <!-- Response Display -->
            <div id="response" class="response-section">
                <div class="response-header">
                    <i class="fas fa-robot"></i>
                    AI Assistant Response:
                </div>
                <div id="responseContent"></div>
            </div>
            
            <!-- Feedback Section -->
            <div id="feedback" class="feedback-section">
                <div class="feedback-title">Was this response helpful?</div>
                <div class="feedback-buttons">
                    <button type="button" class="feedback-btn" onclick="submitFeedback(true)">
                        <i class="fas fa-thumbs-up"></i> Yes, helpful!
                    </button>
                    <button type="button" class="feedback-btn" onclick="submitFeedback(false)">
                        <i class="fas fa-thumbs-down"></i> Not helpful
                    </button>
                </div>
                <input type="text" id="feedbackComment" placeholder="Optional: Tell us how we can improve..." 
                       style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            </div>
            
            <!-- Statistics Section -->
            <div id="stats" class="stats-section">
                <div class="stats-title">
                    <i class="fas fa-chart-bar"></i>
                    Feedback Statistics
                </div>
                <div id="statsContent"></div>
            </div>
            
            <button class="view-stats-btn" onclick="showStats()">
                <i class="fas fa-chart-line"></i> View Statistics
            </button>
        </div>
    </div>
    
    <script>
        let currentFunction = null;
        let currentResponse = null;
        let currentInput = null;
        
        // Create animated particles
        function createParticles() {
            const particles = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = particle.style.height = Math.random() * 10 + 5 + 'px';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
                particles.appendChild(particle);
            }
        }
        
        // Initialize particles
        createParticles();
        
        function selectFunction(funcType) {
            // Remove active class from all cards
            document.querySelectorAll('.function-card').forEach(card => {
                card.classList.remove('active');
            });
            
            // Hide all input sections
            document.querySelectorAll('.input-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Activate selected function
            event.target.closest('.function-card').classList.add('active');
            document.getElementById(funcType + '-input').classList.add('active');
            currentFunction = funcType;
            
            // Hide response and feedback
            document.getElementById('response').classList.remove('show');
            document.getElementById('feedback').classList.remove('show');
            document.getElementById('stats').classList.remove('show');
        }
        
        document.getElementById('assistantForm').onsubmit = async function(e) {
            e.preventDefault();
            
            if (!currentFunction) {
                alert('Please select a function first!');
                return;
            }
            
            const submitBtn = document.getElementById('submitBtn');
            const submitText = document.getElementById('submitText');
            
            // Show loading state
            submitBtn.classList.add('loading');
            submitText.textContent = 'Processing...';
            
            const formData = new FormData();
            formData.append('function', currentFunction);
            
            let inputValue = '';
            try {
                if (currentFunction === 'question') {
                    const questionInput = document.getElementById('question');
                    inputValue = questionInput ? questionInput.value : '';
                } else if (currentFunction === 'summary') {
                    const textInput = document.getElementById('text');
                    inputValue = textInput ? textInput.value : '';
                } else if (currentFunction === 'creative') {
                    const promptInput = document.getElementById('prompt');
                    inputValue = promptInput ? promptInput.value : '';
                } else if (currentFunction === 'study') {
                    inputValue = 'study tips request';
                }
            } catch (error) {
                console.error('Error getting input value:', error);
                inputValue = '';
            }
            
            if (!inputValue.trim() && currentFunction !== 'study') {
                alert('Please provide input for the selected function!');
                submitBtn.classList.remove('loading');
                submitText.textContent = 'Submit';
                return;
            }
            
            formData.append('input', inputValue);
            currentInput = inputValue;
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                const responseContent = document.getElementById('responseContent');
                if (responseContent) {
                    responseContent.textContent = data.response;
                }
                
                const responseSection = document.getElementById('response');
                if (responseSection) {
                    responseSection.classList.add('show');
                }
                
                const feedbackSection = document.getElementById('feedback');
                if (feedbackSection) {
                    feedbackSection.classList.add('show');
                }
                
                currentResponse = data.response;
                
                // Reset feedback buttons
                document.querySelectorAll('.feedback-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
                
                const feedbackComment = document.getElementById('feedbackComment');
                if (feedbackComment) {
                    feedbackComment.value = '';
                }
                
            } catch (error) {
                console.error('Error processing request:', error);
                const responseContent = document.getElementById('responseContent');
                if (responseContent) {
                    responseContent.textContent = 'Error: ' + error.message;
                }
                const responseSection = document.getElementById('response');
                if (responseSection) {
                    responseSection.classList.add('show');
                }
            } finally {
                // Remove loading state
                submitBtn.classList.remove('loading');
                submitText.textContent = 'Submit';
            }
        };
        
        async function submitFeedback(helpful) {
            const comment = document.getElementById('feedbackComment').value;
            const selectedBtn = event.target.closest('.feedback-btn');
            
            // Mark button as selected
            document.querySelectorAll('.feedback-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            selectedBtn.classList.add('selected');
            
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
                    // Show success message
                    document.getElementById('feedback').innerHTML = `
                        <div class="success-message">
                            <i class="fas fa-check-circle"></i>
                            Thank you for your feedback! It helps us improve.
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error submitting feedback:', error);
            }
        }
        
        async function showStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                let statsHTML = `<p><strong>Total responses:</strong> ${data.total}</p>`;
                if (data.total > 0) {
                    statsHTML += `<p><strong>Helpful responses:</strong> ${data.helpful} (${data.helpful_rate}%)</p>`;
                    
                    if (data.by_function && Object.keys(data.by_function).length > 0) {
                        statsHTML += '<h4 style="margin: 15px 0 10px 0; color: #0c5460;">By Function:</h4>';
                        for (const [func, stats] of Object.entries(data.by_function)) {
                            const rate = ((stats.helpful / stats.total) * 100).toFixed(1);
                            statsHTML += `<p><i class="fas fa-chart-pie" style="margin-right: 8px; color: #667eea;"></i> ${func}: ${stats.helpful}/${stats.total} (${rate}%)</p>`;
                        }
                    }
                }
                
                document.getElementById('statsContent').innerHTML = statsHTML;
                document.getElementById('stats').classList.add('show');
                
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

if __name__ == "__main__":
    print("🚀 Starting AI Assistant Web App...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("✨ Enjoy the beautiful interface!")
    app.run(debug=True, port=5000, host='0.0.0.0')