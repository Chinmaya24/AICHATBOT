# ai_assistant.py - Core AI Assistant class
import json
import datetime
import os
from typing import Dict, List, Any
import re

class AIAssistant:
    """Core AI Assistant class with multiple functionalities"""
    
    def __init__(self):
        self.feedback_file = "assistant_feedback.json"
        self.load_feedback_data()
    
    def load_feedback_data(self):
        """Load existing feedback data"""
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r') as f:
                    self.feedback_data = json.load(f)
            else:
                self.feedback_data = []
        except:
            self.feedback_data = []
    
    def save_feedback(self, function_type: str, user_input: str, response: str, helpful: bool, comment: str = ""):
        """Save user feedback"""
        feedback_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "function_type": function_type,
            "user_input": user_input[:100] + "..." if len(user_input) > 100 else user_input,
            "response_preview": response[:100] + "..." if len(response) > 100 else response,
            "helpful": helpful,
            "comment": comment
        }
        
        self.feedback_data.append(feedback_entry)
        
        try:
            with open(self.feedback_file, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save feedback - {e}")
    
    def answer_question(self, question: str) -> str:
        """Function 1: Answer factual questions"""
        question = question.lower().strip()
        
        # Knowledge base for common questions
        knowledge_base = {
            # World Capitals
            "capital of france": "The capital of France is Paris.",
            "capital of japan": "The capital of Japan is Tokyo.",
            "capital of uk": "The capital of the United Kingdom is London.",
            "capital of usa": "The capital of the United States is Washington, D.C.",
            "capital of america": "The capital of the United States is Washington, D.C.",
            "capital of germany": "The capital of Germany is Berlin.",
            "capital of india": "The capital of India is New Delhi.",
            "capital of china": "The capital of China is Beijing.",
            "capital of russia": "The capital of Russia is Moscow.",
            "capital of australia": "The capital of Australia is Canberra.",
            "capital of canada": "The capital of Canada is Ottawa.",
            "capital of brazil": "The capital of Brazil is Brasília.",
            "capital of italy": "The capital of Italy is Rome.",
            "capital of spain": "The capital of Spain is Madrid.",
            
            # Taj Mahal variations
            "taj mahal": "The Taj Mahal is located in Agra, Uttar Pradesh, India. It is a UNESCO World Heritage Site and one of the Seven Wonders of the World, built by Mughal Emperor Shah Jahan for his wife Mumtaz Mahal.",
            "tajmahal": "The Taj Mahal is located in Agra, Uttar Pradesh, India. It is a UNESCO World Heritage Site and one of the Seven Wonders of the World, built by Mughal Emperor Shah Jahan for his wife Mumtaz Mahal.",
            
            # Famous Landmarks
            "eiffel tower": "The Eiffel Tower is located in Paris, France. It stands on the Champ de Mars near the Seine River.",
            "statue of liberty": "The Statue of Liberty is located on Liberty Island in New York Harbor, New York, USA.",
            "great wall": "The Great Wall of China stretches across northern China, running from east to west for thousands of miles.",
            "pyramids": "The famous pyramids are located in Giza, Egypt, near Cairo.",
            "machu picchu": "Machu Picchu is located in the Andes Mountains of Peru, South America.",
            
            # Science and Nature
            "largest planet": "Jupiter is the largest planet in our solar system.",
            "smallest planet": "Mercury is the smallest planet in our solar system.",
            "speed of light": "The speed of light in a vacuum is approximately 299,792,458 meters per second (about 300,000 km/s).",
            "continents": "There are 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia/Oceania.",
            "largest ocean": "The Pacific Ocean is the largest ocean in the world.",
            "photosynthesis": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
            "dna": "DNA (Deoxyribonucleic acid) is the molecule that carries genetic information in living organisms.",
            "gravity": "Gravity is a fundamental force that attracts objects with mass toward each other. On Earth, it gives weight to physical objects.",
            
            # Technology
            "artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn.",
            "machine learning": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
            "python": "Python is a high-level, interpreted programming language known for its simplicity and versatility.",
            "internet": "The Internet is a global network of interconnected computers that communicate using standardized protocols.",
            "computer": "The modern computer was developed by many people, but Charles Babbage is often called the 'father of the computer' for his Analytical Engine design.",
            "telephone": "Alexander Graham Bell is credited with inventing the telephone in 1876.",
            "light bulb": "Thomas Edison is commonly credited with inventing the practical incandescent light bulb in 1879.",
            
            # History and People
            "albert einstein": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity and won the Nobel Prize in Physics in 1921.",
            "einstein": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity and won the Nobel Prize in Physics in 1921.",
            "mahatma gandhi": "Mahatma Gandhi was an Indian independence activist who led India's non-violent independence movement against British rule.",
            "gandhi": "Mahatma Gandhi was an Indian independence activist who led India's non-violent independence movement against British rule.",
            "william shakespeare": "William Shakespeare was an English playwright and poet, widely regarded as the greatest writer in the English language.",
            "shakespeare": "William Shakespeare was an English playwright and poet, widely regarded as the greatest writer in the English language.",
            "world war 2": "World War II ended in 1945, with Germany surrendering in May and Japan surrendering in September.",
            "india independence": "India gained independence from British rule on August 15, 1947.",
            
            # Basic Facts
            "days in year": "There are 365 days in a regular year and 366 days in a leap year.",
            "hours in day": "There are 24 hours in a day.",
            "minutes in hour": "There are 60 minutes in an hour.",
            "boiling point": "Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at standard atmospheric pressure.",
            "freezing point": "Water freezes at 0 degrees Celsius (32 degrees Fahrenheit) at standard atmospheric pressure.",
            
            # Geography
            "highest mountain": "Mount Everest is the highest mountain in the world, standing at 8,848.86 meters (29,031.7 feet) tall.",
            "mount everest": "Mount Everest is the highest mountain in the world, standing at 8,848.86 meters (29,031.7 feet) tall.",
            "longest river": "The Nile River in Africa is generally considered the longest river in the world at about 6,650 km (4,130 miles).",
            "largest country": "Russia is the largest country in the world by land area.",
            "most populated country": "China is the most populated country in the world, followed closely by India.",
        }
        
        # Clean the question - remove common question words and punctuation
        cleaned_question = question.lower().strip('?.,!').replace("where is ", "").replace("what is ", "").replace("who is ", "").replace("who was ", "").replace("when did ", "").replace("how many ", "").replace("the ", "")
        
        # First, try exact match with cleaned question
        if cleaned_question in knowledge_base:
            return knowledge_base[cleaned_question]
        
        # Then try to find any key that matches part of the question
        for key, answer in knowledge_base.items():
            # Check if key words are in the question
            key_words = key.split()
            question_words = cleaned_question.split()
            
            # If any significant word from key is in question, it's a match
            for key_word in key_words:
                if len(key_word) > 3 and key_word in cleaned_question:
                    return answer
            
            # Also check if question contains key
            if key in cleaned_question or cleaned_question in key:
                return answer
        
        # Mathematical operations
        if any(op in question for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            try:
                # Simple math parser
                import re
                math_expr = re.search(r'(\d+(?:\.\d+)?)\s*(?:\+|plus|\-|minus|\*|times|\/|divided by)\s*(\d+(?:\.\d+)?)', question)
                if math_expr:
                    num1, num2 = float(math_expr.group(1)), float(math_expr.group(2))
                    if 'plus' in question or '+' in question:
                        return f"The result is {num1 + num2}"
                    elif 'minus' in question or '-' in question:
                        return f"The result is {num1 - num2}"
                    elif 'times' in question or '*' in question:
                        return f"The result is {num1 * num2}"
                    elif 'divided' in question or '/' in question:
                        if num2 != 0:
                            return f"The result is {num1 / num2}"
                        else:
                            return "Cannot divide by zero."
            except:
                pass
        
        # Default response for unknown questions
        return f"I don't have specific information about '{question}'. This is a simulated AI assistant. For real-world applications, this would connect to a knowledge base, search engine, or language model API to provide accurate answers."
        
        # Mathematical operations
        if any(op in question for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            try:
                # Simple math parser
                math_expr = re.search(r'(\d+(?:\.\d+)?)\s*(?:\+|plus|\-|minus|\*|times|\/|divided by)\s*(\d+(?:\.\d+)?)', question)
                if math_expr:
                    num1, num2 = float(math_expr.group(1)), float(math_expr.group(2))
                    if 'plus' in question or '+' in question:
                        return f"The result is {num1 + num2}"
                    elif 'minus' in question or '-' in question:
                        return f"The result is {num1 - num2}"
                    elif 'times' in question or '*' in question:
                        return f"The result is {num1 * num2}"
                    elif 'divided' in question or '/' in question:
                        if num2 != 0:
                            return f"The result is {num1 / num2}"
                        else:
                            return "Cannot divide by zero."
            except:
                pass
        
        # Default response for unknown questions
        return f"I don't have specific information about '{question}'. This is a simulated AI assistant. For real-world applications, this would connect to a knowledge base, search engine, or language model API to provide accurate answers."
    
    def summarize_text(self, text: str) -> str:
        """Function 2: Summarize given text"""
        if not text.strip():
            return "Please provide text to summarize."
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if len(sentences) <= 2:
            return "Text is already quite short. Here it is: " + text
        
        # Simple extractive summarization
        # In a real implementation, you'd use NLP libraries like NLTK, spaCy, or transformers
        
        # Get word frequency
        words = text.lower().split()
        word_freq = {}
        for word in words:
            word = re.sub(r'[^\w\s]', '', word)
            if word and len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            words_in_sentence = sentence.lower().split()
            score = 0
            word_count = 0
            for word in words_in_sentence:
                word = re.sub(r'[^\w\s]', '', word)
                if word in word_freq:
                    score += word_freq[word]
                    word_count += 1
            
            if word_count > 0:
                sentence_scores[sentence] = score / word_count
        
        # Get top sentences (up to 3)
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        summary = '. '.join([sentence for sentence, score in top_sentences]) + '.'
        
        return f"Summary: {summary}"
    
    def generate_creative_content(self, prompt: str) -> str:
        """Function 3: Generate creative content"""
        prompt = prompt.lower().strip()
        
        # Story templates
        if 'story' in prompt or 'tale' in prompt:
            themes = {
                'adventure': [
                    "Once upon a time, in a land far away, a brave explorer set out on a journey to discover the legendary Crystal of Wisdom. Through treacherous mountains and mysterious forests, they faced countless challenges, but their determination never wavered. In the end, they found that the real treasure was the courage they discovered within themselves.",
                    
                    "In the heart of the Amazon rainforest, Dr. Sarah Mitchell stumbled upon an ancient temple hidden beneath centuries of vines. As she ventured deeper into its chambers, she discovered hieroglyphs that told of a civilization far more advanced than anyone had imagined. Her discovery would change the course of history forever."
                ],
                'mystery': [
                    "The old lighthouse keeper had vanished without a trace on a foggy Tuesday night. Detective Reynolds examined the scene carefully - a cup of still-warm tea, a book left open mid-sentence, and a single muddy footprint that didn't belong to the missing man. The mystery deepened when locals mentioned seeing strange lights from the lighthouse that very night.",
                    
                    "When the famous violinist's priceless Stradivarius disappeared from the locked concert hall, everyone suspected theft. But investigator Chen noticed something odd - the security cameras showed no one entering or leaving, yet the violin case remained, perfectly positioned, but empty. The truth would prove stranger than anyone imagined."
                ]
            }
            
            if 'adventure' in prompt:
                import random
                return random.choice(themes['adventure'])
            elif 'mystery' in prompt:
                import random
                return random.choice(themes['mystery'])
            else:
                return themes['adventure'][0]
        
        # Poem templates
        elif 'poem' in prompt or 'poetry' in prompt:
            if 'nature' in prompt:
                return """Beneath the canopy of emerald green,
Where sunlight dances, soft and serene,
The whisper of leaves tells ancient stories,
Of seasons past and natural glories.

Rivers flow with gentle grace,
Through valleys wide and sacred space,
Nature's symphony plays on,
From early dusk to breaking dawn."""
            
            elif 'love' in prompt:
                return """In quiet moments, hearts align,
Two souls that share a bond divine,
Through laughter shared and tears that fall,
Love conquers and transcends it all.

Like flowers blooming in the spring,
True love makes the spirit sing,
A gentle touch, a knowing glance,
Life's most beautiful romance."""
            
            else:
                return """Words flow like rivers to the sea,
Carrying thoughts both wild and free,
In verses crafted with delight,
Poetry brings darkness into light.

Each stanza holds a different view,
Of life and all that we've been through,
In rhythm, rhyme, and meter's beat,
Poetry makes our souls complete."""
        
        # Essay topics
        elif 'essay' in prompt:
            if 'technology' in prompt:
                return """Technology and Human Connection in the Digital Age

In our increasingly connected world, technology serves as both a bridge and a barrier to human relationships. While digital platforms allow us to communicate instantly across vast distances, they also raise questions about the quality and authenticity of our interactions.

On one hand, technology has democratized communication, enabling people from different cultures and backgrounds to share ideas and experiences. Social media, video calls, and messaging apps have maintained relationships that might otherwise have been lost to distance and time.

However, the convenience of digital communication sometimes comes at the cost of deeper, more meaningful connections. The nuances of face-to-face conversation - body language, tone, and immediate emotional response - can be lost in digital translation.

The key lies in finding balance: using technology as a tool to enhance rather than replace genuine human connection, and being mindful of when digital interaction serves us well and when it falls short of our deeper needs for authentic relationship."""
            
            else:
                return """The Power of Curiosity in Learning and Growth

Curiosity is perhaps the most undervalued yet powerful force in human development. It is the spark that ignites learning, drives innovation, and pushes the boundaries of what we thought possible.

From childhood, curiosity manifests as endless questions about how things work and why things are the way they are. This natural inclination, if nurtured, becomes the foundation for lifelong learning and personal growth.

In professional settings, curious individuals tend to be more adaptable, creative, and successful. They ask better questions, seek diverse perspectives, and are willing to challenge assumptions - all crucial skills in our rapidly changing world.

Cultivating curiosity requires creating space for wonder, embracing uncertainty, and viewing mistakes as learning opportunities rather than failures. In doing so, we not only enrich our own lives but contribute to a more innovative and understanding society."""
        
        # Default creative response
        return f"Here's a creative piece inspired by '{prompt}':\n\nIn a world where imagination knows no bounds, ideas take flight like birds against an endless sky. Each thought becomes a brushstroke on the canvas of possibility, painting stories yet untold and dreams waiting to unfold. The creative spirit within us all whispers of adventures beyond the horizon, inviting us to explore the infinite landscapes of human expression and wonder."
    
    def get_study_advice(self) -> str:
        """Function 4: Provide study advice"""
        tips = [
            "1. Create a dedicated study space: Find a quiet, organized area free from distractions where you can focus completely on your work.",
            
            "2. Use the Pomodoro Technique: Study for 25-minute focused intervals, followed by 5-minute breaks. After 4 cycles, take a longer 15-30 minute break.",
            
            "3. Active recall over passive reading: Instead of just re-reading notes, test yourself by trying to recall information from memory.",
            
            "4. Teach someone else: Explaining concepts to others (or even to yourself out loud) helps identify gaps in understanding.",
            
            "5. Create visual aids: Use mind maps, diagrams, and flowcharts to organize complex information in visual formats.",
            
            "6. Practice spaced repetition: Review material at increasing intervals (1 day, 3 days, 1 week, 2 weeks) to strengthen long-term memory.",
            
            "7. Eliminate distractions: Put your phone in another room, use website blockers, and create a study environment conducive to focus.",
            
            "8. Take care of your physical health: Get adequate sleep, eat nutritious meals, stay hydrated, and exercise regularly.",
            
            "9. Use multiple senses: Read aloud, write notes by hand, use different colors, and create associations with sounds or images.",
            
            "10. Set specific, achievable goals: Instead of 'study biology,' try 'complete chapter 5 and create flashcards for key terms.'"
        ]
        
        return "Here are some effective study tips:\n\n" + "\n\n".join(tips) + "\n\nRemember: consistency is more important than intensity. Regular, focused study sessions are more effective than cramming!"