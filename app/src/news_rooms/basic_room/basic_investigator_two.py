import logging
from datetime import datetime

from app.src.roles.investigator import BaseInvestigator
from app.src.schemas.base import InvestigationTask


class BasicInvestigatorTwo(BaseInvestigator):
    """
    A second basic dummy implementation of an investigator.
    This investigator also marks the task as done and adds a different dummy result.
    """

    def __init__(
        self, name: str = "BasicInvestigatorTwo", journal_dir: str | None = "app/data"
    ):
        """Initializes BasicInvestigatorTwo.

        Args:
            name (str): The name of the investigator.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)

    def investigate(
        self, logger_to_use: logging.Logger, task: InvestigationTask
    ) -> InvestigationTask:
        """
        Processes the given investigation task.

        This dummy implementation logs the task, marks it as 'done',
        and adds a unique simple string as a result.

        Args:
            logger_to_use (logging.Logger): The logger to use for this investigation.
            task (InvestigationTask): The investigation task to be processed.

        Returns:
            InvestigationTask: The processed task with status updated and a dummy result.
        """
        logger_to_use.info(
            f"Investigator {self.name} processing task: {task.task_id} - {task.description}"
        )

        # Simulate investigation work
        task.result = (
            f"Alternative dummy result for task {task.task_id} from {self.name}"
        )
        task.status = "done"
        task.completed_at = datetime.now()

        logger_to_use.info(f"Investigator {self.name} completed task: {task.task_id}")
        return task
