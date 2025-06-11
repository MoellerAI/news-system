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
        """Initializes BaseJournalist.

        Args:
            name (Optional[str]): The name of the journalist. Defaults to class name.
            journal_dir (Optional[str]): Default directory to store logs if this journalist
                                     manages its own file logging independently.
                                     Not used for file creation in this constructor.
        """
        self.name: str = name or self.__class__.__name__
        self.journal_dir: Optional[str] = (
            journal_dir  # Store for potential independent use
        )

        self.logger: logging.Logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)  # Default level

        # Add NullHandler if no handlers are configured to prevent "No handlers" warnings.
        # This allows the logger to be used without output until handlers are added.
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.NullHandler())

        self.logger.propagate = False  # Prevent logs from going to the root logger

    def _setup_logger(
        self,
        logger_name: str,  # Should typically be self.name
        journal_dir: Optional[str],
        log_filename: Optional[str] = None,
    ) -> logging.Logger:
        """Utility to configure a logger instance, typically self.logger.

        This can be called by a journalist instance if it needs to set up its own
        file logging independently of an orchestrator like NewsRoom.

        Args:
            logger_name (str): The name for the logger instance.
            journal_dir (Optional[str]): Directory to store log files.
            log_filename (Optional[str]): Specific filename for the log file. If None,
                                     a default name (<logger_name>_<YYYY-MM-DD>.log) is used.

        Returns:
            logging.Logger: The configured logger instance.
        """
        # Get the logger instance (could be self.logger or another)
        logger_to_configure: logging.Logger = logging.getLogger(logger_name)
        logger_to_configure.setLevel(logging.INFO)  # Ensure level is set

        # Clear any existing handlers to prevent duplicate logging or incorrect file output
        if logger_to_configure.hasHandlers():
            for handler in logger_to_configure.handlers[:]:  # Iterate over a copy
                handler.close()
                logger_to_configure.removeHandler(handler)

        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if journal_dir:
            if not os.path.exists(journal_dir):
                os.makedirs(journal_dir)

            final_log_filename: str
            if log_filename:
                final_log_filename = log_filename
            else:
                final_log_filename = (
                    f"{logger_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
                )

            file_path: str = os.path.join(journal_dir, final_log_filename)
            file_handler: logging.FileHandler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger_to_configure.addHandler(file_handler)
        else:
            # Fallback to console logging if no journal_dir, or add NullHandler
            # For this utility, let's add a console handler if no journal_dir.
            # If called from __init__ (which it isn't anymore for file setup),
            # NullHandler is preferred.
            if (
                not logger_to_configure.hasHandlers()
            ):  # Add console if still no handlers
                console_handler: logging.StreamHandler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger_to_configure.addHandler(console_handler)

        logger_to_configure.propagate = False
        return logger_to_configure

    @abc.abstractmethod
    def _run(self, logger_to_use: logging.Logger, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method that subclasses must implement to define their specific behavior.
        This method is called by the run() method.

        Args:
            logger_to_use (logging.Logger): The logger instance to be used for logging.
                                          This is typically self.logger, which might be
                                          reconfigured by an orchestrator.
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
        It uses self.logger. The handlers for self.logger might be dynamically
        managed by an orchestrator (like NewsRoom) to direct logs to specific files.

        Args:
            *args: Variable length argument list to be passed to _run.
            **kwargs: Arbitrary keyword arguments to be passed to _run.

        Returns:
            Any: The result of the _run method.
        """
        # self.logger is the journalist's own named logger.
        # Its handlers determine where the log output goes.
        self.logger.info(f"Starting execution for {self.name}.")
        result: Any = self._run(
            self.logger, *args, **kwargs
        )  # Pass self.logger to _run
        self.logger.info(f"Finished execution for {self.name}.")
        return result
