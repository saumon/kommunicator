from logging_config import get_logger
import os
import requests

logger = get_logger(__name__)


def send_email_http(to: str, subject: str, body: str) -> None:
    """
    Send an email via Teams webhook.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content

    Raises:
        ValueError: If TEAMS_WEBHOOK_KOMMUNICATOR is not set
        requests.RequestException: If there's an error sending the HTTP request
        Exception: For any other unexpected errors
    """
    try:
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
