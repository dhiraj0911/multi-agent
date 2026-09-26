from dotenv import load_dotenv

load_dotenv()

from graph.workflow import app

response = app.invoke({
    "user_query": "When is BBD sale starting?"
})

print("Result", response)