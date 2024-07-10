

# import enums


# # Set up your API key or service account credentials
# # Replace with your actual API key or path to service account JSON file
# api_key = "AIzaSyDNs_3Ov1iAVEL19-1hrEMXqqua7Zcntcs"
# # If using service account credentials:
# # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account.json"

# def analyze_sentiment(text):
#     client = language_v1.LanguageServiceClient()
#     document = {"content": text, "type": enums.Document.Type.PLAIN_TEXT}
#     response = client.analyze_sentiment(document=document)
#     sentiment = response.document_sentiment
#     return sentiment.score, sentiment.magnitude

# # Example usage:


# MODULE 1 - TESTING BASIC PROMPT WITH BARD 

# Importing the libraries
import google.generativeai as genai

# Getting the API Key
genai.configure(api_key = "AIzaSyB7xp-UZWLpITb-3WcHlEQM8NnqzZTBY_4")

# Getting the Model
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Generating the response
response = model.generate_content("ways to improve time efficiency in the workplace")



# Getting the response
print(response.text)