from dotenv import load_dotenv
load_dotenv()
from graph.workflow import app

response = app.invoke({
    "user_query": "what will be quartic power of 34?"
})

print("Result", response)