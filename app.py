#!/usr/bin/env python3
"""
Riddle Me This - Web GUI version
Flask backend for the riddle game
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import time
import csv
import random
import json
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# List of riddles with questions, answers, and hints
RIDDLES = [
    {
        "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "answer": "echo",
        "hint": "You might hear me in mountains or empty rooms."
    },
    {
        "question": "What has keys but no locks, space but no room, and you can enter but not go in?",
        "answer": "keyboard",
        "hint": "You're using me right now to play this game."
    },
    {
        "question": "What gets wet while drying?",
        "answer": "towel",
        "hint": "You use me after taking a shower."
    },
    {
        "question": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
        "answer": "map",
        "hint": "I help you find your way when you're lost."
    },
    {
        "question": "What can you break, even if you never pick it up or touch it?",
        "answer": "promise",
        "hint": "It's something you give your word on."
    },
    {
        "question": "What has a head and a tail, but no body?",
        "answer": "coin",
        "hint": "You might flip me to make a decision."
    },
    {
        "question": "What can travel around the world while staying in a corner?",
        "answer": "stamp",
        "hint": "I help letters reach their destination."
    }
]

HIGH_SCORES_FILE = "high_scores.csv"

def ensure_high_scores_file_exists():
    """Create the high scores file if it doesn't exist."""
    if not os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Score', 'Time', 'Date'])

def save_score(player_name, score, total_time):
    """Save the player's score to the high scores file."""
    ensure_high_scores_file_exists()
    
    with open(HIGH_SCORES_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            player_name, 
            score, 
            f"{total_time:.2f}", 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

def get_high_scores(limit=10):
    """Get the top scores from the high scores file."""
    ensure_high_scores_file_exists()
    
    high_scores = []
    try:
        with open(HIGH_SCORES_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            
            scores = []
            for row in reader:
                if len(row) >= 3:  # Ensure we have at least name, score, and time
                    scores.append({
                        'name': row[0],
                        'score': int(row[1]),
                        'time': float(row[2]),
                        'date': row[3] if len(row) > 3 else "Unknown"
                    })
            
            # Sort by score (descending) and then by time (ascending)
            scores.sort(key=lambda x: (-x['score'], x['time']))
            high_scores = scores[:limit]
    except Exception as e:
        print(f"Error reading high scores: {e}")
    
    return high_scores

def initialize_game(player_name):
    """Initialize a new game session."""
    # Shuffle riddles for variety
    shuffled_riddles = random.sample(RIDDLES, len(RIDDLES))
    
    # Set up session data
    session['player_name'] = player_name
    session['riddles'] = shuffled_riddles
    session['current_riddle'] = 0
    session['score'] = 0
    session['attempts'] = 0
    session['start_time'] = time.time()
    session['riddle_start_time'] = time.time()
    session['riddle_times'] = []
    session['show_hint'] = False

@app.route('/')
def index():
    """Render the main game page or welcome page."""
    if 'player_name' not in session:
        return render_template('welcome.html')
    
    # If game is in progress, show the current riddle
    if 'riddles' in session and 'current_riddle' in session:
        current_riddle_index = session['current_riddle']
        riddles = session['riddles']
        
        if current_riddle_index < len(riddles):
            current_riddle = riddles[current_riddle_index]
            return render_template(
                'game.html',
                player_name=session['player_name'],
                riddle=current_riddle['question'],
                current_riddle=current_riddle_index + 1,
                total_riddles=len(riddles),
                score=session['score'],
                show_hint=session['show_hint'],
                hint=current_riddle['hint'] if session['show_hint'] else None,
                attempts=session['attempts']
            )
    
    # Default to welcome page if no game in progress
    return render_template('welcome.html')

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game with the provided player name."""
    player_name = request.form.get('player_name', 'Anonymous').strip()
    if not player_name:
        player_name = 'Anonymous'
    
    initialize_game(player_name)
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit_answer():
    """Process the submitted answer."""
    if 'riddles' not in session:
        return redirect(url_for('index'))
    
    user_answer = request.form.get('answer', '').strip().lower()
    
    current_riddle_index = session['current_riddle']
    riddles = session['riddles']
    
    if current_riddle_index >= len(riddles):
        return redirect(url_for('game_over'))
    
    current_riddle = riddles[current_riddle_index]
    correct_answer = current_riddle['answer'].lower()
    
    # Calculate time spent on this riddle
    riddle_time = time.time() - session['riddle_start_time']
    
    # Check if the answer is correct
    is_correct = user_answer == correct_answer
    
    if is_correct:
        session['score'] += 1
        session['attempts'] = 0
        session['show_hint'] = False
        session['riddle_times'].append(riddle_time)
        
        # Move to the next riddle
        session['current_riddle'] += 1
        
        # Check if game is complete
        if session['current_riddle'] >= len(riddles):
            return redirect(url_for('game_over'))
        
        session['riddle_start_time'] = time.time()
    else:
        session['attempts'] += 1
        if session['attempts'] >= 2:
            session['show_hint'] = True
    
    return redirect(url_for('index'))

@app.route('/game_over')
def game_over():
    """Display the game over screen with final score and high scores."""
    if 'player_name' not in session or 'score' not in session:
        return redirect(url_for('index'))
    
    total_time = time.time() - session['start_time']
    save_score(session['player_name'], session['score'], total_time)
    high_scores = get_high_scores()
    
    return render_template(
        'game_over.html',
        player_name=session['player_name'],
        score=session['score'],
        total_riddles=len(session['riddles']),
        total_time=round(total_time, 2),
        high_scores=high_scores
    )

@app.route('/highscores')
def highscores():
    """Display the high scores page."""
    high_scores = get_high_scores()
    return render_template('highscores.html', high_scores=high_scores)

@app.route('/restart')
def restart():
    """Restart the game with the same player name."""
    if 'player_name' in session:
        player_name = session['player_name']
        initialize_game(player_name)
    return redirect(url_for('index'))

@app.route('/quit')
def quit_game():
    """Quit the game and clear the session."""
    session.clear()
    return redirect(url_for('index'))

@app.route('/skip')
def skip_riddle():
    """Skip the current riddle."""
    if 'riddles' not in session:
        return redirect(url_for('index'))
    
    current_riddle_index = session['current_riddle']
    riddles = session['riddles']
    
    if current_riddle_index >= len(riddles):
        return redirect(url_for('game_over'))
    
    # Record time for skipped riddle
    riddle_time = time.time() - session['riddle_start_time']
    session['riddle_times'].append(riddle_time)
    
    # Move to the next riddle
    session['current_riddle'] += 1
    session['attempts'] = 0
    session['show_hint'] = False
    
    # Check if game is complete
    if session['current_riddle'] >= len(riddles):
        return redirect(url_for('game_over'))
    
    session['riddle_start_time'] = time.time()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
