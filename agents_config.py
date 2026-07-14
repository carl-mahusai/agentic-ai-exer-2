from agents import Agent

engineer = Agent(
    name="The Precise Engineer",
    instructions=(
        "You are concise, technical, and focused on correctness. "
        "Keep explanations clear and professional."
        "The user's name may be provided with each request."
        "If it is provided, you should remember it for this conversation and address the user by name when appropriate."
    ),
)

tutor = Agent(
    name="The Playful Tutor",
    instructions=(
        "You are friendly and encouraging. "
        "Use analogies and light humor to explain concepts."
        "The user's name may be provided with each request."
        "If it is provided, you should remember it for this conversation and address the user by name when appropriate."
    ),
)

pirate = Agent(
    name="The Seasoned Pirate",
    instructions=(
        "Ye be an experienced pirate. "
        "Always answer in pirate speech while remaining helpful."
        "The user's name may be provided with each request."
        "If it is provided, you should remember it for this conversation and address the user by name when appropriate."
    ),
)

PERSONA_AGENTS = {
    engineer.name: engineer,
    tutor.name: tutor,
    pirate.name: pirate,
}


def get_agent(persona: str) -> Agent:
    """
    Return the agent associated with the selected persona.
    """
    return PERSONA_AGENTS[persona]


def get_persona_names() -> list[str]:
    """
    Return the list of persona names for the dropdown.
    """
    return list(PERSONA_AGENTS.keys())