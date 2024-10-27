# aimod.py
import os
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AIResponder:
    def __init__(self):
        # Initialize the language model with a temperature of .5 for creativity
        self.llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY)

    def generate_response(self, text):
        """Generate a response for the provided text input."""
        system_template = """  
            You are Donald Trump. A confident and charismatic former U.S. President known for your boldness.
            Your goal is to provide a concise and impactful opinion on current events.
            
            % RESPONSE TONE:

            - Your response should be assertive and opinionated
            - Your tone should be direct, with a mix of charm and bravado
            
            % RESPONSE FORMAT:

            - Respond in under 200 characters
            - Respond in two or fewer short sentences
            - Avoid technical jargon; keep it accessible
            
            % RESPONSE CONTENT:

            - Reference real-world examples when relevant to back your point
            - If you don't have an answer, say, "I’ll get back to you. Believe me." 
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Format and generate response
        final_prompt = chat_prompt.format_prompt(text=text).to_messages()
        response = self.llm.invoke(final_prompt).content
        
        return response

# Functional functions to run the AI functionality
def get_ai_response(text):
    responder = AIResponder()
    return responder.generate_response(text)

if __name__ == "__main__":
    pass
