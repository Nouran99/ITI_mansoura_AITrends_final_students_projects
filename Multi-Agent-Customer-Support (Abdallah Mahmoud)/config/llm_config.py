import os
from openai import OpenAI
from config.settings import OPENROUTER_API_KEY

# Set environment variables for CrewAI
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

class DeepSeekFreeLLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Fixed model - DeepSeek Chat Free only
        self.model = "deepseek/deepseek-chat:free"
        self.token_usage = 0
        self.max_daily_tokens = 1000000  # Estimate for free tier
    
    def generate_response(self, messages, max_tokens=500, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                extra_headers={
                    "HTTP-Referer": "https://github.com/your-username/support-crew",
                    "X-Title": "Support Crew AI System"
                }
            )
            
            # Track usage
            if hasattr(response, 'usage') and response.usage:
                self.token_usage += response.usage.total_tokens
            else:
                # Estimate tokens if not provided
                self.token_usage += len(str(messages)) + max_tokens
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_usage_stats(self):
        return {
            "tokens_used": self.token_usage,
            "tokens_remaining": max(0, self.max_daily_tokens - self.token_usage),
            "usage_percentage": (self.token_usage / self.max_daily_tokens) * 100 if self.max_daily_tokens > 0 else 0,
            "model": "DeepSeek Chat (Free)",
            "cost": "FREE",
            "provider": "OpenRouter"
        }
    

    def get_llm_config(self):
        """Return LLM configuration for CrewAI"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        
        if not api_key or not base_url:
            raise ValueError("DEEPSEEK_API_KEY and DEEPSEEK_BASE_URL must be set in environment variables")
        
        return {
            "model": f"openai/{self.model}",
            "api_key": api_key,
            "base_url": base_url
        }
    
    
    def test_connection(self):
        """Test if API key and connection work"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True, f"✅ DeepSeek Free via OpenRouter works!"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"

# Global LLM instance
llm = DeepSeekFreeLLM()