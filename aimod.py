# aimod.py
from process_text import remove_quotes
from templates import gen_system_template
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from environs import Env
env = Env()
env.read_env('.env')

# Load OpenAI API key from environment variables
OPENAI_API_KEY = env("OPENAI_API_KEY")

class AIResponder:
    def __init__(self):
        # Initialize the language model with a temperature of .5 for creativity
        self.llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY)

    def generate_response(self, text):
        """Generate a response for the provided text input."""
        system_template = gen_system_template()
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
    result = responder.generate_response(text).strip("'\"")
    layer2_text_strip = remove_quotes(result)
    return layer2_text_strip

if __name__ == "__main__":
    pass

# Generate a new quote
text = "Generate a quote"
quote = get_ai_response(text)
# Post the tweet
print("Tweeting: ", quote)