import abc
from datetime import datetime
from typing import List, Optional

from app.src.roles.investigator import BaseInvestigator
from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask, Lead


class BaseEditor(BaseJournalist):
    """
    Master editor abstract class: takes leads, plans tasks, assigns to agents,
    handles human approval for tool calls, aggregates results, and drives final output.
    """

    def __init__(self, name: str, journal_dir: str | None = "app/data"):  # Added journal_dir
        """Initializes BaseEditor.

        Args:
            name (str): The name of the editor.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)  # Pass journal_dir

    @abc.abstractmethod
    def generate_plan(self, lead: Lead) -> List[InvestigationTask]:
        pass

    @abc.abstractmethod
    def get_investigator_for_task(self, task: InvestigationTask) -> BaseInvestigator:
        """
        Returns the appropriate investigator for the given task.
        This method should be implemented by subclasses to determine
        which investigator is best suited for the task.
        """
        pass

    def solve_task(
        self, task: InvestigationTask, investigator: BaseInvestigator
    ) -> InvestigationTask:
        solved_task: InvestigationTask = investigator.run(task)
        return solved_task

    def _run(self, lead: Lead) -> List[InvestigationTask]:
        """
        Template method for running the editor's workflow with logging.
        """
        self.logger.info(
            f"[Editor] Starting lead {lead.lead_id} at {datetime.now().isoformat()}"
        )
        tasks: List[InvestigationTask] = self.generate_plan(lead)

        solved_tasks: List[InvestigationTask] = []
        for task in tasks:
            investigator: BaseInvestigator = self.get_investigator_for_task(task)
            solved_task: InvestigationTask = self.solve_task(task, investigator)
            solved_tasks.append(solved_task)

        self.logger.info(
            f"[Editor] Completed lead {lead.lead_id} with {len(solved_tasks)} tasks"
        )
        return solved_tasks
