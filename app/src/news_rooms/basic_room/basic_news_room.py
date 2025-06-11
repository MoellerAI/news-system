from typing import List # Removed Sequence

from app.src.roles.news_room import NewsRoom
# Imports for Lead and InvestigationTask are not needed if the example method is commented out
# from app.src.schemas.base import Lead, InvestigationTask 
from .basic_editor import BasicEditor
from .basic_investigator_one import BasicInvestigatorOne
from .basic_investigator_two import BasicInvestigatorTwo
from app.src.roles.investigator import BaseInvestigator # Added for type hint


class BasicNewsRoom(NewsRoom):
    """
    A basic dummy implementation of a NewsRoom.
    It uses a BasicEditor and a list of BasicInvestigators.
    """

    def __init__(self, name: str = "BasicNewsRoom", journal_dir: str | None = "app/data"):
        """Initializes BasicNewsRoom.

        Args:
            name (str): The name of the news room.
            journal_dir (str | None): Directory to store logs. Defaults to "app/data".
        """
        # Initialize investigators first
        investigator1: BasicInvestigatorOne = BasicInvestigatorOne(journal_dir=journal_dir)
        investigator2: BasicInvestigatorTwo = BasicInvestigatorTwo(journal_dir=journal_dir)
        # Use BaseInvestigator for the list type hint for broader compatibility if needed
        # but for BasicNewsRoom, it's fine to be specific if these are the exact types it always uses.
        investigators_list: List[BaseInvestigator] = [investigator1, investigator2]

        # Initialize editor with these investigators
        # The BasicEditor now expects a Sequence, List is a Sequence.
        basic_editor: BasicEditor = BasicEditor(name="BasicEditorForNewsRoom", journal_dir=journal_dir, investigators=investigators_list)
        
        # Initialize the NewsRoom (superclass) with the editor and investigators
        super().__init__(
            name=name, 
            editor=basic_editor, 
            investigators=investigators_list, 
            journal_dir=journal_dir
        )
        self.logger.info(f"BasicNewsRoom '{self.name}' initialized with {len(self.investigators)} investigators and editor '{self.editor.name}'.")

    # The `run` method is inherited from the NewsRoom class.
    # It will use the configured BasicEditor which in turn uses BasicInvestigators.
    # No need to override `run` unless specific behavior for the BasicNewsRoom is needed.

    # Example of how to use the newsroom (optional, for demonstration):
    # def process_lead_example(self, lead_content: str) -> List[InvestigationTask]:
    #     """Demonstrates processing a lead.
    # 
    #     Args:
    #         lead_content (str): The content of the lead.
    # 
    #     Returns:
    #         List[InvestigationTask]: The list of solved tasks.
    #     """
    #     dummy_lead: Lead = Lead(lead_id="dummy_lead_001", lead_type="question", content=lead_content)
    #     self.logger.info(f"Processing dummy lead: {dummy_lead.lead_id}")
    #     solved_tasks: List[InvestigationTask] = self.run(lead=dummy_lead)
    #     self.logger.info(f"Finished processing dummy lead: {dummy_lead.lead_id}, {len(solved_tasks)} tasks solved.")
    #     return solved_tasks

