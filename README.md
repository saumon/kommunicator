# Kommunicator

A simple MCP (Model Context Protocol) server built with FastMCP.

## Description

Kommunicator is a demonstration MCP server that exposes a basic status tool. It can serve as a starting point for building more complex MCP servers.

## Features

- 🔧 A `get_status` tool to check server status
- 🚀 Uses FastMCP for simplified setup
- 📡 Communication via stdio

## Prerequisites

- Python >= 3.14
- uv (Python package manager)

## Installation

- Clone the repository:

```bash
git clone <repo-url>
cd kommunicator
```

- Install dependencies with uv:

```bash
uv sync
```

## Usage

### Running the server

```bash
uv run mcp-kommunicator.py
```

The server will start and listen on standard input/output (stdio).

### Development Mode

For development and testing, you can use the MCP Inspector to interact with the server:

```bash
uv run mcp dev mcp-kommunicator.py
```

This will launch the MCP Inspector in your browser, providing a web interface to:

- Test your tools interactively
- Inspect server capabilities
- Debug requests and responses
- View logs in real-time

### Configuration with Claude Desktop

To use this MCP server with Claude Desktop, add the following configuration to your Claude config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "mcp-kommunicator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/kommunicator",
        "run",
        "mcp-kommunicator.py"
      ]
    }
  }
}
```

Replace `/path/to/kommunicator` with the absolute path to the project directory.

## Available Tools

### `get_status`

Returns the current server status.

**Returns:**

- Type: `string`
- Example: `"The kommunicator is up and running!"`

## Development

### Project Structure

```text
kommunicator/
├── mcp-kommunicator.py    # Main MCP server
├── pyproject.toml         # Project configuration
└── README.md              # Documentation
```

### Adding New Tools

To add a new tool, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_new_tool(param1: str) -> str:
    """Tool description"""
    return f"Result: {param1}"
```

## License

To be determined

## Contributing

Contributions are welcome! Feel free to open an issue or pull request.
