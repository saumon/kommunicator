#!/usr/bin/env python3
"""
Kommunicator CLI - Command line interface for interacting with Kommunicator services.
"""

import sys
import argparse
from utils import send_email_http, get_email_by_alias, send_teams_message
from logging_config import get_logger

logger = get_logger(__name__)


def cmd_email(args):
    """Handle the email command."""
    # Get body from argument or stdin
    body = args.body
    if body is None:
        # Check if stdin is not a terminal (i.e., piped input)
        if not sys.stdin.isatty():
            body = sys.stdin.read()
        else:
            print("Error: --body is required when not reading from stdin", file=sys.stderr)
            return 1

    # Validate body is not empty
    if not body or not body.strip():
        print("Error: Email body cannot be empty", file=sys.stderr)
        return 1

    try:
        if args.verbose:
            print(f"Sending email to: {args.to}")
            print(f"Subject: {args.subject}")
            print(f"Body length: {len(body)} characters")

        logger.info(f"CLI: Sending email to {args.to} with subject: {args.subject}")
        send_email_http(args.to, args.subject, body)

        print(f"✓ Email sent successfully to {args.to}")
        logger.info(f"CLI: Email sent successfully to {args.to}")
        return 0

    except ValueError as e:
        print(f"✗ Configuration error: {e}", file=sys.stderr)
        logger.error(f"CLI: Configuration error: {e}")
        return 1

    except Exception as e:
        print(f"✗ Error sending email: {e}", file=sys.stderr)
        logger.error(f"CLI: Error sending email: {e}", exc_info=True)
        return 1


def cmd_get_email(args):
    """Handle the get-email command."""
    try:
        if args.verbose:
            print(f"Looking up alias: {args.alias}")

        logger.info(f"CLI: Looking up email for alias: {args.alias}")
        email = get_email_by_alias(args.alias)

        print(email)
        logger.info(f"CLI: Found email {email} for alias: {args.alias}")
        return 0

    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        logger.error(f"CLI: Error looking up alias '{args.alias}': {e}")
        return 1

    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        logger.error(f"CLI: Unexpected error looking up alias '{args.alias}': {e}", exc_info=True)
        return 1


def cmd_send_teams(args):
    """Handle the send-teams command."""
    # Get message from argument or stdin
    message = args.message
    if message is None:
        # Check if stdin is not a terminal (i.e., piped input)
        if not sys.stdin.isatty():
            message = sys.stdin.read()
        else:
            print("Error: --message is required when not reading from stdin", file=sys.stderr)
            return 1

    # Validate message is not empty
    if not message or not message.strip():
        print("Error: Message cannot be empty", file=sys.stderr)
        return 1

    try:
        if args.verbose:
            print(f"Sending Teams {args.format} to: {args.to}")
            print(f"Bot mode: {args.bot}")
            print(f"Message length: {len(message)} characters")

        logger.info(f"CLI: Sending Teams {args.format} to {args.to} (bot={args.bot})")
        send_teams_message(args.to, message, args.bot, args.format)

        print(f"✓ Teams {args.format} sent successfully to {args.to}")
        logger.info(f"CLI: Teams {args.format} sent successfully to {args.to}")
        return 0

    except ValueError as e:
        print(f"✗ Configuration error: {e}", file=sys.stderr)
        logger.error(f"CLI: Configuration error: {e}")
        return 1

    except Exception as e:
        print(f"✗ Error sending Teams message: {e}", file=sys.stderr)
        logger.error(f"CLI: Error sending Teams message: {e}", exc_info=True)
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="kommunicator-cli",
        description="Kommunicator CLI - Command line interface for interacting with Kommunicator services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        dest="command",
        required=True,
        help="Command to execute"
    )

    # Send-email command
    email_parser = subparsers.add_parser(
        "send-email",
        help="Send an email via Teams webhook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send a simple email with email address
  kommunicator-cli send-email --to user@example.com --subject "Meeting" --body "Meeting at 2pm"

  # Send email using an alias
  kommunicator-cli send-email --to john --subject "Hello" --body "Hi John!"

  # Send email using multi-word alias
  kommunicator-cli send-email --to "john doe" --subject "Meeting" --body "See you at 2pm"

  # Send email with message from stdin
  echo "Hello World" | kommunicator-cli send-email --to john --subject "Greeting"

  # Send email with message from file
  cat message.txt | kommunicator-cli send-email --to user@example.com --subject "Report"

Environment Variables:
  TEAMS_WEBHOOK_KOMMUNICATOR - Required Teams webhook URL
        """
    )

    email_parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address or alias"
    )

    email_parser.add_argument(
        "--subject",
        required=True,
        help="Email subject"
    )

    email_parser.add_argument(
        "--body",
        help="Email body content (or read from stdin if not provided)"
    )

    email_parser.set_defaults(func=cmd_email)

    # Get-email command
    get_email_parser = subparsers.add_parser(
        "get-email",
        help="Look up email address by alias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Look up email by alias
  kommunicator-cli get-email --alias "john"

  # Look up email by multi-word alias
  kommunicator-cli get-email --alias "john smith"

  # Look up email by auto-generated alias
  kommunicator-cli get-email --alias "moore"

Configuration:
  Uses conf/humans.conf for alias-to-email mappings
        """
    )

    get_email_parser.add_argument(
        "--alias",
        required=True,
        help="Alias to look up (case-insensitive, can be multi-word)"
    )

    get_email_parser.set_defaults(func=cmd_get_email)

    # Send-teams command
    send_teams_parser = subparsers.add_parser(
        "send-teams",
        help="Send a Teams message to a user",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send a simple Teams message with email address
  kommunicator-cli send-teams --to user@example.com --message "Hello World"

  # Send Teams message using an alias
  kommunicator-cli send-teams --to john --message "Meeting at 2pm"

  # Send Teams message using multi-word alias
  kommunicator-cli send-teams --to "john doe" --message "Quick reminder"

  # Send message from stdin
  echo "Hello World" | kommunicator-cli send-teams --to john

  # Send message from file
  cat message.txt | kommunicator-cli send-teams --to user@example.com

  # Send bot message (automatic/system message)
  kommunicator-cli send-teams --to john --message "Automatic reminder" --bot

  # Send Adaptive Card from JSON file
  cat adaptivecard.json | kommunicator-cli send-teams --to john --format adaptivecard

  # Send Adaptive Card with bot mode
  cat adaptivecard.json | kommunicator-cli send-teams --to john --format adaptivecard --bot

Environment Variables:
  TEAMS_WEBHOOK_KOMMUNICATOR - Required Teams webhook URL
        """
    )

    send_teams_parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address or alias"
    )

    send_teams_parser.add_argument(
        "--message",
        help="Message content (or read from stdin if not provided)"
    )

    send_teams_parser.add_argument(
        "--format",
        choices=["auto", "message", "adaptivecard"],
        default="auto",
        help="Message format: 'auto' (auto-detect, default), 'message' for plain text, or 'adaptivecard' for Adaptive Card"
    )

    send_teams_parser.add_argument(
        "--bot",
        action="store_true",
        help="Mark the message as coming from a bot"
    )

    send_teams_parser.set_defaults(func=cmd_send_teams)

    # Parse arguments
    args = parser.parse_args()

    # Execute the command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
