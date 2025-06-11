import logging
from datetime import datetime

from app.src.roles.investigator import BaseInvestigator
from app.src.schemas.base import InvestigationTask


class BasicInvestigatorOne(BaseInvestigator):
    """
    A basic dummy implementation of an investigator.
    This investigator simply marks the task as done and adds a dummy result.
    """

    def __init__(
        self, name: str = "BasicInvestigatorOne", journal_dir: str | None = "app/data"
    ):
        """Initializes BasicInvestigatorOne.

        Args:
            name (str): The name of the investigator.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)

    def investigate(self, task: InvestigationTask) -> InvestigationTask:
        """
        Processes the given investigation task.
        Uses self.logger for logging.

        This dummy implementation logs the task, marks it as 'done',
        and adds a simple string as a result.

        Args:
            task (InvestigationTask): The investigation task to be processed.

        Returns:
            InvestigationTask: The processed task with status updated and a dummy result.
        """
        self.logger.info(
            f"Investigator {self.name} processing task: {task.task_id} - {task.description}"
        )

        # Simulate investigation work
        task.result = f"Dummy result for task {task.task_id} from {self.name}"
        task.status = "done"
        task.completed_at = datetime.now()

        self.logger.info(f"Investigator {self.name} completed task: {task.task_id}")
        return task
