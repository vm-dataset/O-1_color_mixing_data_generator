"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK PROMPTS                                   ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define prompts/instructions for your task.            ║
║  Prompts are selected based on task type and returned to the model.           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Predict the additive color mixing result. Show how the two light sources combine in the marked mixing zone.",
        "Demonstrate additive color mixing. Visualize the overlapping light beams merging to create a new color.",
        "Apply additive color mixing rules. Animate the two colored lights blending together in the designated area.",
        "Show the result of combining these colored lights using additive color mixing principles.",
    ],

    "primary": [
        "Predict the additive color mixing result using primary light colors. Show the combination in the mixing zone.",
        "Demonstrate how primary colored lights mix additively to produce a new color.",
    ],

    "secondary": [
        "Show the additive mixing result. Two colored lights combine to create a secondary color.",
        "Apply additive color mixing. The overlapping light beams will produce a distinct secondary color.",
    ],
}


def get_prompt(task_type: str = "default") -> str:
    """
    Select a random prompt for the given task type.

    Args:
        task_type: Type of task (key in PROMPTS dict)

    Returns:
        Random prompt string from the specified type
    """
    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    return random.choice(prompts)


def get_all_prompts(task_type: str = "default") -> list[str]:
    """Get all prompts for a given task type."""
    return PROMPTS.get(task_type, PROMPTS["default"])
