import google.generativeai as genai
from datetime import datetime, timedelta
# Set up the Gemini API key
import os

# ✅ Completely suppress gRPC warnings
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load .env file securely
load_dotenv(override=True)

# ✅ Get API Key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

def generate_study_plan(tasks):
    """
    Generates a smart study plan using the Gemini API and formats the output for better readability.

    Args:
        tasks (list): List of tuples (task_name, deadline_date).

    Returns:
        list: List of tuples (task_name, study_date, study_hours, study_plan).
    """
    study_plan = []

    for task, deadline in tasks:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        days_remaining = (deadline_date - datetime.today()).days

        if days_remaining <= 0:
            study_plan.append((task, "ASAP", days_remaining, "The Time has passed or PLease be Quick to Complete Your Task, but Do not Lose hope."))
            continue

        # Generate a smart study plan using Gemini
        prompt = f"""
        Create a detailed study plan for the following task:
        - Task: {task}
        - Deadline: {deadline}
        - Days remaining: {days_remaining}

        The study plan should:
        1. Break the task into manageable subtasks.
        2. Allocate study hours for each subtask.
        3. Suggest optimal study dates based on the deadline.
        4. Include tips for effective studying.

        Provide the output in the following format:
        - Subtask 1: [description] on [date] for [hours] hours.
        - Subtask 2: [description] on [date] for [hours] hours.
        """
        response = model.generate_content(prompt)
        
        # Clean up the study plan
        cleaned_plan = response.text.replace("**", "")  # Remove asterisks
        cleaned_plan = cleaned_plan.replace("*", "")  # Remove asterisks
        cleaned_plan = cleaned_plan.replace("  ", " ")  # Remove double spaces
        
        # Format the study plan into separate lines
        formatted_plan = "\n".join([line.strip() for line in cleaned_plan.split("\n") if line.strip()])
        
        study_plan.append((task, deadline, days_remaining, formatted_plan))

    return study_plan