from fastapi import FastAPI
from google.cloud import bigquery, pubsub_v1
import openai
import os
import json

app = FastAPI()
client = bigquery.Client()

openai.api_key = os.getenv("OPENAI_API_KEY")

project_id = "your-gcp-project-id"
topic_id = "analyzed-feedback-topic"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def analyze_with_llm(feedback_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyse le sentiment."},
            {"role": "user", "content": feedback_text}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

@app.post("/analyze_feedback/")
async def analyze_feedback(feedback: dict):
    feedback_id = feedback["feedback_id"]
    feedback_text = feedback["feedback_text"]
    sentiment = analyze_with_llm(feedback_text)

    query = f"""
    UPDATE customer_feedback
    SET sentiment = '{sentiment}', processed = TRUE, model_used = 'ChatGPT'
    WHERE feedback_id = '{feedback_id}'
    """
    client.query(query).result()

    publisher.publish(topic_path, json.dumps({"feedback_id": feedback_id, "sentiment": sentiment}).encode("utf-8"))

    return {"feedback_id": feedback_id, "sentiment": sentiment}
