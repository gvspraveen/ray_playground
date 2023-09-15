import os 
from scripts.agent import chat

model = "meta-llama-Llama-2-7b-chat-hf"
api_key = os.getenv('ANYSCALE_API_KEY')
api_base = "https://api.endpoints.anyscale.com/v1"

chat(model, api_base, api_key)


# Write a SQL query to answer the question based on the table schema.\n\n context: CREATE TABLE table_name_80 (name VARCHAR, style VARCHAR, status VARCHAR)\n\n question: Who had a ballet style with original cast?
# A rectangle has a length of 4 inches and a width of 6 inches. A square has a width of 5 inches. What is the difference in area between the two shapes?
# John drives for 3 hours at a speed of 60 mph and then turns around because he realizes he forgot something very important at home.  He tries to get home in 4 hours but spends the first 2 hours in standstill traffic.  He spends the next half-hour driving at a speed of 30mph, before being able to drive the remaining time going at 80 mph.  How far is he from home at the end of those 4 hours?
