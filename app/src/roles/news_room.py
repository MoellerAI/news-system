import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional  # Added Any

from app.src.roles.editor import BaseEditor
from app.src.roles.investigator import BaseInvestigator
from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask, Lead
from app.src.utils.logging_utils import redirect_loggers_to_handler  # Added import


class NewsRoom:
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

        # Initialize the NewsRoom's own logger.
        # This logger's output will be managed by the run() method for lead-specific logging.
        self.logger: logging.Logger = logging.getLogger(
            self.name
        )  # Use NewsRoom's actual name
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.NullHandler())
        self.logger.propagate = False

    def run(self, lead: Lead) -> List[InvestigationTask]:
        """Processes a given lead.
        All logs for this specific lead (from NewsRoom, Editor, Investigators)
        will be directed to a single file: <journal_dir>/<lead_id>.log.
        The logger name in the log entries will reflect the actual source component.

        Args:
            lead (Lead): The lead to be investigated.

        Returns:
            List[InvestigationTask]: A list of tasks that have been processed.
        """

        lead_file_handler: Optional[logging.FileHandler] = None
        if self.journal_dir:
            if not os.path.exists(self.journal_dir):
                os.makedirs(self.journal_dir)
            lead_log_file_path: str = os.path.join(
                self.journal_dir, f"{lead.lead_id}.log"
            )
            lead_file_handler = logging.FileHandler(
                lead_log_file_path, mode="a"
            )  # Append mode
            formatter: logging.Formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            lead_file_handler.setFormatter(formatter)
        else:
            self.logger.warning(
                f"No journal_dir configured for NewsRoom {self.name}. "
                f"Logs for lead {lead.lead_id} will not be saved to a dedicated file."
            )
            # If no journal_dir, proceed without file logging for this lead.
            # Components will use their NullHandlers or other pre-configured handlers.
            log_content_no_file: str = (
                lead.content[:50] + "..." if len(lead.content) > 50 else lead.content
            )
            self.logger.info(
                f"News Room {self.name} received lead: {lead.lead_id} - {log_content_no_file}"
            )
            solved_tasks_no_file: List[InvestigationTask] = self.editor.run(lead=lead)
            self.logger.info(
                f"News Room {self.name} finished processing lead: {lead.lead_id}. "
                f"Solved tasks: {len(solved_tasks_no_file)}"
            )
            return solved_tasks_no_file

        # At this point, lead_file_handler is guaranteed to be a FileHandler
        # because the else block above returns.

        journalists_involved: List[BaseJournalist] = [self.editor] + self.investigators
        all_loggers_for_lead: List[logging.Logger] = [self.logger]
        all_loggers_for_lead.extend([j.logger for j in journalists_involved])

        try:
            with redirect_loggers_to_handler(all_loggers_for_lead, lead_file_handler):
                log_content: str = (
                    lead.content[:50] + "..."
                    if len(lead.content) > 50
                    else lead.content
                )
                self.logger.info(
                    f"News Room {self.name} received lead: {lead.lead_id} - {log_content}"
                )

                solved_tasks: List[InvestigationTask] = self.editor.run(lead=lead)

                self.logger.info(
                    f"News Room {self.name} finished processing lead: {lead.lead_id}. "
                    f"Solved tasks: {len(solved_tasks)}"
                )
                return solved_tasks
        finally:
            if lead_file_handler:
                lead_file_handler.close()
