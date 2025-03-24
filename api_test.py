import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCpIfUjFvJgJjz_PtTrpyF7ppEA60HU32Q"
genai.configure(api_key=GEMINI_API_KEY)

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
