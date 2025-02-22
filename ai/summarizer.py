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

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

def summarize_text(text, max_tokens=500):
    """
    Summarizes the given text using the Gemini API and formats the output into well-structured points.

    Args:
        text (str): The text to summarize.
        max_tokens (int): Maximum length of the summary.

    Returns:
        str: The formatted and summarized text in points.
    """
    try:
        prompt = f"""
Summarize the following text in detail, using no more than {max_tokens} words and no less than 200 words. 
The summary should be:
1. Explanatory: Cover all key points and details from the text.
2. Structured: Organized into clear, numbered points for easy understanding.
3. Student-Friendly: Use simple language and provide explanations where necessary.
4. Engaging: Make the summary interesting and easy to follow.

Text to summarize:
{text}
"""
        response = model.generate_content(prompt)
        
        # Clean up the summary
        cleaned_summary = response.text.replace("**", "")  # Remove asterisks
        cleaned_summary = cleaned_summary.replace("*", "")  # Remove asterisks
        cleaned_summary = cleaned_summary.replace("  ", " ")  # Remove double spaces
        
        # Format the summary into separate lines
        formatted_summary = "\n".join([line.strip() for line in cleaned_summary.split("\n") if line.strip()])
        
        return formatted_summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary generation failed. Please try again."
