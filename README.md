# Riddle Me This

A web-based riddle game built with Flask, HTML, CSS, and JavaScript.

## Description

"Riddle Me This" is an interactive web game that challenges players with a series of riddles. Players earn points for correct answers and can compete for high scores. The game includes features like timing, hints, and a persistent leaderboard.

## Features

- Interactive web-based interface
- Collection of challenging riddles
- Scoring system (1 point per correct answer)
- Timer to track time spent on each riddle
- Hints provided after 2 failed attempts
- High score system stored in a CSV file
- Responsive design for various screen sizes

## Project Structure

```
riddle-me-this/
├── app.py                 # Flask application
├── high_scores.csv        # High scores data file
├── riddle_me_this.py      # Original console version
├── static/
│   └── css/
│       └── style.css      # CSS styles
└── templates/
    ├── game.html          # Game page template
    ├── game_over.html     # Game over page template
    ├── highscores.html    # High scores page template
    └── welcome.html       # Welcome page template
```

## Installation and Setup

1. Make sure you have Python 3 installed
2. Install Flask:
   ```
   pip install flask
   ```
3. Navigate to the project directory:
   ```
   cd riddle-me-this
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## How to Play

1. Enter your name on the welcome screen
2. Read each riddle carefully
3. Type your answer in the input box and click "Submit"
4. After 2 wrong attempts, a hint will be displayed
5. Try to solve all riddles as quickly as possible
6. View your final score and time at the end
7. Check the high scores to see how you rank

## Customization

To add more riddles, edit the `RIDDLES` list in `app.py`. Each riddle should be a dictionary with "question", "answer", and "hint" keys.

## License

This project is open source and available for personal and educational use.

## Author

Created by Yusra Liaqat
