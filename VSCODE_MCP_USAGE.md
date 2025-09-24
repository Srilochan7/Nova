# How to Add MCP Server to Global VS Code Settings

## Step 1: Open User Settings
- Press `Ctrl + Shift + P`
- Type "Preferences: Open User Settings (JSON)"
- Press Enter

## Step 2: Add MCP Configuration
Add this configuration to your user settings.json:

```json
{
    "github.copilot.chat.experimental.mcp.servers": {
        "manim-server": {
            "command": "uv",
            "args": ["run", "python", "falcon.py"],
            "cwd": "c:\\Users\\kalak\\Downloads\\Desktop\\nova"
        }
    }
}
```

## What This Does:
- Tells GitHub Copilot about your MCP server
- When you ask Copilot to create animations, it will automatically use your tools
- The server starts automatically when needed

## Your Available Tools:
1. `execute_manim_code()` - Runs Manim code and returns video
2. `generate_manim_template()` - Provides code templates

## Testing:
Ask Copilot things like:
- "Create a simple math animation with Manim"
- "Generate a basic Manim template"
- "Make an animation showing E=mc²"