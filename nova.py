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
BASE_DIR = Path(__file__).resolve().parent / "media"
BASE_DIR.mkdir(parents=True, exist_ok=True)

TEMP_DIRS = {}

@server.tool()
def render_scene(code: str) -> str:
    """
    Render a Manim scene from code and display in Claude.
    """
    # Use fixed temp directory like the reference
    tmpdir = BASE_DIR / "manim_tmp"
    tmpdir.mkdir(exist_ok=True)
    script_file = tmpdir / "scene.py"

    try:
        # Write Manim script
        script_file.write_text(code)

        # Run manim with -p flag (preview) like the working reference
        result = subprocess.run(
            [MANIM_PATH, "-p", str(script_file)],
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        if result.returncode == 0:
            TEMP_DIRS[str(tmpdir)] = True
            return f"✅ Execution successful. Video generated.\n📁 Check the generated video at: {tmpdir}"
        else:
            return f"❌ Execution failed: {result.stderr}"

    except Exception as e:
        return f"⚠️ Error during execution: {str(e)}"


@server.tool()
def cleanup(directory: str) -> str:
    """Clean up the specified Manim temporary directory after execution."""
    try:
        if Path(directory).exists():
            shutil.rmtree(directory)
            return f"🗑️ Cleanup successful for directory: {directory}"
        else:
            return f"⚠️ Directory not found: {directory}"
    except Exception as e:
        return f"⚠️ Failed to clean up directory: {directory}. Error: {str(e)}"


if __name__ == "__main__":
    server.run("stdio") 