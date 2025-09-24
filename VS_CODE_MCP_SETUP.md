# How to Add Your MCP Server to VS Code

## Quick Setup Steps:

### 1. Open VS Code Settings
- Press `Ctrl + ,` to open settings
- OR go to File → Preferences → Settings

### 2. Open Settings JSON
- Click the "Open Settings (JSON)" button (looks like a document icon in the top right)
- OR press `Ctrl + Shift + P` and search for "Preferences: Open User Settings (JSON)"

### 3. Add Your MCP Server Configuration
Add this to your settings.json file:

```json
{
    "mcp.servers": {
        "manim-server": {
            "command": "uv",
            "args": ["run", "python", "falcon.py"],
            "cwd": "c:\\Users\\kalak\\Downloads\\Desktop\\nova"
        }
    }
}
```

### 4. Alternative: Workspace Settings
If you want the MCP server only for this project:
- I've already created `.vscode/settings.json` in your project
- This will only work when you have this specific folder open in VS Code

### 5. Restart VS Code
- Close and reopen VS Code for the changes to take effect
- OR press `Ctrl + Shift + P` and run "Developer: Reload Window"

## Verification Steps:

1. Open GitHub Copilot Chat
2. Try asking: "Can you run a manim animation?"
3. Copilot should be able to use your `execute_manim_code` and `generate_manim_template` tools

## Troubleshooting:

If it doesn't work:
1. Check that your MCP server starts correctly: `uv run python falcon.py`
2. Make sure the file paths in the configuration are correct
3. Check VS Code's output panel for any MCP-related errors
4. Ensure you have the latest version of GitHub Copilot extension