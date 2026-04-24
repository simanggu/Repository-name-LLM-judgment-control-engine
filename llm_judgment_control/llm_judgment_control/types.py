from dataclasses import dataclass
from typing import Optional


@dataclass
class JudgmentResult:
    action: str
    model: Optional[str]
    risk_score: int
    thesis_score: int
    memory_score: int
    reason: str
    slot_carry: str
    recovery_recenter: str
