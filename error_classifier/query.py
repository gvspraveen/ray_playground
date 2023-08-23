import sys
import requests

# first run the service locally: serve run serve:deployment
# question = sys.argv[1]

# err_summary = """
# he actor died unexpectedly before finishing this task.
# The actor died due to an unexpected error. Check the task logs for more information.
# Check the task logs for more information and make sure the actor is properly configured.
# Node Id: 627b95ed76acabf6e9d7035aca73133581b7348f98cf4bb542364e4f
# The node that the actor was running on died. Check the node logs for more information.
# Check the node logs for more information and make sure the node is properly configured.
# The actor never ran - it was cancelled before it started running.
# The actor was cancelled before it started running. Check the task logs for more information.
# Check the task logs for more information and make sure the actor is properly configured.
# Terminated with signal 15
# The autoscaler failed with an unexpected error. Check the autoscaler logs for more information.
# Check the autoscaler logs for more information and make sure the autoscaler is properly configured.
# Attempting to recover lost objects by resubmitting their tasks
# The system is attempting to recover lost objects by resubmitting their tasks. This may cause some tasks to be retried.
# Wait for the retries to complete and check the task logs for more information.
# """

err_summary="""
The error occurred when importing the 'jax' library, which is required by the TensorFlow Lite API. The version of jaxlib installed on the system is 0.4.6, but the minimum required version is 0.4.7.
Upgrade jaxlib to version 0.4.7 or higher.
Terminal fix
pip install -U jaxlib==0.4.7
"""

response = requests.post(
    "http://127.0.0.1:8000/classify", params={"err_summary": err_summary}
)
print(response.content.decode())