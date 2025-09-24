# MCP Server Configuration Instructions

## Option 1: VS Code Extension Settings
1. Open VS Code
2. Go to Settings (Ctrl+,)
3. Search for "MCP" or "Model Context Protocol"
4. Add a new MCP server with these settings:
   - Name: manim-server
   - Command: uv
   - Args: ["run", "python", "falcon.py"]
   - Working Directory: c:\Users\kalak\Downloads\Desktop\nova

## Option 2: Configuration File
Copy the mcp_config.json to your MCP configuration directory:

**Windows (typical locations):**
- %APPDATA%\Code\User\mcp_servers.json
- %USERPROFILE%\.config\mcp\servers.json
- Or wherever your GitHub Copilot extension stores MCP configs

## Option 3: Environment Variable
Set the MCP_CONFIG_FILE environment variable to point to your config:
```
set MCP_CONFIG_FILE=c:\Users\kalak\Downloads\Desktop\nova\mcp_config.json
```

## Starting the Server
1. Run the start_mcp_server.bat file, or
2. Run directly: `uv run python falcon.py`
3. The server will start and listen for connections

## Testing
Once configured, you should be able to use your Manim tools in GitHub Copilot:
- execute_manim_code() - Run Manim animations
- generate_manim_template() - Get code templates