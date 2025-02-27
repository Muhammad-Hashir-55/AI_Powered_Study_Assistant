import google.generativeai as genai
import os
from dotenv import load_dotenv
import apig

# Suppress gRPC warnings
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Load .env file securely
load_dotenv(override=True)

# Get API Key from .env
GEMINI_API_KEY = apig.s

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Initialize Model
model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")
# models = genai.list_models()
# print([m.name for m in models])

def explain_topic(topic):
    """
    Generates an explanation for the given topic using the Gemini API and formats the output into well-structured points.

    Args:
        topic (str): The topic to explain.

    Returns:
        str: The formatted and explained text in points.
    """
    try:
        # Generate the explanation
        prompt = f"""
        Explain the following topic in simple terms suitable for a student.
        Format the explanation into clear, bullet points for easy understanding:
        
        {topic}
        """
        response = model.generate_content(prompt)
        
        # Clean up the explanation
        cleaned_explanation = response.text.replace("**", "")  # Remove asterisks
        cleaned_explanation = cleaned_explanation.replace("*", "")  # Remove asterisks
        cleaned_explanation = cleaned_explanation.replace("  ", " ")  # Remove double spaces
        
        # Format the explanation into separate lines
        formatted_explanation = "\n".join([line.strip() for line in cleaned_explanation.split("\n") if line.strip()])
        
        return formatted_explanation
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return "Explanation generation failed. Please try again."
