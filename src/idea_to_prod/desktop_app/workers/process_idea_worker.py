"""Worker thread for processing ideas"""

from PyQt6.QtCore import QThread, pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from idea_to_prod.agents.team import IdeaToProdTeam


class ProcessIdeaWorker(QThread):
    """Worker thread for processing ideas asynchronously"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str, int)  # message, step number
    
    def __init__(self, team: "IdeaToProdTeam", idea: str):
        super().__init__()
        self.team = team
        self.idea = idea
    
    def run(self):
        """Execute the idea processing"""
        try:
            self.progress.emit("Starting High-Level Design...", 1)
            result = self.team.process_idea(self.idea)
            
            for i in range(2, 6):
                self.progress.emit(f"Completed Stage {i-1}", i)
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
