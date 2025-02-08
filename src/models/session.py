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
    sets: List<SwimmingSet> # type: ignore
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

