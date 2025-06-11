import logging
from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional  # Ensure Optional is imported

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
        self, logger_to_use: logging.Logger, task: InvestigationTask
    ) -> InvestigationTask:
        """
        Perform the investigation for a single task.
        Must return a solved task with results.

        Args:
            logger_to_use (logging.Logger): The logger to use for this investigation.
            task (InvestigationTask): The task to investigate.
        Returns:
            InvestigationTask: The solved task.
        """
        raise NotImplementedError

    def _run(
        self, logger_to_use: logging.Logger, *args: Any, **kwargs: Any
    ) -> InvestigationTask:
        """
        Template method for running an investigation with logging and retries.
        Args:
            logger_to_use (logging.Logger): The logger to use for this run.
            *args: Variable length argument list. Expected to contain 'task' in kwargs.
            **kwargs: Arbitrary keyword arguments. Expected to contain 'task'.
        Returns:
            InvestigationTask: The processed task.
        Raises:
            ValueError: If 'task' is not provided in kwargs.
        """
        task: Optional[InvestigationTask] = kwargs.get("task")
        if not task or not isinstance(task, InvestigationTask):
            logger_to_use.error(
                "'task' argument of type InvestigationTask must be provided in kwargs to BaseInvestigator._run"
            )
            raise ValueError(
                "'task' argument of type InvestigationTask must be provided in kwargs"
            )

        logger_to_use.info(
            f"[Investigator] Starting task {task.task_id} at {datetime.now().isoformat()}"
        )
        try:
            result_task: InvestigationTask = self.investigate(logger_to_use, task)
            logger_to_use.info(f"[Investigator] Task {task.task_id} succeeded")
            return result_task
        except Exception as e:
            logger_to_use.warning(f"[Investigator] Task {task.task_id} failed: {e}")
            task.status = "failed"
            return task
