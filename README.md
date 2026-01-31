# Apak's BMI Calculus
#### Video Demo: https://youtu.be/BaxW1SrqfN4
#### Description:

"Apak's BMI Calculus" is not your ordinary health tool. It is a web-based BMI calculator built with Python (Flask) that combines rigorous mathematical precision with a touch of humor and personality.

Most BMI calculators are boring tables of numbers. My goal was to create an experience that "defines" the user, offering personalized feedback, visual cues, and "Troll" modes for edge cases.

### Features:
- **Dynamic Glassmorphism UI:** The interface features a modern, frosted-glass design that adapts to the user's results.
- **Micro-Detailed Analysis:** Instead of broad ranges, the app provides specific feedback for every BMI integer (e.g., specific advice for BMI 19 vs BMI 20).
- **Troll & Edge Case Detection:**
  - **Hobbit Mode:** If height is <150cm, the app assumes you are a Hobbit.
  - **Titan Mode:** If height is >210cm, special "Titan" feedback is triggered.
  - **Glitch Protection:** Inputs that defy physics (negative numbers, etc.) trigger a system failure screen.
- **Local Static Assets:** All memes and reaction images are served locally to ensure stability.

### Technical Details:
The project uses **Flask** as the backend framework.
- `app.py`: Handles the routing and logic. It processes the POST requests from the form, performs the BMI calculation, and determines the "mood" (color, image, message) of the result.
- `templates/`: Contains the Jinja2 templates (`index.html`, `result.html`, `troll.html`). I used Jinja2 inheritance and dynamic class injection to change the UI colors based on the Python logic.
- `static/`: Stores the CSS styles (embedded in HTML for this project) and the collection of reaction images.

### How to Run:
1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the Flask application:
   `flask run`
3. Open the local link provided in the terminal.
