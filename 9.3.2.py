# Warning: to use this program install module keyboard.
# You can install the module keyboard from command line
# >> pip3 install keyboard
# or use pycharm buildin installer.

import keyboard
from abc import ABC, abstractmethod
from datetime import datetime


# ─────────────────────────────────────────────
#  Interface (abstract base class) – Observer
# ─────────────────────────────────────────────
class KeyboardListener(ABC):
    """Interface for all keyboard event listeners (Observer)."""

    @abstractmethod
    def on_key_pressed(self, key: str) -> None:
        """Called every time a key is pressed."""
        pass


# ─────────────────────────────────────────────
#  Concrete Observer 1 – logs to a file
# ─────────────────────────────────────────────
class KeyFileLogger(KeyboardListener):
    """Saves every key press to a file with a timestamp."""

    def __init__(self, filename: str = "keylog.txt"):
        self._filename = filename
        # Create / clear the file on start
        with open(self._filename, "w", encoding="utf-8") as f:
            f.write(f"=== KeyFileLogger started at {datetime.now()} ===\n")

    def on_key_pressed(self, key: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {key}\n")


# ─────────────────────────────────────────────
#  Concrete Observer 2 – prints to console
# ─────────────────────────────────────────────
class KeyLogger(KeyboardListener):
    """Prints every key press to the console."""

    def on_key_pressed(self, key: str) -> None:
        print(f"[KeyLogger] Key pressed: {key}")


# ─────────────────────────────────────────────
#  Subject – KeyboardSpy
# ─────────────────────────────────────────────
class KeyboardSpy:
    """
    Captures all keyboard events and notifies registered listeners.
    Implements the Observable (Subject) role of the Observer pattern.
    """

    def __init__(self):
        self._listeners: list[KeyboardListener] = []

    # ── Observer management ──────────────────
    def add_listener(self, listener: KeyboardListener) -> None:
        """Register a new listener."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: KeyboardListener) -> None:
        """Unregister an existing listener."""
        self._listeners.remove(listener)

    # ── Notification ─────────────────────────
    def _notify(self, key: str) -> None:
        """Notify all registered listeners about a key press."""
        for listener in self._listeners:
            listener.on_key_pressed(key)

    # ── Main loop ────────────────────────────
    def main(self) -> None:
        print("KeyboardSpy started. Press Ctrl+Q to quit.")
        while True:
            try:
                key = keyboard.read_key()
                if keyboard.is_pressed("ctrl") and key == "q":
                    print("Finished!")
                    self._notify("CTRL+Q (exit)")
                    break
                self._notify(key)
            except Exception:
                break


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    spy = KeyboardSpy()

    # Register listeners
    spy.add_listener(KeyLogger())           # prints to console
    spy.add_listener(KeyFileLogger("keylog.txt"))  # saves to file

    spy.main()
