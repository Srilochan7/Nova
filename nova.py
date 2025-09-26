import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
server = FastMCP("nova")

# Get Manim binary from env or fallback to "manim"
MANIM_PATH = os.getenv("MANIM_EXECUTABLE", "manim")

# Base output dir (persistent, not temp)
OUTPUT_DIR = Path(__file__).resolve().parent / "media"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@server.tool()
def render_scene(code: str) -> str:
    """
    Render a Manim scene from a code string.
    Returns the path to the generated video.
    """
    temp_dir = tempfile.mkdtemp(dir=OUTPUT_DIR)
    script_file = Path(temp_dir) / "scene.py"

    try:
        # Write user-provided Manim script
        script_file.write_text(code)

        # Run manim as subprocess
        result = subprocess.run(
            [MANIM_PATH, "-pql", str(script_file)],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"❌ Render failed:\n{result.stderr}"

        # Find generated media dir
        videos_dir = Path(temp_dir) / "media" / "videos"
        if videos_dir.exists():
            return f"✅ Render complete! Check {videos_dir}"
        else:
            return "⚠️ Render completed but no video found."

    except Exception as e:
        return f"⚠️ Error: {e}"


@server.tool()
def cleanup(path: str) -> str:
    """
    Delete a temporary render directory.
    """
    try:
        shutil.rmtree(path)
        return f"🗑️ Cleaned: {path}"
    except Exception as e:
        return f"⚠️ Failed cleanup: {e}"


if __name__ == "__main__":
    # Run server via stdio (Claude/other MCP clients expect this)
    server.run("stdio")