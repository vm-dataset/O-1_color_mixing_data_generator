"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK GENERATOR                                 ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to implement your data generation logic.                 ║
║  Replace the example implementation with your own task.                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class TaskGenerator(BaseGenerator):
    """
    Color Mixing (Additive) task generator.

    Generates tasks showing additive color mixing of light sources.

    Required:
        - generate_task_pair(task_id) -> TaskPair

    The base class provides:
        - self.config: Your TaskConfig instance
        - generate_dataset(): Loops and calls generate_task_pair() for each sample
    """

    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)

        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")

    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one color mixing task pair."""

        # Generate task data (select random color pair)
        task_data = self._generate_task_data()

        # Render images
        first_image = self._render_initial_state(task_data)
        final_image = self._render_final_state(task_data)

        # Generate video (optional)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(first_image, final_image, task_id, task_data)

        # Select prompt
        prompt = get_prompt(task_data.get("type", "default"))

        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC METHODS
    # ══════════════════════════════════════════════════════════════════════════

    def _generate_task_data(self) -> dict:
        """
        Generate random color combination with physically correct additive mixing.

        Randomly generates two colors and calculates the additive mixing result
        following RGB light mixing rules (each channel is clamped to max 255).
        """
        # Generate two random colors
        color1 = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        color2 = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        # Calculate additive color mixing result (RGB addition, clamped to 255)
        result = (
            min(color1[0] + color2[0], 255),  # Red channel
            min(color1[1] + color2[1], 255),  # Green channel
            min(color1[2] + color2[2], 255)   # Blue channel
        )

        return {
            "color1": color1,
            "color2": color2,
            "result": result,
            "type": "default"
        }

    def _render_initial_state(self, task_data: dict) -> Image.Image:
        """
        Render initial state: two light sources and mixing zone marker.

        Layout:
        - Black background
        - Two colored light circles (left and right)
        - Mixing zone marked with a rectangle border in the center
        """
        width, height = self.config.image_size
        img = Image.new('RGB', (width, height), color=(0, 0, 0))  # Black background

        # Calculate positions
        light_radius = self.config.light_radius
        mixing_zone_size = self.config.mixing_zone_size

        # Light source positions (left and right)
        left_light_x = width // 4
        right_light_x = 3 * width // 4
        light_y = height // 2

        # Mixing zone position (center)
        mixing_zone_x = (width - mixing_zone_size) // 2
        mixing_zone_y = (height - mixing_zone_size) // 2

        # Draw light sources with radial gradient
        img = self._draw_radial_light(
            img,
            (left_light_x, light_y),
            light_radius,
            task_data["color1"]
        )
        img = self._draw_radial_light(
            img,
            (right_light_x, light_y),
            light_radius,
            task_data["color2"]
        )

        # Draw mixing zone marker (rectangle border)
        draw = ImageDraw.Draw(img)
        border_width = self.config.mixing_zone_border_width
        for i in range(border_width):
            draw.rectangle(
                [
                    mixing_zone_x - i,
                    mixing_zone_y - i,
                    mixing_zone_x + mixing_zone_size + i,
                    mixing_zone_y + mixing_zone_size + i
                ],
                outline=(255, 255, 255),
                width=1
            )

        return img

    def _render_final_state(self, task_data: dict) -> Image.Image:
        """
        Render final state: mixed color appears in the mixing zone.

        Shows the result of additive color mixing.
        """
        width, height = self.config.image_size
        img = Image.new('RGB', (width, height), color=(0, 0, 0))

        # Calculate positions
        light_radius = self.config.light_radius
        mixing_zone_size = self.config.mixing_zone_size

        # Light source positions
        left_light_x = width // 4
        right_light_x = 3 * width // 4
        light_y = height // 2

        # Mixing zone position
        mixing_zone_x = (width - mixing_zone_size) // 2
        mixing_zone_y = (height - mixing_zone_size) // 2

        # Draw light sources (same as initial)
        img = self._draw_radial_light(
            img,
            (left_light_x, light_y),
            light_radius,
            task_data["color1"]
        )
        img = self._draw_radial_light(
            img,
            (right_light_x, light_y),
            light_radius,
            task_data["color2"]
        )

        # Draw mixed color in the mixing zone
        draw = ImageDraw.Draw(img)
        draw.rectangle(
            [
                mixing_zone_x,
                mixing_zone_y,
                mixing_zone_x + mixing_zone_size,
                mixing_zone_y + mixing_zone_size
            ],
            fill=task_data["result"]
        )

        # Draw mixing zone border
        border_width = self.config.mixing_zone_border_width
        for i in range(border_width):
            draw.rectangle(
                [
                    mixing_zone_x - i,
                    mixing_zone_y - i,
                    mixing_zone_x + mixing_zone_size + i,
                    mixing_zone_y + mixing_zone_size + i
                ],
                outline=(255, 255, 255),
                width=1
            )

        return img

    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str,
        task_data: dict
    ) -> str:
        """Generate animation showing additive color mixing process."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"

        # Create animation frames
        frames = self._create_color_mixing_animation(task_data)

        result = self.video_generator.create_video_from_frames(
            frames,
            video_path
        )

        return str(result) if result else None

    def _create_color_mixing_animation(
        self,
        task_data: dict,
        hold_frames: int = 5,
        transition_frames: int = 30
    ) -> list:
        """
        Create animation frames showing color mixing process.

        Animation:
        1. Hold initial state (two light sources, mixing zone marked)
        2. Transition: Light beams gradually overlap in mixing zone
        3. Hold final state (mixed color visible in mixing zone)
        """
        frames = []
        width, height = self.config.image_size

        light_radius = self.config.light_radius
        mixing_zone_size = self.config.mixing_zone_size

        # Positions
        left_light_x = width // 4
        right_light_x = 3 * width // 4
        light_y = height // 2
        mixing_zone_x = (width - mixing_zone_size) // 2
        mixing_zone_y = (height - mixing_zone_size) // 2

        # Initial frame
        initial_frame = self._render_initial_state(task_data)
        for _ in range(hold_frames):
            frames.append(initial_frame.copy())

        # Transition frames: gradually fill mixing zone with mixed color
        for i in range(transition_frames):
            progress = (i + 1) / transition_frames

            # Create base image with light sources
            img = Image.new('RGB', (width, height), color=(0, 0, 0))
            img = self._draw_radial_light(
                img,
                (left_light_x, light_y),
                light_radius,
                task_data["color1"]
            )
            img = self._draw_radial_light(
                img,
                (right_light_x, light_y),
                light_radius,
                task_data["color2"]
            )

            # Gradually fill mixing zone with result color
            # Use alpha blending to create smooth transition
            overlay = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # Draw result color with increasing opacity
            result_color = task_data["result"]
            alpha = int(255 * progress)
            overlay_draw.rectangle(
                [
                    mixing_zone_x,
                    mixing_zone_y,
                    mixing_zone_x + mixing_zone_size,
                    mixing_zone_y + mixing_zone_size
                ],
                fill=result_color + (alpha,)
            )

            # Composite overlay onto base image
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')

            # Draw mixing zone border
            draw = ImageDraw.Draw(img)
            border_width = self.config.mixing_zone_border_width
            for j in range(border_width):
                draw.rectangle(
                    [
                        mixing_zone_x - j,
                        mixing_zone_y - j,
                        mixing_zone_x + mixing_zone_size + j,
                        mixing_zone_y + mixing_zone_size + j
                    ],
                    outline=(255, 255, 255),
                    width=1
                )

            frames.append(img)

        # Final frame
        final_frame = self._render_final_state(task_data)
        for _ in range(hold_frames):
            frames.append(final_frame.copy())

        return frames

    def _draw_radial_light(
        self,
        img: Image.Image,
        center: tuple[int, int],
        radius: int,
        color: tuple[int, int, int]
    ) -> Image.Image:
        """
        Draw a radial gradient light source.

        Creates a glowing effect by drawing concentric circles
        with decreasing opacity from center to edge.
        """
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        cx, cy = center

        # Draw concentric circles with decreasing intensity
        steps = 50
        for i in range(steps, 0, -1):
            alpha = int(255 * (i / steps) ** 2)  # Quadratic falloff
            current_radius = int(radius * (i / steps))

            draw.ellipse(
                [
                    cx - current_radius,
                    cy - current_radius,
                    cx + current_radius,
                    cy + current_radius
                ],
                fill=color + (alpha,)
            )

        # Composite onto original image
        img = img.convert('RGBA')
        result = Image.alpha_composite(img, overlay)
        return result.convert('RGB')
