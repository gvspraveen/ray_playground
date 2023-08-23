from ray import serve
from fastapi import FastAPI
import openai
import os

# Create Open API key here : https://app.endpoints.anyscale.com/
open_api_key = os.getenv('OPENAI_API_KEY')
open_api_base = "https://api.endpoints.anyscale.com/v1"

openai.api_key = open_api_key
openai.api_base = open_api_base

# Using LLM as text classifier. Here I am using LLama-2 70b model to classify error summary as either Python code issue or missing dependency error or Node termination errors.
# I used Chain of thought prompting technique: https://www.promptingguide.ai/techniques/cot
# I also explored more advanced techniques like: Clue And Reasoning Prompting (CARP) technique proposed in paper from Cornell University: https://arxiv.org/abs/2305.08377.
# But In this case CARP seemed overkill with no additional performance gain.

system_content = """
You are an error type classifier for error SUMMARY. Classify the ERROR_TYPE of the SUMMARY as one of PYTHON_CODE_ISSUE or MISSING_DEPENDENCY or NODE_FAILURE

Examples:
SUMMARY: The trial actor was not properly cached. Please ensure that the `reset_config()` method is implemented and returns `True` to enable trainable runner reuse.
ERROR_TYPE: Let's think step-by-step. Summary does not refer to any failed nodes or termination issues. It is also not talking about a missing import or dependency. Instead summary suggests the code was not correctly implemented. So ERROR_TYPE: PYTHON_CODE_ISSUE

SUMMARY: Your environment does not have 'gputil' installed which is required for GPU system monitoring. pip install gputil
ERROR_TYPE: Let's think step-by-step. The summary states that a library needed to run the code is not present. Also there is a suggestion to install a library. This is a case of missing dependency and so ERROR_TYPE: MISSING_DEPENDENCY

SUMMARY: This error indicates that the Ray Actor, in this case the PPO reinforcement learning algorithm, has failed unexpectedly. This generally occurs when the node running the actor has failed
ERROR_TYPE: Let's think step-by-step. The summary states that a Ray actor has failed. Even though it refers to Ray, it is clear that it failure is due to node failing or terminated and nothing to do with usage of Ray. So ERROR_TYPE: NODE_FAILURE

Do not use external sources unless you are highly confident. If you don't know the answer, just say that you don't know.
If you see multiple SUMMARY in the given input, then just return multiple choices with each choice having summary and error_type you predicted.
"""

query_template = """
SUMMARY: {summary}
"""

app = FastAPI()
@serve.deployment(ray_actor_options={"num_gpus": 1})
@serve.ingress(app)
class QADeployment:
    def __init__(self):
        self.api_base = open_api_base
        self.api_key = open_api_key
        
    def __query__(self, err_summary: str):        
        completion = openai.ChatCompletion.create(
            api_base=self.api_base,
            api_key=self.api_key,
            model="meta-llama/Llama-2-70b-chat-hf",
            messages=[{"role": "system", "content": system_content}, 
                    {"role": "user", "content": query_template.format(summary=err_summary)}],
            temperature=0.9,
            max_tokens=4000
         )
        return completion
    
    @app.post("/classify")
    async def classify(self, err_summary: str):
        return self.__query__(err_summary)

# Deploy the Ray Serve application.
deployment = QADeployment.bind()