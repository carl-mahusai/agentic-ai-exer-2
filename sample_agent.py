import os

import gradio as gr
from dotenv import load_dotenv

from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------------------------
# Agents per persona
# --------------------------------------------------------------------

engineer = Agent(
    name="The Precise Engineer",
    instructions=(
        "You are concise, technical, and focused on correctness."
        " Keep explanations clear and professional."
    ),
)

tutor = Agent(
    name="The Playful Tutor",
    instructions=(
        "You are friendly and encouraging."
        " Use analogies and light humor to explain concepts."
    ),
)

pirate = Agent(
    name="The Seasoned Pirate",
    instructions=(
        "Ye be an experienced pirate."
        " Always answer in pirate speech while remaining helpful."
    ),
)

PERSONA_AGENTS = {
    "The Precise Engineer": engineer,
    "The Playful Tutor": tutor,
    "The Seasoned Pirate": pirate,
}


# --------------------------------------------------------------------
# Chat callback
# --------------------------------------------------------------------

async def chat(message, history, persona):

    history = history.copy()

    agent = PERSONA_AGENTS[persona]

    history.append(
        {"role": "user", "content": message}
    )

    history.append(
        {"role": "assistant", "content": ""}
    )

    result = Runner.run_streamed(
        agent,
        input=message,
    )

    response = ""

    async for event in result.stream_events():

        if (
            event.type == "raw_response_event"
            and isinstance(event.data, ResponseTextDeltaEvent)
        ):
            response += event.data.delta

            history[-1]["content"] = response

            yield "", history


# --------------------------------------------------------------------
# Persona changed
# --------------------------------------------------------------------

def persona_changed(persona):
    """
    Clears the visible chat.
    Any agent conversation/session would also be reset here.
    """

    return []


# --------------------------------------------------------------------
# UI
# --------------------------------------------------------------------

with gr.Blocks() as demo:

    gr.Markdown("# Personality-Driven Assistant")

    persona = gr.Dropdown(
        choices=list(PERSONA_AGENTS.keys()),
        value="The Precise Engineer",
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
        ],
        outputs=[
            message,
            chatbot,
        ],
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
            persona,
        ],
        outputs=[
            message,
            chatbot,
        ],
    )

    persona.change(
        fn=persona_changed,
        inputs=persona,
        outputs=chatbot,
    )


if __name__ == "__main__":
    demo.launch()