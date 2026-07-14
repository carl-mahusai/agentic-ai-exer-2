import os

import gradio as gr
from dotenv import load_dotenv

from agents import Agent, Runner
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

def chat(message, history, persona):
    agent = PERSONA_AGENTS[persona]

    result = Runner.run_sync(
        agent,
        message,
    )

    response = result.final_output

    history.append(
        {"role": "user", "content": message}
    )
    history.append(
        {"role": "assistant", "content": response}
    )

    return "", history


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
        placeholder="Type your message...",
        label="Message",
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