import abc
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from app.src.roles.journalist import BaseJournalist
from app.src.schemas.base import InvestigationTask, Source


class BaseInvestigator(BaseJournalist):
    """
    Abstract Investigator: defines a template _run and requires subclasses
    to implement investigate().
    """

    def __init__(self, name: str, journal_dir: str | None = "app/data"):  # Added journal_dir
        """Initializes BaseInvestigator.

        Args:
            name (str): The name of the investigator.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        super().__init__(name=name, journal_dir=journal_dir)  # Pass journal_dir

    @abstractmethod
    def investigate(self, task: InvestigationTask) -> InvestigationTask:
        """
        Perform the investigation for a single task.
        Must return a solved task with results.
        """
        pass

    def _run(self, task: InvestigationTask) -> InvestigationTask:
        """
        Template method for running an investigation with logging and retries.
        """
        self.logger.info(
            f"[Investigator] Starting task {task.task_id} at {datetime.now().isoformat()}"
        )
        try:
            result = self.investigate(task)
            self.logger.info(f"[Investigator] Task {task.task_id} succeeded")
            return result
        except:
            self.logger.warning(f"[Investigator] Task {task.task_id} failed")
            task.status = "failed"
            return task
