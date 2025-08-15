from threading import Event, Thread


def run_periodically(func, interval=30*60, *args, **kwargs):
    """
    Runs a function in a separate thread every interval seconds.

    Args:
        func: Function to be run periodically
        interval: Number of seconds to wait between each run. Default is 30 minutes.
        *args: Arguments to be passed to the function
        **kwargs: Keyword arguments to be passed to the function

    Returns:
        stop_event: An Event that can be used to stop the thread
        thread: The thread running the function
    """
    stop_event = Event()

    def wrapper():
        while not stop_event.is_set():
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error in periodic function: {e}")
            stop_event.wait(interval)  # wait with ability to stop

    thread = Thread(target=wrapper, daemon=True)
    thread.start()
    return stop_event, thread