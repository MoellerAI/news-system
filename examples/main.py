"""
Example script to demonstrate the usage of BasicNewsRoom.
"""

from typing import List

from app.src.news_rooms.basic_room.basic_news_room import BasicNewsRoom
from app.src.schemas.base import InvestigationTask


def run_basic_news_room_example() -> None:
    """
    Initializes and runs the BasicNewsRoom with a dummy lead.
    Prints the results of the investigation tasks.
    """
    print("Initializing BasicNewsRoom...")
    # Initialize the BasicNewsRoom. Logs will be in app/data/BasicNewsRoom_YYYY-MM-DD.log
    news_room: BasicNewsRoom = BasicNewsRoom(journal_dir="app/data/examples")

    dummy_lead_content: str = (
        "This is a dummy lead for the BasicNewsRoom to process. What happened?"
    )
    print(f"Processing dummy lead: '{dummy_lead_content}'")

    # Process the dummy lead
    solved_tasks: List[InvestigationTask] = news_room.process_lead_example(
        lead_content=dummy_lead_content
    )

    print("\\n--- Results of Investigation Tasks ---")
    if solved_tasks:
        for i, task in enumerate(solved_tasks):
            print(f"Task {i+1}:")
            print(f"  ID: {task.task_id}")
            print(f"  Description: {task.description}")
            print(f"  Assigned To: {task.assigned_to}")
            print(f"  Status: {task.status}")
            print(f"  Result: {task.result}")
            print(f"  Completed At: {task.completed_at}")
            print("---")
    else:
        print("No tasks were solved.")

    print("\\nExample run finished. Check logs in app/data/examples for more details.")


if __name__ == "__main__":
    run_basic_news_room_example()
