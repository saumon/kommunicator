# Kommunicator

A simple MCP (Model Context Protocol) server built with FastMCP.

## Description

Kommunicator is an MCP server that provides email sending capabilities through Microsoft Teams webhooks. It exposes tools for checking server status and sending emails to recipients, and includes a command-line interface for standalone email sending.

## Features

- 🔧 A `get_status` tool to check server status
- 📧 A `send_email` tool to send emails via Teams webhook
- 👥 Human-friendly email aliases system
- 💻 Command-line interface for standalone email sending
- 🚀 Uses FastMCP for simplified setup
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

- `TEAMS_WEBHOOK_KOMMUNICATOR`: The Microsoft Teams webhook URL for sending emails

**Setting the environment variable:**

```bash
export TEAMS_WEBHOOK_KOMMUNICATOR='https://your-teams-webhook-url'
```

**For persistent configuration**, you can create a `.env` file or add it to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.).

### Human Aliases Configuration

The `conf/humans.conf` file allows you to map human-friendly aliases to email addresses, making it easier to send emails without remembering full email addresses.

**Configuration file format:**

```ini
# conf/humans.conf
# Format: email = alias1, alias2, alias3

# Explicit aliases
john.doe@example.com = john, john doe, jd
alice.smith@example.com = alice, alice smith
bob@example.com = bob, bobby

# Auto-generated aliases (no explicit aliases needed)
toto.smith@example.com = 
momo.salam-ext@example.com = 
```

**Setup:**

1. Copy the example configuration:

   ```bash
   cp conf/humans.conf.example conf/humans.conf
   ```

2. Edit `conf/humans.conf` and add your email-to-alias mappings

**Features:**

- **Case-insensitive**: Aliases like "John", "john", and "JOHN" all work
- **Multi-word aliases**: Support for aliases like "john doe"
- **Multiple aliases**: One email can have several aliases
- **Auto-generated aliases**: For emails without explicit aliases, the system automatically generates aliases from the email parts:
  - `toto.smith@example.com =` can be found by: "toto", "smith", or "toto smith"
  - `momo.salam-ext@example.com =` can be found by: "momo", "salam", or "momo salam"
  - Common suffixes like `-ext`, `-int`, `-temp` are automatically filtered out
- **Duplicate detection**: When multiple emails share a common part, that part is skipped to avoid ambiguity:
  - With `roger.moore@example.com =` and `roger.rabbit@example.com =`:
    - "roger" is ambiguous → will fail (not unique)
    - "moore" → finds `roger.moore@example.com` ✓
    - "roger moore" → finds `roger.moore@example.com` ✓
    - "rabbit" → finds `roger.rabbit@example.com` ✓
    - "roger rabbit" → finds `roger.rabbit@example.com` ✓

**Using aliases programmatically:**

```python
from utils import get_email_by_alias

# Look up email by explicit alias
email = get_email_by_alias("john")  # Returns "john.doe@example.com"
email = get_email_by_alias("John Doe")  # Case-insensitive, returns same email

# Look up email by auto-generated alias
email = get_email_by_alias("toto")  # Returns "toto.smith@example.com"
email = get_email_by_alias("smith")  # Returns "toto.smith@example.com"
email = get_email_by_alias("toto smith")  # Returns "toto.smith@example.com"

# Duplicate handling
email = get_email_by_alias("moore")  # Returns "roger.moore@example.com"
email = get_email_by_alias("roger")  # Raises ValueError - ambiguous!
```

**Note:** The configuration is cached on first load for performance.

## Usage

### Command-Line Interface (CLI)

The CLI allows you to send emails directly from the command line without running the MCP server.

**Basic usage:**

```bash
./kommunicator-cli.py email --to user@example.com --subject "Meeting" --body "Meeting at 2pm"
```

**Available commands:**

- `email`: Send an email via Teams webhook

**Global options:**

- `-v`, `--verbose`: Enable verbose output
- `-h`, `--help`: Show help message

**Email command options:**

- `--to` (required): Recipient email address
- `--subject` (required): Email subject
- `--body` (optional): Email body content. If not provided, reads from stdin

**Examples:**

```bash
# Simple email
./kommunicator-cli.py email --to user@example.com --subject "Hello" --body "Hello World!"

# Email with message from stdin
echo "Meeting at 2pm" | ./kommunicator-cli.py email --to user@example.com --subject "Reminder"

# Email with message from file
cat report.txt | ./kommunicator-cli.py email --to user@example.com --subject "Daily Report"

# Verbose mode
./kommunicator-cli.py -v email --to user@example.com --subject "Test" --body "Test"

# Using with uv
uv run kommunicator-cli.py email --to user@example.com --subject "Hello" --body "Test"

# Show help for email command
./kommunicator-cli.py email --help
```

**Note:** The CLI requires the same `TEAMS_WEBHOOK_KOMMUNICATOR` environment variable as the MCP server.

### Running the MCP Server

```bash
uv run kommunicator-mcp.py
```

The server will start and listen on standard input/output (stdio).

### Development Mode

For development and testing, you can use the MCP Inspector to interact with the server:

```bash
uv run mcp dev kommunicator-mcp.py
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
        "kommunicator-mcp.py"
      ],
      "env": {
        "TEAMS_WEBHOOK_KOMMUNICATOR": "https://your-teams-webhook-url"
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

**Note:** Requires `TEAMS_WEBHOOK_KOMMUNICATOR` environment variable to be set.

## Development

### Project Structure

```text
kommunicator/
├── kommunicator-mcp.py    # Main MCP server
├── kommunicator-cli.py    # Command-line interface
├── utils.py               # Email sending and alias utilities
├── logging_config.py      # Logging configuration
├── conf/
│   ├── humans.conf        # Email-to-alias mappings (user-configured)
│   └── humans.conf.example # Example configuration file
├── tests/
│   └── test_humans.py     # Test script for alias resolution
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

### Testing Alias Resolution

To test the human alias resolution system:

```bash
# Make sure conf/humans.conf exists with some test data
cp conf/humans.conf.example conf/humans.conf

# Run the test script
./tests/test_humans.py

# Or with uv
uv run tests/test_humans.py
```

The test script will validate that aliases are correctly resolved to email addresses.

## License

To be determined

## Contributing

Contributions are welcome! Feel free to open an issue or pull request.
