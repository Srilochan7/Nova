import os
import subprocess
import base64
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("manim-server")

# Config
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")
BASE_MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(BASE_MEDIA_DIR, exist_ok=True)


@mcp.tool()
def execute_manim_code(manim_code: str, quality: str = "medium") -> str:
    """
    Execute user-provided Manim code and return Base64 video.
    """
    temp_dir = os.path.join(BASE_MEDIA_DIR, "temp_manim")
    os.makedirs(temp_dir, exist_ok=True)
    script_file = os.path.join(temp_dir, "animation.py")

    try:
        # Write script
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(manim_code)

        # Quality flags
        quality_flags = {"low": "-ql", "medium": "-qm", "high": "-qh"}
        quality_flag = quality_flags.get(quality, "-qm")

        cmd = [MANIM_EXECUTABLE, quality_flag, script_file]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_dir)

        if result.returncode != 0:
            return f"❌ Manim failed:\n{result.stderr}"

        # Find video
        media_path = Path(temp_dir) / "media" / "videos"
        video_files = list(media_path.rglob("*.mp4"))
        if not video_files:
            return "✅ Manim ran, but no video file found."

        video_path = video_files[0]
        with open(video_path, "rb") as f:
            video_data = f.read()
        video_base64 = base64.b64encode(video_data).decode("utf-8")

        return f"✅ Animation generated!\n\n📹 data:video/mp4;base64,{video_base64}"

    except Exception as e:
        return f"❌ Error: {e}"


@mcp.tool()
def generate_manim_template(animation_type: str = "basic") -> str:
    """
    Generate example Manim templates (basic, math, geometry, graph).
    """
    templates = {
        "basic": '''from manim import *

class BasicAnimation(Scene):
    def construct(self):
        text = Text("Hello Manim!", font_size=48)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
''',
        "math": '''from manim import *

class MathAnimation(Scene):
    def construct(self):
        equation = MathTex(r"E = mc^2", font_size=72)
        self.play(Write(equation))
        self.wait(1)
        self.play(equation.animate.scale(1.5).set_color(YELLOW))
        self.wait(2)
''',
    }
    template = templates.get(animation_type, templates["basic"])
    return f"📝 {animation_type} template:\n```python\n{template}\n```"


if __name__ == "__main__":
    mcp.run()  # Keeps server alive