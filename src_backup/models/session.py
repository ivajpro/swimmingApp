from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SwimmingSet:
    distance: int
    time: int
    stroke: str
    rest_interval: int = 0

@dataclass
class Session:
    date: datetime
    pool_length: int
    sets: List[SwimmingSet]
    notes: Optional[str] = None
    
    @property
    def total_distance(self) -> int:
        return sum(s.distance for s in self.sets)
    
    @property
    def total_time(self) -> int:
        return sum(s.time for s in self.sets)
    
    @property
    def average_pace(self) -> float:
        if self.total_distance == 0:
            return 0
        return self.total_time / (self.total_distance / 100)  # seconds per 100m

