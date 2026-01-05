# Color Mixing Data Generator

A synthetic data generator for additive color mixing reasoning tasks.

---

## Overview

This generator creates visual reasoning tasks that demonstrate additive color mixing principles. Each task shows two colored light sources and challenges the model to predict the result when they mix in a designated zone.

**Task Type**: Physics Worlds - Color Mixing (Additive)

**Domain**: `color_mixing`

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/reasoning-task-generators/color-mixing-data-generator.git
cd color-mixing-data-generator

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python examples/generate.py --num-samples 50
```

---

## Task Description

### Initial State
- Black background
- Two randomly colored light sources (left and right)
- White rectangular border marking the mixing zone in the center

### Task
Predict the result of additive color mixing when the two light sources overlap.

### Final State
- Same light sources
- Mixing zone filled with the physically correct mixed color

### Video (Optional)
Animated transition showing the two colors gradually blending in the mixing zone.

---

## Output Format

Each task generates:

```
data/questions/color_mixing_task/{task_id}/
├── first_frame.png          # Initial state with two light sources
├── final_frame.png          # Final state with mixed color
├── prompt.txt               # Task instruction
└── ground_truth.mp4         # Solution video (optional)
```

---

## Color Mixing Rules

Uses RGB additive color mixing (light mixing):

- **Red + Green = Yellow**
- **Red + Blue = Magenta**
- **Green + Blue = Cyan**
- **Any Color 1 + Any Color 2 = Component-wise Addition (clamped to 255)**

Formula:
```
result_R = min(color1_R + color2_R, 255)
result_G = min(color1_G + color2_G, 255)
result_B = min(color1_B + color2_B, 255)
```

---

## Configuration

Customize generation in `src/config.py`:

```python
domain: str = "color_mixing"
image_size: tuple[int, int] = (512, 512)
light_radius: int = 80              # Light source radius
mixing_zone_size: int = 120         # Mixing zone size
generate_videos: bool = True        # Enable video generation
video_fps: int = 10                 # Video frame rate
```

---

## Examples

### Generate with specific seed
```bash
python examples/generate.py --num-samples 100 --seed 42
```

### Generate without videos
```bash
python examples/generate.py --num-samples 50 --no-videos
```

### Custom output directory
```bash
python examples/generate.py --num-samples 50 --output data/my_tasks
```

---

## Project Structure

```
color-mixing-data-generator/
├── core/                    # Framework utilities (do not modify)
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # Task implementation
│   ├── generator.py        # Color mixing generator
│   ├── prompts.py          # Prompt templates
│   └── config.py           # Configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## Requirements

- Python >= 3.8
- numpy >= 1.26.4
- Pillow >= 10.4.0
- pydantic >= 2.10.5
- opencv-python >= 4.10.0 (for video generation)

---

## License

MIT License
