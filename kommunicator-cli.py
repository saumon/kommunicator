#!/usr/bin/env python3
"""
Kommunicator CLI - Command line interface for interacting with Kommunicator services.
"""

import sys
import argparse
from utils import send_email_http
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

    # Email command
    email_parser = subparsers.add_parser(
        "email",
        help="Send an email via Teams webhook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send a simple email
  %(prog)s email --to user@example.com --subject "Meeting" --body "Meeting at 2pm"

  # Send email with message from stdin
  echo "Hello World" | %(prog)s email --to user@example.com --subject "Greeting"

  # Send email with message from file
  cat message.txt | %(prog)s email --to user@example.com --subject "Report"

Environment Variables:
  TEAMS_WEBHOOK_URL_SEND_EMAIL_TO_USER - Required Teams webhook URL
        """
    )

    email_parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address"
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

    # Parse arguments
    args = parser.parse_args()

    # Execute the command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
