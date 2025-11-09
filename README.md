# Kommunicator

A simple MCP (Model Context Protocol) server built with FastMCP.

## Description

Kommunicator is an MCP server that provides email sending capabilities through Microsoft Teams webhooks. It exposes tools for checking server status and sending emails to recipients.

## Features

- 🔧 A `get_status` tool to check server status
- � A `send_email` tool to send emails via Teams webhook
- �🚀 Uses FastMCP for simplified setup
- 📡 Communication via stdio
- 📝 Comprehensive logging to file

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

## Configuration

### Environment Variables

The server requires the following environment variable to be set:

- `TEAMS_WEBHOOK_URL_SEND_EMAIL_TO_USER`: The Microsoft Teams webhook URL for sending emails

**Setting the environment variable:**

```bash
export TEAMS_WEBHOOK_URL_SEND_EMAIL_TO_USER='https://your-teams-webhook-url'
```

**For persistent configuration**, you can create a `.env` file or add it to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.).

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
      ],
      "env": {
        "TEAMS_WEBHOOK_URL_SEND_EMAIL_TO_USER": "https://your-teams-webhook-url"
      }
    }
  }
}
```

Replace `/path/to/kommunicator` with the absolute path to the project directory and set your Teams webhook URL.

## Available Tools

### `get_status`

Returns the current server status.

**Returns:**

- Type: `string`
- Example: `"The kommunicator is up and running!"`

### `send_email`

Send an email to a recipient via Teams webhook.

**Parameters:**

- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject
- `body` (string, required): Email body content (supports `\n` for line breaks, automatically converted to `<br>`)

**Returns:**

- Type: `string`
- Success: `"Email sent successfully to {email}"`
- Error: `"Error sending email: {error_message}"`

**Example:**

```python
send_email(
    to="user@example.com",
    subject="Meeting Reminder",
    body="Don't forget our meeting at 2 PM today.\nSee you there!"
)
```

**Note:** Requires `TEAMS_WEBHOOK_URL_SEND_EMAIL_TO_USER` environment variable to be set.

## Development

### Project Structure

```text
kommunicator/
├── mcp-kommunicator.py    # Main MCP server
├── utils.py               # Email sending utilities
├── logging_config.py      # Logging configuration
├── pyproject.toml         # Project configuration
├── kommunicator.log       # Log file (generated at runtime)
└── README.md              # Documentation
```

### Logging

The server logs all operations to `kommunicator.log` in the project directory. This includes:

- Server startup/shutdown events
- Email sending attempts and results
- Error details with stack traces
- General operational information

The log file is automatically created on first run and uses the format:

```text
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
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
