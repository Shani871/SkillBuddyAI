from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai.language_models import TextGenerationModel

from SkillBuddyAI import settings

def get_gemini_response(prompt):
    try:
        # Path to your service account JSON file (replace with your actual file path)
        credentials = service_account.Credentials.from_service_account_file(
            'path/to/your/service-account-file.json'  # Use the correct file path
        )

        # Initialize the AI platform with credentials
        aiplatform.init(credentials=credentials, project=settings.GOOGLE_PROJECT_ID)

        # Initialize the TextGenerationModel
        model = TextGenerationModel.from_pretrained("gemini-1.5-flash")

        # Call the predict method
        response = model.predict(
            prompt,
            temperature=0.7,          # Adjust temperature if needed
            max_output_tokens=256     # Set the max output length
        )

        return response.text  # Extract the generated text
    except Exception as e:
        return f"Error: {str(e)}"