from logging_config import get_logger
import os
import requests
from pathlib import Path
import re

logger = get_logger(__name__)

# Cache for humans configuration
_humans_config = None
_all_emails = None


def _extract_email_parts(email: str) -> list:
    """
    Extract searchable parts from an email address.

    Args:
        email: Email address

    Returns:
        list: List of searchable parts (lowercase)

    Example:
        "toto.smith@example.com" -> ["toto", "smith", "toto smith"]
        "momo.salam-ext@example.com" -> ["momo", "salam", "momo salam"]
    """
    # Get the local part (before @)
    local_part = email.split('@')[0]

    # Split by common separators (., -, _)
    parts = re.split(r'[.\-_]', local_part)

    # Filter out common suffixes like 'ext', 'int', etc.
    filtered_parts = [p for p in parts if p and p.lower() not in ['ext', 'int', 'temp']]

    searchable_parts = []

    # Add individual parts
    for part in filtered_parts:
        searchable_parts.append(part.lower())

    # Add combination of all parts (space-separated)
    if len(filtered_parts) > 1:
        searchable_parts.append(' '.join(filtered_parts).lower())

    return searchable_parts


def _load_humans_config():
    """
    Load and parse the humans.conf file.

    Returns:
        tuple: (alias_dict, email_list) - Dictionary mapping lowercase aliases to email addresses
               and list of all emails
    """
    global _humans_config, _all_emails

    if _humans_config is not None:
        return _humans_config, _all_emails

    config_file = Path(__file__).parent / "conf" / "humans.conf"
    _humans_config = {}
    _all_emails = []

    # Track duplicates to avoid ambiguous aliases
    _alias_counts = {}

    if not config_file.exists():
        logger.warning(f"Humans config file not found: {config_file}")
        return _humans_config, _all_emails

    try:
        # First pass: collect all aliases and count duplicates
        temp_aliases = {}

        with open(config_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Parse line: email = alias1, alias2, alias3
                if '=' not in line:
                    logger.warning(f"Invalid line {line_number} in humans.conf: {line}")
                    continue

                email, aliases_str = line.split('=', 1)
                email = email.strip()

                # Validate email format (basic check)
                if not email or '@' not in email:
                    logger.warning(f"Invalid email on line {line_number}: {email}")
                    continue

                # Add to email list
                _all_emails.append(email)

                # Collect all potential aliases for this email
                potential_aliases = []

                # Always generate aliases from email parts
                email_parts = _extract_email_parts(email)
                potential_aliases.extend(email_parts)

                # Parse explicit aliases and add them as well
                aliases_str = aliases_str.strip()
                if aliases_str:
                    # Has explicit aliases - add them too
                    aliases = [alias.strip() for alias in aliases_str.split(',')]
                    potential_aliases.extend([a.lower() for a in aliases if a])

                # Deduplicate aliases for this email (to avoid counting same alias twice)
                potential_aliases = list(set(potential_aliases))

                # Store email with its potential aliases
                temp_aliases[email] = potential_aliases

                # Count occurrences of each alias
                for alias in potential_aliases:
                    _alias_counts[alias] = _alias_counts.get(alias, 0) + 1

        # Second pass: add only non-ambiguous aliases
        for email, aliases in temp_aliases.items():
            for alias in aliases:
                # Only add alias if it's unique (not a duplicate)
                if _alias_counts[alias] == 1:
                    _humans_config[alias] = email
                else:
                    logger.debug(f"Skipping ambiguous alias '{alias}' (appears in multiple emails)")

            # Also map email to itself for direct email lookup
            _humans_config[email.lower()] = email

        logger.info(f"Loaded {len(_humans_config)} alias mappings from humans.conf for {len(_all_emails)} emails")
        logger.debug(f"Skipped {sum(1 for count in _alias_counts.values() if count > 1)} duplicate aliases")

    except Exception as e:
        logger.error(f"Error loading humans.conf: {e}", exc_info=True)

    return _humans_config, _all_emails


def get_email_by_alias(alias: str) -> str:
    """
    Get email address by alias.

    Supports:
    - Explicit aliases defined in humans.conf
    - Auto-generated aliases from email parts (for emails without explicit aliases)

    Examples:
        For "toto.smith@example.com =":
        - "toto" -> toto.smith@example.com
        - "smith" -> toto.smith@example.com
        - "toto smith" -> toto.smith@example.com

    Args:
        alias: Alias to lookup (case-insensitive, can be multiple words)

    Returns:
        str: Email address corresponding to the alias

    Raises:
        ValueError: If alias is not found in the configuration
    """
    if not alias or not alias.strip():
        raise ValueError("Alias cannot be empty")

    # Load config if not already loaded
    config, all_emails = _load_humans_config()

    # Normalize alias for lookup (lowercase, strip whitespace)
    normalized_alias = alias.strip().lower()

    # Look up the email
    email = config.get(normalized_alias)

    if email is None:
        logger.warning(f"Alias not found: {alias}")
        raise ValueError(f"No email found for alias: {alias}")

    logger.debug(f"Resolved alias '{alias}' to email '{email}'")
    return email


def send_email_http(to: str, subject: str, body: str) -> None:
    """
    Send an email via Teams webhook.

    Args:
        to: Recipient email address or alias
        subject: Email subject
        body: Email body content

    Raises:
        ValueError: If TEAMS_WEBHOOK_KOMMUNICATOR is not set or if alias is not found
        requests.RequestException: If there's an error sending the HTTP request
        Exception: For any other unexpected errors
    """
    try:
        # If 'to' is not an email address (doesn't contain @), treat it as an alias
        if '@' not in to:
            logger.info(f"'{to}' appears to be an alias, looking up email address")
            to = get_email_by_alias(to)
            logger.info(f"Resolved alias to email: {to}")

        logger.info(f"Attempting to send email to {to}")

        # Get webhook URL from environment variable
        webhook_url = os.getenv("TEAMS_WEBHOOK_KOMMUNICATOR")

        if not webhook_url:
            error_msg = (
                "TEAMS_WEBHOOK_KOMMUNICATOR environment variable is not set. "
                "Please set it to your Teams webhook URL."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Format message: replace newlines with <br>
        body_formatted = body.replace("\n", "<br>")

        # Prepare JSON payload
        payload = {
            "target": "email",
            "to": to,
            "subject": subject,
            "body": body_formatted
        }

        # Send POST request to webhook
        logger.debug(f"Sending POST request to webhook with payload: {payload}")
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check if request was successful
        response.raise_for_status()

        logger.debug(f"Received response: {response.status_code} - {response.text}")

        logger.info(f"Email sent successfully to {to} with subject '{subject}'")

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except requests.RequestException as e:
        logger.error(f"HTTP request error sending email: {str(e)}", exc_info=True)
        raise requests.RequestException(f"Failed to send email via webhook: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
        raise Exception(f"Unexpected error sending email: {str(e)}")


def send_teams_message(to: str, message: str, bot: bool = False, format: str = "auto") -> None:
    """
    Send a Teams message to a user via Teams webhook.

    Args:
        to: Recipient email address or alias
        message: Message content (plain text for 'message' format, JSON string for 'adaptivecard' format)
        bot: Whether the message is from a bot (default: False)
        format: Message format - 'auto' (auto-detect), 'message' for plain text, or 'adaptivecard' for Adaptive Card (default: 'auto')

    Raises:
        ValueError: If TEAMS_WEBHOOK_KOMMUNICATOR is not set, if alias is not found, or if format is invalid
        requests.RequestException: If there's an error sending the HTTP request
        Exception: For any other unexpected errors
    """
    import json
    
    try:
        # Auto-detect format if set to 'auto'
        if format == "auto":
            # Try to detect if message is an Adaptive Card JSON
            try:
                parsed_json = json.loads(message.strip())
                if isinstance(parsed_json, dict) and parsed_json.get("type") == "AdaptiveCard":
                    format = "adaptivecard"
                    logger.info("Auto-detected Adaptive Card format")
                else:
                    format = "message"
                    logger.debug("JSON detected but not an Adaptive Card, using message format")
            except (json.JSONDecodeError, ValueError):
                # Not valid JSON, treat as plain text message
                format = "message"
                logger.debug("Not valid JSON, using message format")
        
        # Validate format
        if format not in ["message", "adaptivecard"]:
            raise ValueError(f"Invalid format '{format}'. Must be 'auto', 'message' or 'adaptivecard'")

        # If 'to' is not an email address (doesn't contain @), treat it as an alias
        if '@' not in to:
            logger.info(f"'{to}' appears to be an alias, looking up email address")
            to = get_email_by_alias(to)
            logger.info(f"Resolved alias to email: {to}")

        logger.info(f"Attempting to send Teams {format} to {to}")

        # Get webhook URL from environment variable
        webhook_url = os.getenv("TEAMS_WEBHOOK_KOMMUNICATOR")

        if not webhook_url:
            error_msg = (
                "TEAMS_WEBHOOK_KOMMUNICATOR environment variable is not set. "
                "Please set it to your Teams webhook URL."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Prepare JSON payload based on format
        if format == "adaptivecard":
            # Parse the JSON content for adaptive card
            try:
                adaptive_card_content = json.loads(message)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON for adaptive card: {str(e)}")
                raise ValueError(f"Invalid JSON for adaptive card: {str(e)}")

            payload = {
                "target": "teams-message",
                "format": "adaptivecard",
                "userEmail": to,
                "bot": str(bot).lower(),
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": adaptive_card_content
                    }
                ]
            }
        else:
            # Format message: replace newlines with <br>
            message_formatted = message.replace("\n", "<br>")

            payload = {
                "target": "teams-message",
                "format": "message",
                "userEmail": to,
                "message": message_formatted,
                "bot": str(bot).lower()
            }

        # Send POST request to webhook
        logger.debug(f"Sending POST request to webhook with payload: {json.dumps(payload, indent=2)}")
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check if request was successful
        response.raise_for_status()

        logger.debug(f"Received response: {response.status_code} - {response.text}")

        logger.info(f"Teams {format} sent successfully to {to}")

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except requests.RequestException as e:
        logger.error(f"HTTP request error sending Teams message: {str(e)}", exc_info=True)
        raise requests.RequestException(f"Failed to send Teams message via webhook: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error sending Teams message: {str(e)}", exc_info=True)
        raise Exception(f"Unexpected error sending Teams message: {str(e)}")
