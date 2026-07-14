import uuid

import gradio as gr
from dotenv import load_dotenv

from agents import Runner

from agents_config import get_agent, get_persona_names
from sessions import get_session

load_dotenv()


# --------------------------------------------------------------------
# Chat callback
# --------------------------------------------------------------------

async def chat(message, history, username, persona, session_id):

    if history is None:
        history = []
    else:
        history = history.copy()

    if not username.strip():
        username = "guest"

    session = get_session(
        username=username,
        session_id=session_id,
    )

    agent = get_agent(persona)

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

            yield (
                "",
                history,
                session_id,
            )


# --------------------------------------------------------------------
# Persona changed
# --------------------------------------------------------------------

def persona_changed(persona):

    return (
        [],
        str(uuid.uuid4()),
    )


# --------------------------------------------------------------------
# UI
# --------------------------------------------------------------------

with gr.Blocks() as demo:

    gr.Markdown("# Personality-Driven Assistant")

    session_state = gr.State(str(uuid.uuid4()))

    username = gr.Textbox(
        label="Username",
        value="Carl",
    )

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
            username,
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
            username,
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