<div align="center">
  <img src="docs/assets/logo.png" alt="Kommunicator Logo" width="200">

# Kommunicator™

  **A lightweight CLI and MCP server for sending emails and Microsoft Teams messages via webhooks.**

  [![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE) [![MCP](https://img.shields.io/badge/MCP-Compatible-8B5CF6?style=flat-square)](https://modelcontextprotocol.io/) [![Microsoft Teams](https://img.shields.io/badge/Microsoft%20Teams-Webhooks-6264A7?style=flat-square&logo=microsoftteams&logoColor=white)](https://www.microsoft.com/en-us/microsoft-teams/) [![FastMCP](https://img.shields.io/badge/Built%20with-FastMCP-FF6B6B?style=flat-square)](https://github.com/jlowin/fastmcp) [![Open Source](https://img.shields.io/badge/Open%20Source-❤️-red?style=flat-square)]() [![Website](https://img.shields.io/badge/Website-Landing%20Page-00D4AA?style=flat-square&logo=github-pages&logoColor=white)](https://saumon.github.io/kommunicator/)

</div>

---

## Table of contents

- [Kommunicator™](#kommunicator)
  - [Table of contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the repository](#clone-the-repository)
    - [Install as a global CLI tool](#install-as-a-global-cli-tool)
    - [Update the tool](#update-the-tool)
    - [Uninstall the tool](#uninstall-the-tool)
    - [Alternative: Development only (without global installation)](#alternative-development-only-without-global-installation)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
    - [Human Aliases Configuration](#human-aliases-configuration)
    - [Conversations and Channels Configuration](#conversations-and-channels-configuration)
  - [Usage](#usage)
    - [Command-Line Interface (CLI)](#command-line-interface-cli)
      - [Mass Sending](#mass-sending)
        - [Mass Sending with send-email](#mass-sending-with-send-email)
        - [Mass Sending with send-teams](#mass-sending-with-send-teams)
    - [Running the MCP Server](#running-the-mcp-server)
    - [Development Mode](#development-mode)
    - [Configuration with Claude Desktop](#configuration-with-claude-desktop)
  - [Available Tools](#available-tools)
    - [`get_status`](#get_status)
    - [`send_email`](#send_email)
    - [`send_teams`](#send_teams)
  - [Development](#development)
    - [Project Structure](#project-structure)
    - [Logging](#logging)
    - [Adding New Tools](#adding-new-tools)
    - [Testing Alias Resolution](#testing-alias-resolution)
  - [License](#license)
  - [Contributing](#contributing)

## Description

Kommunicator™ is both:

- a **command-line interface (CLI)** for sending emails and Teams messages from your terminal, and
- an **MCP server** exposing the same capabilities to MCP-compatible clients.

The MCP server is implemented in **Python** and built on top of the **FastMCP** framework.

Kommunicator™ is designed for employees in Office 365-enabled organizations and is intended to be used with an automation flow in **Microsoft Power Automate**. It allows employees to send emails and messages without needing special privileges (no admin rights required). The main prerequisite is access to Power Automate, which is typically available in Office 365 enterprise environments.

It sends emails and Teams messages via Microsoft Teams webhooks, supports human-friendly aliases, and can target users, conversations, and channels.

## Features

- 🔧 A `get_status` tool to check server status
- 📧 A `send_email` tool to send emails via Teams webhook (supports email addresses and aliases)
- 💬 A `send_teams` tool to send Teams messages to users, conversations, and channels (supports aliases and auto-detection)
- 👥 Human-friendly email aliases system with automatic resolution
- 🗣️ Conversation and channel name mapping for easy group messaging
- 🎯 Automatic target detection (user/conversation/channel) based on recipient
- 💻 Command-line interface for standalone email and Teams message sending
- 🚀 Uses FastMCP for simplified setup
- 📡 Communication via stdio
- 📝 Comprehensive logging to file

## Prerequisites

- Python >= 3.14
- uv (Python package manager)

## Installation

### Clone the repository

```bash
git clone <repo-url>
cd kommunicator
```

### Install as a global CLI tool

Install the CLI as a global command available from anywhere:

```bash
uv tool install -e .
```

The `-e` (editable) flag allows code changes to be reflected immediately without reinstallation.

**Note:** Make sure `~/.local/bin` is in your PATH. Add this to your shell profile (`~/.zshrc`, `~/.bashrc`) if needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

After installation, verify it works:

```bash
kommunicator-cli --help
```

### Update the tool

To update after pulling new changes:

```bash
cd /path/to/kommunicator
git pull
uv tool install -e . --force
```

The `--force` flag reinstalls even if already installed.

### Uninstall the tool

```bash
uv tool uninstall kommunicator
```

### Alternative: Development only (without global installation)

If you only want to run the CLI from the project directory:

```bash
uv sync
uv run kommunicator_cli.py --help
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

The `conf/humans.conf` file allows you to map human-friendly aliases to email addresses, making it easier to send messages to users without remembering full email addresses.

**Configuration file format:**

```ini
# conf/humans.conf
# Format: email = alias1, alias2, alias3

# Explicit aliases
john.doe@example.com = john, john doe, jd
alice.wonder@example.com = alice, alice wonder, aw
bob.wilson@example.com = bob, bobby

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
- **Auto-generated aliases**: Aliases are **always** automatically generated from email parts, even when explicit aliases are provided:
  - `toto.smith@example.com =` can be found by: "toto", "smith", or "toto smith"
  - `momo.salam-ext@example.com =` can be found by: "momo", "salam", or "momo salam"
  - `bill.gates@example.com = boss` can be found by: "bill", "gates", "bill gates", **or** "boss"
  - Common suffixes like `-ext`, `-int`, `-temp` are automatically filtered out
- **Duplicate detection**: When multiple emails share a common part, that part is skipped to avoid ambiguity:
  - With `roger.moore@example.com =` and `roger.rabbit@example.com =`:
    - "roger" is ambiguous → will fail (not unique)
    - "moore" → finds `roger.moore@example.com` ✓
    - "roger moore" → finds `roger.moore@example.com` ✓

### Conversations and Channels Configuration

The `conf/conversations.conf` file allows you to map friendly names to Teams conversation and channel IDs, making it easier to send messages to groups without remembering long IDs.

**Configuration file format:**

```ini
# conf/conversations.conf
# Format for conversations: NAME=CONVERSATION_ID
# Format for channels: NAME=CONVERSATION_ID|TEAM_ID

# Conversations/Groups
Equipe_Dev=19:meeting_abc123def456@thread.skype
Support_Client=19:meeting_def456ghi789@thread.skype

# Channels (require teamId)
Canal_General=19:meeting_abc123@thread.skype|19:team_def456ghi789@thread.tacv2
Canal_Dev=19:meeting_def456@thread.skype|19:team_abc123def456@thread.tacv2
```

**Setup:**

1. Copy the example configuration:

   ```bash
   cp conf/conversations.conf.example conf/conversations.conf
   ```

2. Edit `conf/conversations.conf` and add your conversation/channel mappings

**Features:**

- **Conversations/Groups**: Simple format with just the conversation ID
- **Team Channels**: Format with conversation ID and team ID separated by `|`
- **Case-insensitive**: Names like "Equipe_Dev", "equipe_dev" all work
- **Automatic detection**: The system automatically detects if the target is a conversation or a channel based on the configuration
- **Flexible naming**: Use underscores or spaces in names (spaces are converted to underscores internally)
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

# Combined: explicit + auto-generated aliases
email = get_email_by_alias("bill")  # Returns "bill.gates@example.com" (auto-generated)
email = get_email_by_alias("gates")  # Returns "bill.gates@example.com" (auto-generated)
email = get_email_by_alias("boss")  # Returns "bill.gates@example.com" (explicit)

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
kommunicator-cli send-email --to user@example.com --subject "Meeting" --body "Meeting at 2pm"
```

**Available commands:**

- `send-email`: Send an email via Teams webhook
- `send-teams`: Send a Teams message to a user
- `get-email`: Look up email address by alias

**Global options:**

- `-v`, `--verbose`: Enable verbose output
- `-h`, `--help`: Show help message

**Send-email command options:**

- `--to` (required): Recipient - can be:
  - Email address (`user@example.com`)
  - User alias from `humans.conf` (`john`, `john doe`)
  - **Path to a recipients file** for mass sending (see Mass Sending section below)
- `--subject` (required): Email subject
- `--body` (optional): Email body content. If not provided, reads from stdin

**Send-teams command options:**

- `--to` (required): Recipient - can be:
  - Email address (`user@example.com`)
  - User alias from `humans.conf` (`john`, `john doe`)
  - Conversation name from `conversations.conf` (`Equipe_Dev`, `Support_Client`)
  - Channel name from `conversations.conf` (`Canal_General`)
  - **Path to a recipients file** for mass sending (see Mass Sending section below)
- `--message` (optional): Message content. If not provided, reads from stdin
- `--format` (optional): Message format - `auto` (auto-detect, default), `message` for plain text, or `adaptivecard` for Adaptive Card
- `--bot` (optional): Mark the message as coming from a bot (automatic/system message)

**Note on format auto-detection:** When `--format` is set to `auto` (default), the command automatically detects Adaptive Cards by checking if the message is valid JSON containing `"type": "AdaptiveCard"`. This means you can send Adaptive Cards without explicitly specifying `--format adaptivecard`.

**Note on recipient resolution:** The `--to` parameter automatically detects the target type:

1. First checks if it matches a conversation/channel name in `conversations.conf`
2. If not found, checks if it's an email address or user alias in `humans.conf`
3. Automatically selects the appropriate Teams target (`teams-message`, `teams-conversation`, or `teams-canal`)

**Get-email command options:**

- `--alias` (required): Alias to look up (case-insensitive, can be multi-word)

**Examples:**

```bash
# Simple email with email address
kommunicator-cli send-email --to user@example.com --subject "Hello" --body "Hello World!"

# Send email using an alias (no need for get-email!)
kommunicator-cli send-email --to john --subject "Hello" --body "Hello John!"

# Send email using multi-word alias
kommunicator-cli send-email --to "john doe" --subject "Meeting" --body "See you at 2pm"

# Email with message from stdin
echo "Meeting at 2pm" | kommunicator-cli send-email --to user@example.com --subject "Reminder"

# Email with message from file
cat report.txt | kommunicator-cli send-email --to user@example.com --subject "Daily Report"

# Send a Teams message with email address
kommunicator-cli send-teams --to user@example.com --message "Hello World"

# Send Teams message using an alias
kommunicator-cli send-teams --to john --message "Meeting at 2pm"

# Send Teams message using multi-word alias
kommunicator-cli send-teams --to "john doe" --message "Quick reminder"

# Send Teams message to a conversation/group
kommunicator-cli send-teams --to "Equipe_Dev" --message "Team meeting at 3pm"

# Send Teams message to a channel
kommunicator-cli send-teams --to "Canal_General" --message "Important announcement"

# Send Adaptive Card to a channel
cat messages/adaptivecard.json.sample | kommunicator-cli send-teams --to "Canal_Dev"

# Send Teams message from stdin
echo "Hello World" | kommunicator-cli send-teams --to john

# Send Teams message from file
cat message.txt | kommunicator-cli send-teams --to user@example.com

# Send bot message (automatic/system message)
kommunicator-cli send-teams --to john --message "Automatic reminder" --bot

# Send Adaptive Card (auto-detected from JSON content)
cat messages/adaptivecard.json.sample | kommunicator-cli send-teams --to john

# Send Adaptive Card with explicit format
cat messages/adaptivecard.json.sample | kommunicator-cli send-teams --to john --format adaptivecard

# Send Adaptive Card with bot mode
cat messages/adaptivecard.json.sample | kommunicator-cli send-teams --to user@example.com --bot

# Send plain text message from file
cat messages/message.txt.sample | kommunicator-cli send-teams --to john

# Send multi-line message using heredoc
kommunicator-cli send-teams --to john <<EOF
Hello John,

This is a multi-line message.
It supports multiple paragraphs.

Best regards
EOF

# Send multi-line email using heredoc
kommunicator-cli send-email --to john --subject "Multi-line message" <<EOF
Hello John,

This is a multi-line email body.
You can write as many lines as you need.

Best regards,
Your Team
EOF

# Create and send an Adaptive Card using heredoc
kommunicator-cli send-teams --to "Canal_General" <<'EOF'
{
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "Important Announcement",
      "weight": "Bolder",
      "size": "Large"
    },
    {
      "type": "TextBlock",
      "text": "This is an announcement sent via heredoc",
      "wrap": true
    },
    {
      "type": "FactSet",
      "facts": [
        {
          "title": "Date:",
          "value": "December 1, 2025"
        },
        {
          "title": "Status:",
          "value": "Active"
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "Learn More",
      "url": "https://example.com"
    }
  ]
}
EOF

# Send bot message using heredoc
kommunicator-cli send-teams --to john --bot <<EOF
🤖 Automatic System Notification

Your daily report is ready.
Please review it at your earliest convenience.
EOF

# Look up email by alias
kommunicator-cli get-email --alias "john"

# Look up email by multi-word alias
kommunicator-cli get-email --alias "john smith"

# Look up email by auto-generated alias
kommunicator-cli get-email --alias "moore"

# Combine get-email with send-email command (optional, can use alias directly)
email=1000 27 100 1000 1001kommunicator-cli get-email --alias "john")
kommunicator-cli send-email --to "$email" --subject "Hello" --body "Message"

# Verbose mode
kommunicator-cli -v send-email --to john --subject "Test" --body "Test"
kommunicator-cli -v send-teams --to john --message "Test message"
kommunicator-cli -v get-email --alias "john"

# Using with uv
kommunicator-cli send-email --to john --subject "Hello" --body "Test"
kommunicator-cli send-teams --to john --message "Hello from uv"
kommunicator-cli get-email --alias "john"

# Show help for commands
kommunicator-cli send-email --help
kommunicator-cli send-teams --help
kommunicator-cli get-email --help
```

#### Mass Sending

Both `send-email` and `send-teams` commands support sending messages to multiple recipients in a single operation. When the `--to` parameter points to an existing file, the command enters **mass sending mode**.

**Recipient file format:**

- One recipient per line
  - For `send-email`: email addresses or user aliases
  - For `send-teams`: email addresses, user aliases, conversation names, or channel names
- Lines starting with `#` are treated as comments and ignored
- Empty lines are ignored

**Example recipient file** (`conf/mass-target.conf`):

```text
# Users (emails and aliases)
john.doe@example.com
alice
bobby

# For send-teams: also supports conversations and channels
Equipe_Dev
Canal_General

# This is a comment - will be skipped
# jane@example.com
```

##### Mass Sending with send-email

**Examples:**

```bash
# Send email to multiple recipients from a file
kommunicator-cli send-email --to conf/mass-target.conf --subject "Notice" --body "Important update"

# Mass sending with body from stdin
cat message.txt | kommunicator-cli send-email --to recipients.conf --subject "Report"

# Mass sending with verbose output
kommunicator-cli -v send-email --to recipients.conf --subject "Alert" --body "Urgent message"

# Using with uv
kommunicator-cli send-email --to conf/mass-target.conf --subject "Announcement" --body "News"
```

**Behavior:**

- Reads all recipients from the file
- Sends the email to each recipient individually (same subject and body for all)
- Continues sending even if some recipients fail
- Provides a summary with success and failure counts at the end
- Returns exit code 0 if all succeeded, or 1 if any failed
- Each recipient is resolved independently (supports email addresses and aliases)

**Example output:**

```text
  → Sending to: john.doe@example.com
  ✓ Sent successfully to john.doe@example.com
  → Sending to: alice
  ✓ Sent successfully to alice
  → Sending to: bob
  ✗ Failed to send to bob: Alias 'bob' not found

📊 Summary: 2/3 emails sent successfully
❌ Failed recipients (1):
  - bob: Alias 'bob' not found
```

##### Mass Sending with send-teams

**Examples:**

```bash
# Send a message to multiple recipients from a file
kommunicator-cli send-teams --to conf/mass-target.conf --message "Hello everyone"

# Send an Adaptive Card to multiple recipients
cat messages/adaptivecard.json.sample | kommunicator-cli send-teams --to recipients.conf

# Send a bot message to multiple recipients
kommunicator-cli send-teams --to recipients.conf --message "System notification" --bot

# Mass sending with verbose output
kommunicator-cli -v send-teams --to recipients.conf --message "Alert"

# Using with uv
kommunicator-cli send-teams --to conf/mass-target.conf --message "Announcement"
```

**Behavior:**

- Reads all recipients from the file
- Sends the message to each recipient individually
- Continues sending even if some recipients fail
- Provides a summary with success and failure counts at the end
- Returns exit code 0 if all succeeded, or 1 if any failed
- Each recipient is resolved independently (users, conversations, channels)

**Example output:**

```text
Successfully sent to: john.doe@example.com
Successfully sent to: alice (alice.wonder@example.com)
Successfully sent to: Equipe_Dev (conversation)
Error sending to bob: Alias 'bob' not found
Successfully sent to: Canal_General (channel)

Mass sending complete: 4 succeeded, 1 failed
  → Sending to: john.doe@example.com
  ✓ Sent successfully to john.doe@example.com
  → Sending to: Equipe_Dev
  ✓ Sent successfully to Equipe_Dev
  → Sending to: bob
  ✗ Failed to send to bob: Alias 'bob' not found

📊 Summary: 2/3 messages sent successfully
❌ Failed recipients (1):
  - bob: Alias 'bob' not found
```

**Note:** An example configuration file is provided at `conf/mass-target.conf.example`. Copy it to create your own recipient list.

**Note:** The CLI requires the same `TEAMS_WEBHOOK_KOMMUNICATOR` environment variable as the MCP server. The `get-email` command uses the `conf/humans.conf` configuration file.

### Running the MCP Server

```bash
uv run kommunicator_mcp.py
```

The server will start and listen on standard input/output (stdio).

### Development Mode

For development and testing, you can use the MCP Inspector to interact with the server:

```bash
uv run mcp dev kommunicator_mcp.py
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
        "kommunicator_mcp.py"
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

- `to` (string, required): Recipient email address or alias
- `subject` (string, required): Email subject
- `body` (string, required): Email body content (supports `\n` for line breaks, automatically converted to `<br>`)

**Returns:**

- Type: `string`
- Success: `"Email sent successfully to {email}"`
- Error: `"Error sending email: {error_message}"`

**Examples:**

```python
# Send email using email address
send_email(
    to="user@example.com",
    subject="Meeting Reminder",
    body="Don't forget our meeting at 2 PM today.\nSee you there!"
)

# Send email using alias
send_email(
    to="john",
    subject="Hello John",
    body="Quick update for you."
)

# Send email using multi-word alias
send_email(
    to="john doe",
    subject="Meeting",
    body="See you at 2pm"
)
```

**Note:** Requires `TEAMS_WEBHOOK_KOMMUNICATOR` environment variable to be set.

### `send_teams`

Send a Teams message to a user, conversation, or channel.

**Parameters:**

- `to` (string, required): Recipient - can be:
  - Email address (`user@example.com`)
  - User alias from `humans.conf` (`john`, `john doe`)
  - Conversation name from `conversations.conf` (`Equipe_Dev`, `Support_Client`)
  - Channel name from `conversations.conf` (`Canal_General`)
- `message` (string, required): Message content (plain text or Adaptive Card JSON)
- `bot` (boolean, optional): Whether the message is from a bot (default: False)
- `format` (string, optional): Message format - `auto` (auto-detect, default), `message` for plain text, or `adaptivecard` for Adaptive Card

**Returns:**

- Type: `string`
- Success: `"Teams message sent successfully to {target}"`
- Error: `"Error sending Teams message: {error_message}"`

**Format auto-detection:** When `format` is `auto` (default), the tool automatically detects Adaptive Cards by checking if the message is valid JSON containing `"type": "AdaptiveCard"`.

**Target auto-detection:** The tool automatically detects the target type:

1. First checks if it matches a conversation/channel name in `conversations.conf`
2. If not found, checks if it's an email address or user alias in `humans.conf`
3. Automatically selects the appropriate Teams target (`teams-message`, `teams-conversation`, or `teams-canal`)

**Examples:**

```python
# Send Teams message using email address
send_teams(
    to="user@example.com",
    message="Don't forget our meeting at 2 PM today.\nSee you there!"
)

# Send Teams message using alias
send_teams(
    to="john",
    message="Quick reminder for you."
)

# Send Teams message using multi-word alias
send_teams(
    to="john doe",
    message="Meeting at 2pm"
)

# Send bot message (automatic/system message)
send_teams(
    to="john",
    message="Automatic system alert",
    bot=True
)

# Send Adaptive Card (auto-detected from JSON content)
adaptive_card_json = '''
{
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "Hello from Adaptive Card!",
      "weight": "Bolder",
      "size": "Large"
    }
  ]
}
'''
send_teams(
    to="john",
    message=adaptive_card_json
)

# Send Adaptive Card with explicit format
send_teams(
    to="john",
    message=adaptive_card_json,
    format="adaptivecard"
)

# Send message to a conversation/group
send_teams(
    to="Equipe_Dev",
    message="Team meeting at 3pm"
)

# Send message to a channel
send_teams(
    to="Canal_General",
    message="Important announcement"
)

# Send Adaptive Card to a channel
send_teams(
    to="Canal_Dev",
    message=adaptive_card_json
)
```

**Note:** Requires `TEAMS_WEBHOOK_KOMMUNICATOR` environment variable to be set.

## Development

### Project Structure

```text
kommunicator/
├── kommunicator_mcp.py    # Main MCP server
├── kommunicator_cli.py    # Command-line interface
├── utils.py               # Email sending and alias utilities
├── logging_config.py      # Logging configuration
├── conf/
│   ├── humans.conf                      # Email-to-alias mappings (user-configured)
│   ├── humans.conf.example              # Example configuration file
│   ├── conversations.conf               # Conversation/channel mappings (user-configured)
│   ├── conversations.conf.example       # Example configuration file
│   └── mass-target.conf.example         # Example mass sending recipient list
├── messages/              # Sample message templates
│   ├── message.txt.sample           # Plain text message example
│   └── adaptivecard.json.sample     # Adaptive Card JSON example
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

Copyright (c) 2025 saumon

This project is licensed under the MIT License. See the [LICENCE](LICENCE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or pull request.
