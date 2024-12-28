from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load questions from JSON file
with open('data/questions.json') as f:
    questions = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Initialize session variables for the quiz
        session['score'] = 0
        session['current_question'] = 0
        session['answers'] = []
        return redirect(url_for('question'))
    return render_template('quiz.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    # Get the current question index
    current_question_index = session.get('current_question', 0)

    if current_question_index >= len(questions):
        # If we've reached the end of the quiz, redirect to the result page
        return redirect(url_for('result'))

    current_question = questions[current_question_index]

    if request.method == 'POST':
        # Get the user's selected option
        selected_option = request.form.get('option')

        # Save the answer in the session
        session['answers'].append(selected_option)

        # Check if the answer is correct and update the score
        correct_answer = current_question['answer']
        if selected_option == correct_answer:
            session['score'] += 1

        # Move to the next question
        session['current_question'] += 1
        return redirect(url_for('question'))

    # Render the current question
    return render_template('question.html', question=current_question, q_num=current_question_index + 1)

@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(questions)
    return render_template('result.html', score=score, total=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
