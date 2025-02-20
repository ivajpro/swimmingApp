from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SwimmingSet:
    distance: int
    time: int
    stroke: str
    repetitions: int = 1
    rest_interval: int = 0
    description: str = ""
    
    @property
    def total_distance(self) -> int:
        return self.distance * self.repetitions
    
    @property
    def total_time(self) -> int:
        return self.time * self.repetitions

@dataclass
class Session:
    date: datetime
    pool_length: int
    sets: List[SwimmingSet]  # Fixed from List<SwimmingSet>
    notes: Optional[str] = None
    
    @property
    def total_distance(self) -> int:
        return sum(s.total_distance for s in self.sets)
    
    @property
    def total_time(self) -> int:
        return sum(s.total_time for s in self.sets)
    
    @property
    def average_pace(self) -> float:
        if self.total_distance == 0:
            return 0
        return self.total_time / (self.total_distance / 100)  # seconds per 100m

    @property
    def total_rest_time(self) -> int:
        return sum(s.rest_interval for s in self.sets)
    
    @property
    def effective_swim_time(self) -> int:
        return self.total_time - self.total_rest_time
    
    @property
    def calories_burned(self) -> float:
        # Approximate calculation based on MET values
        MET = 6.0  # Moderate swimming
        WEIGHT = 70  # Default weight in kg, could be made configurable
        hours = self.effective_swim_time / 3600
        return MET * WEIGHT * hours

