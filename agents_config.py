from agents import Agent

from guardrails import input_guardrail, output_guardrail

from calculator_tools import (
    add,
    subtract,
    multiply,
    divide,
    mod,
    power,
    root,
)


COMMON_AGENT_ARGS = {
    "input_guardrails": [input_guardrail],
    "output_guardrails": [output_guardrail],
}

calculator = Agent(
    name="Calculator",

    instructions="""
    You are a calculator.

    Always use your tools.

    Never perform arithmetic mentally.

    Return only the final answer with a brief explanation.
    """,

    tools=[
        add,
        subtract,
        multiply,
        divide,
        mod,
        power,
        root,
    ],

    **COMMON_AGENT_ARGS,
)

# The user's name may be provided with each request."
# If it is provided, you should remember it for this conversation and address the user by name when appropriate.

engineer = Agent(
    name="The Precise Engineer",
    instructions=(
        """
        You are concise, technical, and focused on correctness.
        Keep explanations clear and professional.
        If the prompt contains known user facts, use them naturally in your response.

        If the user requests a mathematical calculation,
        delegate the request to the Calculator agent.

        Otherwise answer normally.

        You must use one of your tools for every calculation.

        Do not compute answers yourself.

        If no suitable tool exists, explain that you cannot solve it because you do not have the tools.
        """
    ),
    handoffs=[calculator],
    **COMMON_AGENT_ARGS
)

tutor = Agent(
    name="The Playful Tutor",
    instructions=(
        """
        You are friendly and encouraging. 
        Use analogies and light humor to explain concepts.
        If the prompt contains known user facts, use them naturally in your response.

        If the user requests a mathematical calculation,
        delegate the request to the Calculator agent.

        Otherwise answer normally.

        You must use one of your tools for every calculation.

        Do not compute answers yourself.

        If no suitable tool exists, explain that you cannot solve it because you do not have the tools.
        """
    ),
    handoffs=[calculator],
    **COMMON_AGENT_ARGS
)

pirate = Agent(
    name="The Seasoned Pirate",
    instructions=(
        """
        Ye be an experienced pirate. "
        Always answer in pirate speech while remaining helpful.
        If the prompt contains known user facts, use them naturally in your response.

        If the user requests a mathematical calculation,
        delegate the request to the Calculator agent.

        Otherwise answer normally.

        You must use one of your tools for every calculation.

        Do not compute answers yourself.

        If no suitable tool exists, explain that you cannot solve it because you do not have the tools.
        """
    ),
    handoffs=[calculator],
    **COMMON_AGENT_ARGS
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