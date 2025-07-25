import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

ASSISTANT_ID="asst_KCV0QphfRIr9KwttLxHNKWUB"

def create_thread():
    return client.beta.threads.create()

def send_message(thread_id, message):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

def run_and_stream_response(thread_id):
    stream = client.beta.threads.runs.create(
        assistant_id=ASSISTANT_ID,
        thread_id=thread_id,
        stream=True
    )

    for event in stream:
        # Each event is a `RunStepDelta` or similar event type
        if event.event == "thread.message.delta":
            content_delta = event.data.delta
            if content_delta and content_delta.content:
                yield content_delta.content[0].text.value

