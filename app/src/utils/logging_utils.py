import logging
from contextlib import contextmanager
from typing import List, Dict, Any, Iterator # Added Iterator

@contextmanager
def redirect_loggers_to_handler(
    loggers: List[logging.Logger], target_handler: logging.Handler
) -> Iterator[None]:
    """Temporarily redirects a list of loggers to a specific target handler.

    Saves the original handlers and propagation settings for each logger,
    removes existing handlers, adds the target_handler, and sets propagate to False.
    Upon exiting the context, it restores the original handlers and propagation
    settings and removes the target_handler.

    Args:
        loggers (List[logging.Logger]): A list of logger instances to redirect.
        target_handler (logging.Handler): The handler to which logs should be redirected.

    Yields:
        None: Yields control back to the `with` block.
    """
    original_states: Dict[logging.Logger, Dict[str, Any]] = {}
    try:
        for logger_instance in loggers:
            original_states[logger_instance] = {
                "handlers": logger_instance.handlers[:],
                "propagate": logger_instance.propagate,
            }
            # Remove all existing handlers from the current logger instance
            for h in logger_instance.handlers[:]:
                logger_instance.removeHandler(h)
            
            logger_instance.addHandler(target_handler)
            logger_instance.propagate = False
        yield
    finally:
        for logger_instance in loggers:
            # Ensure the target_handler is removed first
            logger_instance.removeHandler(target_handler)
            
            # Restore original handlers and propagation status
            if logger_instance in original_states:
                # Add back the original handlers that were removed
                for original_handler in original_states[logger_instance]["handlers"]:
                    logger_instance.addHandler(original_handler)
                logger_instance.propagate = original_states[logger_instance]["propagate"]
            # If a logger had no original state recorded (should not happen if list is not empty)
            # it will now have no handlers (after target_handler removal) or default ones if added by getLogger.
            # This is generally fine as our BaseJournalist adds a NullHandler if none exist.
