import sys
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
           api_base = self.api_base,
           api_key=self.api_key,
           model = self.model,
           messages = self.message_history,
           stream = True
        )
        words = 'You are a helpful assistant'
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
