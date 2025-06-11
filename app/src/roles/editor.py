import abc
import logging
from datetime import datetime
from typing import Any, List, Optional  # Added Optional

from app.src.roles.investigator import BaseInvestigator
from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask, Lead


class BaseEditor(BaseJournalist):
    """
    Master editor abstract class: takes leads, plans tasks, assigns to agents,
    handles human approval for tool calls, aggregates results, and drives final output.
    """

    def __init__(
        self, name: str, journal_dir: str | None = "app/data"
    ):  # Added journal_dir
        """Initializes BaseEditor.

        Args:
            name (str): The name of the editor.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)  # Pass journal_dir

    @abc.abstractmethod
    def generate_plan(self, lead: Lead) -> List[InvestigationTask]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_investigator_for_task(self, task: InvestigationTask) -> BaseInvestigator:
        """
        Returns the appropriate investigator for the given task.
        This method should be implemented by subclasses to determine
        which investigator is best suited for the task.
        """
        raise NotImplementedError

    def solve_task(
        self, task: InvestigationTask, investigator: BaseInvestigator
    ) -> InvestigationTask:
        # The investigator will use its own logger, which should be configured by the NewsRoom
        solved_task: InvestigationTask = investigator.run(task=task)
        return solved_task

    def _run(
        self, logger_to_use: logging.Logger, *args: Any, **kwargs: Any
    ) -> List[InvestigationTask]:
        """
        Template method for running the editor's workflow with logging.

        Args:
            logger_to_use (logging.Logger): The logger to use for this run.
            *args: Variable length argument list. Expected to contain 'lead' in kwargs.
            **kwargs: Arbitrary keyword arguments. Expected to contain 'lead'.

        Returns:
            List[InvestigationTask]: A list of solved tasks.

        Raises:
            ValueError: If 'lead' is not provided in kwargs.
        """
        lead: Optional[Lead] = kwargs.get("lead")
        if not lead or not isinstance(lead, Lead):
            logger_to_use.error(
                "'lead' argument of type Lead must be provided in kwargs to BaseEditor._run"
            )
            raise ValueError("'lead' argument of type Lead must be provided in kwargs")

        logger_to_use.info(
            f"[Editor] Starting lead {lead.lead_id} at {datetime.now().isoformat()}"
        )
        tasks: List[InvestigationTask] = self.generate_plan(lead)

        solved_tasks: List[InvestigationTask] = []
        for task_item in tasks:
            investigator: BaseInvestigator = self.get_investigator_for_task(task_item)
            solved_task: InvestigationTask = investigator.run(
                task=task_item
            )  # Pass task as keyword argument
            solved_tasks.append(solved_task)

        logger_to_use.info(
            f"[Editor] Completed lead {lead.lead_id} with {len(solved_tasks)} tasks"
        )
        return solved_tasks
