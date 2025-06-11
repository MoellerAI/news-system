import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from app.src.roles.editor import BaseEditor
from app.src.roles.investigator import BaseInvestigator
from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask, Lead


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
            # Logs will go to wherever the components' loggers are currently configured
            # (e.g., NullHandler or console if that's their default).

        # Loggers whose output should go to the lead_id.log for this run
        # This includes the NewsRoom's own logger (self.logger), the editor, and all investigators.
        journalists_involved: List[BaseJournalist] = [self.editor] + self.investigators
        # self.logger is now logging.getLogger(self.name), e.g., "BasicNewsRoom"
        all_loggers_for_lead: List[logging.Logger] = [self.logger]
        all_loggers_for_lead.extend([j.logger for j in journalists_involved])

        original_handlers_map: Dict[logging.Logger, List[logging.Handler]] = {}
        original_propagate_map: Dict[logging.Logger, bool] = {}

        if lead_file_handler:
            for logger_instance in all_loggers_for_lead:
                original_handlers_map[logger_instance] = logger_instance.handlers[:]
                original_propagate_map[logger_instance] = logger_instance.propagate

                # Remove all existing handlers
                for h in logger_instance.handlers[:]:
                    # Do not close NullHandlers or system handlers if they are not file handlers
                    # However, for this specific redirection, we clear all to ensure exclusive output.
                    if isinstance(
                        h, logging.FileHandler
                    ):  # Close file handlers before removing
                        h.close()
                    logger_instance.removeHandler(h)

                logger_instance.addHandler(lead_file_handler)
                logger_instance.propagate = False

        try:
            log_content: str = (
                lead.content[:50] + "..." if len(lead.content) > 50 else lead.content
            )
            # This log message will use self.logger (e.g., logger named "BasicNewsRoom")
            # which now has lead_file_handler attached.
            self.logger.info(
                f"News Room {self.name} received lead: {lead.lead_id} - {log_content}"
            )

            # The editor.run() will use editor.logger, which also has lead_file_handler.
            # Inside editor.run(), it calls investigator.run(), which uses investigator.logger,
            # also now equipped with lead_file_handler.
            solved_tasks: List[InvestigationTask] = self.editor.run(lead=lead)

            self.logger.info(
                f"News Room {self.name} finished processing lead: {lead.lead_id}. "
                f"Solved tasks: {len(solved_tasks)}"
            )
            return solved_tasks
        finally:
            if lead_file_handler:
                for logger_instance in all_loggers_for_lead:
                    logger_instance.removeHandler(lead_file_handler)
                    # Restore original handlers
                    for original_handler in original_handlers_map.get(
                        logger_instance, []
                    ):
                        logger_instance.addHandler(original_handler)
                    # Restore original propagate status
                    logger_instance.propagate = original_propagate_map.get(
                        logger_instance, False
                    )

                lead_file_handler.close()
