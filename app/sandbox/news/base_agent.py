"""
Base Agent class to replace Agno import until proper Agno framework is available
"""

class Agent:
    """Base agent class for news retrieval system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def run(self, *args, **kwargs):
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement the run method")