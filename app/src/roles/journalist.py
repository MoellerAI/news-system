import abc
import logging
import os
from datetime import datetime
from typing import Any, Optional


class BaseJournalist(abc.ABC):
    """
    Master abstract class for AI agents (Journalists) in the system.
    Handles logging. Name defaults to subclass name.
    Provides template run() that logs at start and end, delegating to _run().
    """

    def __init__(
        self, name: Optional[str] = None, journal_dir: Optional[str] = "app/data"
    ):
        # Default name to class name if not given
        self.name: str = name or self.__class__.__name__
        self.journal_dir: Optional[str] = journal_dir
        self.logger: logging.Logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Sets up a logger for the journalist.

        The logger will log to a file in the journal_dir directory.
        The log file name will be in the format: <journalist_name>_<YYYY-MM-DD>.log.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger: logging.Logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create file handler if journal_dir is specified
        if self.journal_dir:
            # Ensure the journal directory exists
            if not os.path.exists(self.journal_dir):
                os.makedirs(self.journal_dir)

            log_file_name: str = (
                f"{self.name}_{datetime.now().strftime('%Y-%m-%d')}.log"
            )
            file_handler: logging.FileHandler = logging.FileHandler(
                os.path.join(self.journal_dir, log_file_name)
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            # If no journal_dir is specified, log to console
            console_handler: logging.StreamHandler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    @abc.abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method that subclasses must implement to define their specific behavior.
        This method is called by the run() method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the subclass does not implement this method.

        Returns:
            Any: The result of the journalist's execution.
        """
        raise NotImplementedError

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Runs the journalist's task.

        Logs an informational message before and after calling the _run method.

        Args:
            *args: Variable length argument list to be passed to _run.
            **kwargs: Arbitrary keyword arguments to be passed to _run.

        Returns:
            Any: The result of the _run method.
        """
        self.logger.info(f"Starting execution for {self.name}.")
        result: Any = self._run(*args, **kwargs)
        self.logger.info(f"Finished execution for {self.name}.")
        return result
