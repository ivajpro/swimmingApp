from dataclasses import dataclass
from typing import List, Optional

from swimmingApp.src_backup.models.session import SwimmingSet

@dataclass
class ValidationError:
    field: str
    message: str

class Validator:
    @staticmethod
    def validate_swimming_set(swimming_set: 'SwimmingSet') -> List[ValidationError]:
        errors = []
        if swimming_set.distance <= 0:
            errors.append(ValidationError("distance", "Distance must be positive"))
        if swimming_set.time < 0:
            errors.append(ValidationError("time", "Time cannot be negative"))
        if swimming_set.repetitions <= 0:
            errors.append(ValidationError("repetitions", "Repetitions must be positive"))
        return errors