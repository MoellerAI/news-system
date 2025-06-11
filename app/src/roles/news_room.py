import logging
import os
from datetime import datetime
from typing import List, Optional

from app.src.roles.editor import BaseEditor
from app.src.roles.investigator import (
    BaseInvestigator,
)
from app.src.schemas.base import Lead, InvestigationTask


class NewsRoom:  # Renamed from BaseNewsRoom
    """A class representing a News Room.

    The News Room coordinates an editor and a team of investigators to process
    leads and produce a list of solved investigation tasks. It handles its own
    logging.

    Attributes:
        name (str): The name of the news room.
        editor (BaseEditor): The editor responsible for planning and assigning tasks.
        investigators (List[BaseInvestigator]): A list of investigators available.
        journal_dir (Optional[str]): Directory to store logs.
        logger (logging.Logger): The logger instance for this news room.
    """

    def __init__(
        self,
        name: str,
        editor: BaseEditor,
        investigators: List[BaseInvestigator],
        journal_dir: Optional[str] = "app/data",
    ):
        """Initializes the NewsRoom.

        Args:
            name (str): The name of the news room.
            editor (BaseEditor): The editor for this news room.
            investigators (List[BaseInvestigator]): The list of investigators.
            journal_dir (Optional[str]): Directory to store logs. Defaults to "app/data".
        """
        self.name: str = name
        self.editor: BaseEditor = editor
        self.investigators: List[BaseInvestigator] = investigators
        self.journal_dir: Optional[str] = journal_dir
        self.logger: logging.Logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Sets up a logger for the news room.

        The logger will log to a file in the journal_dir directory if specified,
        otherwise to the console. The log file name will be in the format:
        <news_room_name>_<YYYY-MM-DD>.log.

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

    def run(self, lead: Lead) -> List[InvestigationTask]:  # Changed signature
        """Processes a given lead through the news room's editor.

        The editor will generate a plan, assign tasks to investigators, and return
        the solved tasks.

        Args:
            lead (Lead): The lead to be investigated.

        Returns:
            List[InvestigationTask]: A list of tasks that have been processed.
        """
        # Removed kwargs.get("lead") and the subsequent check, as lead is now a direct parameter.
        # Type checking for lead is handled by Python's type hinting system at development time
        # and potentially at runtime if static analysis tools or runtime checkers are used.
        # If explicit runtime check is still desired, it can be added back:
        # if not isinstance(lead, Lead):
        #     self.logger.error(f"Argument 'lead' must be of type Lead, got {type(lead)}")
        #     raise TypeError(f"Argument 'lead' must be of type Lead, got {type(lead)}")

        # Truncate lead.content for logging if it's too long
        log_content: str = (
            lead.content[:50] + "..." if len(lead.content) > 50 else lead.content
        )
        self.logger.info(
            f"News Room {self.name} received lead: {lead.lead_id} - {log_content}"
        )

        # The editor's run method handles the orchestration
        solved_tasks: List[InvestigationTask] = self.editor.run(lead=lead)

        self.logger.info(
            f"News Room {self.name} finished processing lead: {lead.lead_id}. Solved tasks: {len(solved_tasks)}"
        )
        return solved_tasks

