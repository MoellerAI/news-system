from typing import List, Sequence # Removed cast

from app.src.roles.editor import BaseEditor
from app.src.roles.investigator import BaseInvestigator
from app.src.schemas.base import InvestigationTask, Lead
from .basic_investigator_one import BasicInvestigatorOne
from .basic_investigator_two import BasicInvestigatorTwo


class BasicEditor(BaseEditor):
    """
    A basic dummy implementation of an editor.
    It creates a predefined set of tasks for any lead and assigns them
    alternately to BasicInvestigatorOne and BasicInvestigatorTwo.
    """

    def __init__(self, name: str = "BasicEditor", journal_dir: str | None = "app/data", investigators: Sequence[BaseInvestigator] | None = None): # Changed List to Sequence
        """Initializes BasicEditor.

        Args:
            name (str): The name of the editor.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
            investigators (Sequence[BaseInvestigator] | None): A sequence of investigators. 
                                                        If None, initializes with default basic investigators.
        """
        super().__init__(name=name, journal_dir=journal_dir)
        if investigators is None:
            self.investigators: List[BaseInvestigator] = [ # Keep as List for internal mutable list
                BasicInvestigatorOne(journal_dir=journal_dir), # Pass journal_dir
                BasicInvestigatorTwo(journal_dir=journal_dir)  # Pass journal_dir
            ]
        else:
            self.investigators: List[BaseInvestigator] = list(investigators) # Convert Sequence to List for internal use
        self.investigator_idx: int = 0 # For round-robin assignment

    def generate_plan(self, lead: Lead) -> List[InvestigationTask]:
        """
        Generates a dummy investigation plan for the given lead.

        Creates two predefined tasks for each lead.

        Args:
            lead (Lead): The lead to generate a plan for.

        Returns:
            List[InvestigationTask]: A list of dummy investigation tasks.
        """
        self.logger.info(f"Editor {self.name} generating plan for lead: {lead.lead_id}")
        
        tasks: List[InvestigationTask] = [
            InvestigationTask(
                task_id=f"{lead.lead_id}_task_1",
                description=f"First dummy task for lead: {lead.content[:50]}...",
                content=lead.content,
                assigned_to="", # Will be assigned by get_investigator_for_task
            ),
            InvestigationTask(
                task_id=f"{lead.lead_id}_task_2",
                description=f"Second dummy task for lead: {lead.content[:50]}...",
                content=lead.content,
                assigned_to="", # Will be assigned by get_investigator_for_task
            ),
        ]
        self.logger.info(f"Editor {self.name} generated {len(tasks)} tasks for lead: {lead.lead_id}")
        return tasks

    def get_investigator_for_task(self, task: InvestigationTask) -> BaseInvestigator:
        """
        Assigns an investigator to the task in a round-robin fashion.

        Args:
            task (InvestigationTask): The task to assign an investigator to.

        Returns:
            BaseInvestigator: The investigator assigned to the task.
        """
        if not self.investigators:
            self.logger.error("No investigators available to assign task.")
            # This case should ideally be handled more gracefully, 
            # perhaps by raising an exception or ensuring investigators are always present.
            raise ValueError("No investigators available in the editor.")

        investigator: BaseInvestigator = self.investigators[self.investigator_idx % len(self.investigators)]
        task.assigned_to = investigator.name
        self.logger.info(f"Editor {self.name} assigned task {task.task_id} to investigator {investigator.name}")
        self.investigator_idx += 1
        return investigator
    
    # _run method is inherited from BaseEditor and uses the above methods.
    # No need to override it for this basic implementation unless specific
    # pre/post processing for the whole lead is needed here.
