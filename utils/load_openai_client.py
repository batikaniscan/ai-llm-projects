from dotenv import load_dotenv
import os
from openai import OpenAI
import sys

def create_openai_client():
    """
    Creates an OpenAI client using API key from .env file
    Returns:
        OpenAI: Configured OpenAI client object
    Raises:
        ValueError: If API key is not found in .env
        Exception: For other initialization errors
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        # Create OpenAI client
        client = OpenAI(api_key=api_key)
        return client
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    client = create_openai_client()
    print("OpenAI client successfully initialized!")