import subprocess
import tempfile
import os
import shutil
import glob
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

# Get Manim executable path from environment variables or assume it's in the system PATH
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")   #MANIM_PATH "/Users/[Your_username]/anaconda3/envs/manim2/Scripts/manim.exe"

TEMP_DIRS = {}
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(BASE_DIR, exist_ok=True)  # Ensure the media folder exists

def generate_manim_code_from_prompt(prompt: str) -> str:
    """Generate Manim code from natural language prompt"""
    base_template = '''from manim import *

class GeneratedScene(Scene):
    def construct(self):
        {}
'''
    
    if "circle" in prompt.lower():
        code = "        circle = Circle()\n        self.play(Create(circle))\n        self.wait()"
    elif "square" in prompt.lower():
        code = "        square = Square()\n        self.play(Create(square))\n        self.wait()"
    elif "text" in prompt.lower():
        code = "        text = Text('Hello World')\n        self.play(Write(text))\n        self.wait()"
    elif "dot" in prompt.lower():
        code = "        dot = Dot()\n        self.play(Create(dot))\n        self.wait()"
    elif "triangle" in prompt.lower():
        code = "        triangle = Triangle()\n        self.play(Create(triangle))\n        self.wait()"
    else:
        code = "        circle = Circle()\n        self.play(Create(circle))\n        self.wait()"
    
    return base_template.format(code)

@mcp.tool()
def create_video_from_prompt(prompt: str) -> str:
    """Create video from natural language prompt"""
    tmpdir = os.path.join(BASE_DIR, "manim_tmp")  
    os.makedirs(tmpdir, exist_ok=True)  # Ensure the temp folder exists
    script_path = os.path.join(tmpdir, "scene.py")
    
    try:
        # Generate Manim code from prompt
        manim_code = generate_manim_code_from_prompt(prompt)
        
        # Write the Manim script to the temp directory
        with open(script_path, "w") as script_file:
            script_file.write(manim_code)
        
        # Execute Manim without preview
        result = subprocess.run(
            [MANIM_EXECUTABLE, "-ql", script_path, "GeneratedScene"],
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        if result.returncode == 0:
            # Find the generated video file
            video_files = glob.glob(os.path.join(tmpdir, "media", "videos", "scene", "480p15", "*.mp4"))
            
            if video_files:
                # Copy only the video file to the media folder
                source_video = video_files[0]
                filename = f"generated_video_{abs(hash(prompt)) % 10000}.mp4"
                destination = os.path.join(BASE_DIR, filename)
                
                shutil.copy2(source_video, destination)
                
                # Clean up temp directory
                try:
                    shutil.rmtree(tmpdir)
                except:
                    pass
                    
                return "video generated"
            else:
                return "error"
        else:
            return "error"

    except Exception as e:
        return "error"

@mcp.tool()
def execute_manim_code(manim_code: str) -> str:
    """Execute the Manim code"""
    tmpdir = os.path.join(BASE_DIR, "manim_tmp")  
    os.makedirs(tmpdir, exist_ok=True)  # Ensure the temp folder exists
    script_path = os.path.join(tmpdir, "scene.py")
    
    try:
        # Write the Manim script to the temp directory
        with open(script_path, "w") as script_file:
            script_file.write(manim_code)
        
        # Execute Manim with the correct path
        result = subprocess.run(
            [MANIM_EXECUTABLE, "-p", script_path],
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        if result.returncode == 0:
            TEMP_DIRS[tmpdir] = True
            print(f"Check the generated video at: {tmpdir}")
            return "Execution successful. Video generated."
        else:
            return f"Execution failed: {result.stderr}"

    except Exception as e:
        return f"Error during execution: {str(e)}"

@mcp.tool()
def cleanup_manim_temp_dir(directory: str) -> str:
    """Clean up the specified Manim temporary directory after execution."""
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            return f"Cleanup successful for directory: {directory}"
        else:
            return f"Directory not found: {directory}"
    except Exception as e:
        return f"Failed to clean up directory: {directory}. Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")