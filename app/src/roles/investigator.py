import logging
from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional  # Added Any, Optional

from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask


class BaseInvestigator(BaseJournalist):
    """
    Abstract Investigator: defines a template _run and requires subclasses
    to implement investigate().
    """

    def __init__(
        self, name: str, journal_dir: str | None = "app/data"
    ):  # Added journal_dir
        """Initializes BaseInvestigator.

        Args:
            name (str): The name of the investigator.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)  # Pass journal_dir

    @abstractmethod
    def investigate(
        self, task: InvestigationTask
    ) -> InvestigationTask:  # Removed logger_to_use
        """
        Perform the investigation for a single task.
        Uses self.logger.
        Must return a solved task with results.

        Args:
            task (InvestigationTask): The task to investigate.
        Returns:
            InvestigationTask: The solved task.
        """
        raise NotImplementedError

    def _run(
        self, *args: Any, **kwargs: Any
    ) -> InvestigationTask:  # Removed logger_to_use
        """
        Template method for running an investigation with logging and retries.
        Uses self.logger.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Expected to contain 'task'.
        Returns:
            InvestigationTask: The processed task.
        Raises:
            ValueError: If 'task' is not provided in kwargs.
        """
        task: Optional[InvestigationTask] = kwargs.get("task")
        if not task or not isinstance(task, InvestigationTask):
            self.logger.error(
                "'task' argument of type InvestigationTask must be provided in kwargs to BaseInvestigator._run"
            )
            raise ValueError(
                "'task' argument of type InvestigationTask must be provided in kwargs"
            )

        self.logger.info(
            f"[Investigator] Starting task {task.task_id} at {datetime.now().isoformat()}"
        )
        try:
            result_task: InvestigationTask = self.investigate(
                task
            )  # self.investigate will use self.logger
            self.logger.info(
                f"[Investigator] Task {task.task_id} succeeded"
            )  # Use self.logger
            return result_task
        except Exception as e:
            self.logger.warning(
                f"[Investigator] Task {task.task_id} failed: {e}"
            )  # Use self.logger
            task.status = "failed"
            return task
