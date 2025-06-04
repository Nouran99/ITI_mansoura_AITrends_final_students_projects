import ollama

class LLMModel:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
    
    def chat_completion(self, system, user, temperature=0.7):
        prompt = f"{system}\n\nUser:\n{user}\n\nAssistant:"
        response = ollama.chat(model=self.model_name, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        print("🧪 Raw API Response:", response)
        return response['message']['content'].strip()
