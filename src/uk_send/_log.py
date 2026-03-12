import os
from typing import Any


def log(msg: Any) -> None:  # noqa: ANN401
    if os.getenv("UK_DEBUG"):
        v: str = os.getenv("UK_DEBUG")  # pyright: ignore [reportAssignmentType]
        if v.lower() in ["true", "1"]:
            print(msg)