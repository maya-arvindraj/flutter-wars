from dataclasses import dataclass


@dataclass
class Principal:
    user_id: int
    team_id: int
    role: str