#!/usr/bin/env python3
"""
Riddle Me This - A text-based riddle game
"""
import os
import time
import csv
import random
from datetime import datetime

class RiddleGame:
    def __init__(self):
        self.score = 0
        self.total_time = 0
        self.player_name = ""
        self.high_scores_file = "high_scores.csv"
        
        # List of riddles with questions, answers, and hints
        self.riddles = [
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
        
        # Shuffle the riddles for variety
        random.shuffle(self.riddles)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_welcome(self):
        """Display welcome message and get player name."""
        self.clear_screen()
        print("=" * 60)
        print("                     RIDDLE ME THIS                     ")
        print("=" * 60)
        print("\nWelcome to 'Riddle Me This', a game of riddles and wit!")
        print("\nInstructions:")
        print("- You will be presented with a series of riddles")
        print("- Type your answer and press Enter")
        print("- Each correct answer earns you 1 point")
        print("- After 2 wrong attempts, you'll get a hint")
        print("- Type 'quit' or 'exit' at any time to end the game")
        print("=" * 60)
        
        while True:
            self.player_name = input("\nPlease enter your name: ").strip()
            if self.player_name and not self.player_name.lower() in ['quit', 'exit']:
                break
            elif self.player_name.lower() in ['quit', 'exit']:
                print("Thanks for stopping by! Goodbye!")
                exit()
            else:
                print("Please enter a valid name.")
        
        input(f"\nWelcome, {self.player_name}! Press Enter to start the game...")
    
    def check_for_quit(self, user_input):
        """Check if the user wants to quit the game."""
        if user_input.lower() in ['quit', 'exit']:
            print("\nThanks for playing! Goodbye!")
            self.display_final_score()
            exit()
    
    def play_game(self):
        """Main game loop."""
        self.display_welcome()
        
        for i, riddle in enumerate(self.riddles):
            self.clear_screen()
            print(f"Riddle {i+1} of {len(self.riddles)}")
            print("=" * 60)
            print(f"\n{riddle['question']}\n")
            print("=" * 60)
            
            attempts = 0
            start_time = time.time()
            
            while attempts < 3:  # Max 3 attempts (original + 2 more with hint)
                if attempts == 2:
                    print(f"\nHint: {riddle['hint']}")
                
                user_answer = input("\nYour answer: ").strip().lower()
                self.check_for_quit(user_answer)
                
                if user_answer == riddle['answer'].lower():
                    end_time = time.time()
                    riddle_time = end_time - start_time
                    self.total_time += riddle_time
                    self.score += 1
                    
                    print(f"\n✓ Correct! Well done!")
                    print(f"Time taken: {riddle_time:.2f} seconds")
                    input("\nPress Enter to continue...")
                    break
                else:
                    attempts += 1
                    if attempts < 3:
                        print(f"\n✗ Sorry, that's incorrect. Try again! (Attempt {attempts}/2)")
                    else:
                        end_time = time.time()
                        riddle_time = end_time - start_time
                        self.total_time += riddle_time
                        
                        print(f"\n✗ Sorry, that's incorrect. The answer was: {riddle['answer']}")
                        print(f"Time taken: {riddle_time:.2f} seconds")
                        input("\nPress Enter to continue...")
        
        self.display_final_score()
    
    def ensure_high_scores_file_exists(self):
        """Create the high scores file if it doesn't exist."""
        if not os.path.exists(self.high_scores_file):
            with open(self.high_scores_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Score', 'Time', 'Date'])
    
    def save_score(self):
        """Save the player's score to the high scores file."""
        self.ensure_high_scores_file_exists()
        
        with open(self.high_scores_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.player_name, 
                self.score, 
                f"{self.total_time:.2f}", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
    
    def get_high_scores(self, limit=5):
        """Get the top scores from the high scores file."""
        self.ensure_high_scores_file_exists()
        
        high_scores = []
        try:
            with open(self.high_scores_file, 'r', newline='') as file:
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
    
    def display_high_scores(self):
        """Display the high scores table."""
        high_scores = self.get_high_scores()
        
        if not high_scores:
            print("\nNo high scores yet!")
            return
        
        print("\n" + "=" * 60)
        print("                     HIGH SCORES                     ")
        print("=" * 60)
        print(f"{'Rank':<6}{'Name':<15}{'Score':<10}{'Time':<10}{'Date':<20}")
        print("-" * 60)
        
        for i, score in enumerate(high_scores):
            print(f"{i+1:<6}{score['name']:<15}{score['score']:<10}{score['time']:<10.2f}{score['date']:<20}")
    
    def display_final_score(self):
        """Display the final score and game over message."""
        self.clear_screen()
        print("=" * 60)
        print("                     GAME OVER                     ")
        print("=" * 60)
        print(f"\nPlayer: {self.player_name}")
        print(f"Final Score: {self.score} out of {len(self.riddles)}")
        print(f"Total Time: {self.total_time:.2f} seconds")
        
        # Calculate performance message
        if self.score == len(self.riddles):
            print("\nPerfect score! You're a riddle master!")
        elif self.score >= len(self.riddles) * 0.7:
            print("\nGreat job! You have an excellent mind for riddles!")
        elif self.score >= len(self.riddles) * 0.5:
            print("\nNot bad! You solved half or more of the riddles!")
        else:
            print("\nBetter luck next time! Riddles can be tricky.")
        
        # Save score and display high scores
        self.save_score()
        self.display_high_scores()
        
        print("\nThanks for playing 'Riddle Me This'!")
        print("=" * 60)
        
        play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if play_again in ['yes', 'y']:
            new_game = RiddleGame()
            new_game.play_game()

if __name__ == "__main__":
    try:
        game = RiddleGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Sorry for the inconvenience!")
