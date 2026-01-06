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
        "Predict the additive color mixing result. Two colored light sources are shown on the left and right. A white rectangular border marks the mixing zone in the center. Fill the marked zone with the color that results from combining these two lights using additive color mixing rules.",
        "Apply additive color mixing principles. Observe the two colored lights positioned on the left and right sides. The white-bordered rectangular area in the center is the mixing zone. Display the resulting mixed color inside this marked zone.",
        "Demonstrate additive color mixing. The image shows two light sources of different colors. The center region is marked with a white rectangular outline. Predict and show what color appears in the marked mixing zone when these two lights combine.",
        "Two colored light sources are displayed. A rectangular zone marked with a white border indicates where the lights will mix. Using additive color mixing rules, determine the resulting color and display it within the marked zone.",
    ],

    "primary": [
        "Predict the additive color mixing result using primary light colors. Two primary colored lights are positioned on the left and right. Fill the white-bordered mixing zone in the center with the resulting secondary color.",
        "Apply additive mixing with primary lights. The white rectangular border marks where the two primary colored lights will combine. Show the resulting color in this marked zone.",
    ],

    "secondary": [
        "Show the additive mixing result. Two colored lights will combine in the white-bordered rectangular zone at the center. Display the resulting secondary color inside the marked area.",
        "Demonstrate color combination. The white rectangular outline marks the mixing zone. Predict and fill this zone with the color that results from additively mixing the two light sources shown.",
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
