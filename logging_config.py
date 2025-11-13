import logging
from pathlib import Path

_logging_configured = False


def setup_logging():
    """Configure logging to file for the MCP Kommunicator application."""
    global _logging_configured

    if _logging_configured:
        return

    log_file = Path(__file__).parent / "kommunicator.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
        ]
    )

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name. Automatically configures logging on first call."""
    setup_logging()
    return logging.getLogger(name)
