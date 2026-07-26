# models/task.py

from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    project: str
    done: bool