"""Define a Timer class that is used to measure the execution time of queries."""

import time


class Timer:
    """Represent a Timer."""

    def __init__(self):
        """Initialise a Timer and start the clock."""
        self.start_time = self.get_current_time()

    @staticmethod
    def get_current_time():
        """Get the current time to start the Timer."""
        return time.time()

    def get_elapsed_time(self):
        """Get the elapsed time from when this object was created."""
        return time.time() - self.start_time
