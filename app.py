from flask import Flask, render_template, request, redirect, url_for
import os
import ai.summarizer
from utils.extract_text import extract_text_from_file
from ai.summarizer import summarize_text  # We'll create this later
import ai
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded files

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

from ai.summarizer import summarize_text  # Import the summarizer

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # Extract text from the file
            text = extract_text_from_file(filepath)
            # Summarize the text using the AI summarizer
            summary = summarize_text(text)
            return render_template('notes.html', summary=summary)
    return render_template('notes.html')

from ai.explainer import explain_topic  # Import the explainer

@app.route('/explainer', methods=['GET', 'POST'])
def explainer():
    if request.method == 'POST':
        topic = request.form['topic']
        # Generate explanation using the AI explainer
        explanation = explain_topic(topic)
        return render_template('explainer.html', explanation=explanation)
    return render_template('explainer.html')

from ai.planner import generate_study_plan  # Import the planner

from ai.planner import generate_study_plan  # Import the updated planner

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    if request.method == 'POST':
        tasks = request.form.getlist('task')
        deadlines = request.form.getlist('deadline')
        task_deadlines = list(zip(tasks, deadlines))
        study_plan = generate_study_plan(task_deadlines)
        return render_template('planner.html', study_plan=study_plan)
    return render_template('planner.html')



# Run the app
if __name__ == '__main__':
    app.run(debug=True)