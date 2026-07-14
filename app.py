import os
import uuid

import gradio as gr
from dotenv import load_dotenv

from agents import Runner

from agents_config import get_agent, get_persona_names
from sessions import get_session

load_dotenv()

DEFAULT_USER = "default"


async def chat(message, history, persona, session_id):

    history = history.copy()

    agent = get_agent(persona)

    session = get_session(session_id)

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": "",
        }
    )

    result = Runner.run_streamed(
        starting_agent=agent,
        input=message,
        session=session,
    )

    assistant_response = ""

    async for event in result.stream_events():

        if (
            event.type == "raw_response_event"
            and event.data.type == "response.output_text.delta"
        ):

            assistant_response += event.data.delta

            history[-1]["content"] = assistant_response

            yield "", history, session_id


def persona_changed(persona):

    new_session_id = str(uuid.uuid4())

    return [], new_session_id


with gr.Blocks() as demo:

    gr.Markdown("# Personality-Driven Assistant")

    session_state = gr.State(str(uuid.uuid4()))

    persona = gr.Dropdown(
        choices=get_persona_names(),
        value=get_persona_names()[0],
        label="Assistant Personality",
    )

    chatbot = gr.Chatbot(
        height=500,
    )

    message = gr.Textbox(
        label="Message",
        placeholder="Type your message...",
    )

    send = gr.Button("Send")

    send.click(
        fn=chat,
        inputs=[
            message,
            chatbot,
            persona,
            session_state,
        ],
        outputs=[
            message,
            chatbot,
            session_state,
        ],
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
            persona,
            session_state,
        ],
        outputs=[
            message,
            chatbot,
            session_state,
        ],
    )

    persona.change(
        fn=persona_changed,
        inputs=persona,
        outputs=[
            chatbot,
            session_state,
        ],
    )


if __name__ == "__main__":
    demo.launch()