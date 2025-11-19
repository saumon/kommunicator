from mcp.server.fastmcp import FastMCP
from utils import send_email_http, send_teams_message
from logging_config import get_logger

logger = get_logger(__name__)

# Initialize FastMCP server
mcp = FastMCP("mcp-kommunicator")

@mcp.tool()
def get_status():
    return "The mcp-kommunicator is up and running!"

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email to a recipient.

    Args:
        to: Recipient email address or alias
        subject: Email subject
        body: Email body content

    Returns:
        Success or error message
    """
    try:
        logger.info(f"Sending email to {to} with subject: {subject}")
        send_email_http(to, subject, body)
        logger.info(f"Email sent successfully to {to}")
        return f"Email sent successfully to {to}"
    except Exception as e:
        logger.error(f"Error sending email to {to}: {str(e)}", exc_info=True)
        return f"Error sending email: {str(e)}"


@mcp.tool()
def send_teams(to: str, message: str, bot: bool = False) -> str:
    """
    Send a Teams message to a user.

    Args:
        to: Recipient email address or alias
        message: Message content
        bot: Whether the message is from a bot (default: False)

    Returns:
        Success or error message
    """
    try:
        logger.info(f"Sending Teams message to {to} (bot={bot})")
        send_teams_message(to, message, bot)
        logger.info(f"Teams message sent successfully to {to}")
        return f"Teams message sent successfully to {to}"
    except Exception as e:
        logger.error(f"Error sending Teams message to {to}: {str(e)}", exc_info=True)
        return f"Error sending Teams message: {str(e)}"


def main():
    # Initialize and run the server
    logger.info("Starting MCP Kommunicator server")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
