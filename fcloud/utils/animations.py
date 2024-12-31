import os
import functools
from sys import stdout
from typing import Optional

import animation as _animation
import cursor



def animation(
    title: str = "Waiting",
    animation_symbols: Optional[list] = None,
    speed: float = 0.4,
):
    if animation_symbols is None:
        animation_symbols = ["|", "/", "-", "|", "-", "\\"]

    def decorator(
        func,
    ):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if ("without_animation", True) in kwargs.items():
                kwargs.pop("without_animation")
                return func(*args, **kwargs)
            try:
                columns, _ = os.get_terminal_size()
            except OSError:
                columns = 10
            output = title + "  " + ((columns - len(title) - 15) * "." + "  ")
            stdout.write(output)
            cursor.hide()

            wait = _animation.Wait(animation_symbols, speed)
            wait.start()
            try:
                return func(*args, **kwargs)
            finally:
                cursor.show()
                wait.stop()

        return wrapper

    return decorator
