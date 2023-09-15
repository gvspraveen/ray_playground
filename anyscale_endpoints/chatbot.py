import sys
import os 
import openai

class ChatAgent:
    def __init__(self, model: str, api_key:str, api_base: str):
        self.message_history = []
        self.model = model 
        self.api_key = api_key
        self.api_base = api_base

    def greet(self):
        return None

    def process_input(self, input: str):
        self.update_message_history(input)

        response = openai.ChatCompletion.create(
           api_base = api_base,
           api_key=api_key,
           model = self.model,
           messages = self.message_history,
           stream = True
        )
        words = 'You are good at math'
        for tok in response: 
            delta = tok.choices[0].delta
            if not delta: # End token 
                self.message_history.append({
                    'role': 'assistant',
                    'content': words
                })
                break
            elif 'content' in delta:
                words += delta['content']
                yield delta['content'] 
            else: 
                continue

    def update_message_history(self, inp):
        self.message_history.append({
            'role': 'user',
            'content': inp
        })

def chat(model, api_base, api_key):     
    agent = ChatAgent(model, api_base=api_base, api_key=api_key)
    sys.stdout.write("Let's have a chat. (Enter `quit` to exit)\n") 
    while True: 
        sys.stdout.write('> ')
        inp = input()
        if inp == 'quit':
            break
        for word in agent.process_input(inp):
            sys.stdout.write(word)
            sys.stdout.flush()
        sys.stdout.write('\n')

base_model = "meta-llama-Llama-2-7b-chat-hf"
api_key = os.getenv('ANYSCALE_API_KEY')
api_base = "https://api.endpoints.anyscale.com/v1"

chat(base_model, api_base, api_key)




# Write a SQL query to answer the question based on the table schema.\n\n context: CREATE TABLE table_name_80 (name VARCHAR, style VARCHAR, status VARCHAR)\n\n question: Who had a ballet style with original cast?
# A rectangle has a length of 4 inches and a width of 6 inches. A square has a width of 5 inches. What is the difference in area between the two shapes?
# John drives for 3 hours at a speed of 60 mph and then turns around because he realizes he forgot something very important at home.  He tries to get home in 4 hours but spends the first 2 hours in standstill traffic.  He spends the next half-hour driving at a speed of 30mph, before being able to drive the remaining time going at 80 mph.  How far is he from home at the end of those 4 hours?
