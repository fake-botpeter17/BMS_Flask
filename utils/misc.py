from threading import Event, Thread
from pathlib import Path
from json import load, dump
import qrcode
import base64
from io import BytesIO


def run_periodically(func, interval=30 * 60, *args, **kwargs):
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


def read_json_file(path: Path) -> dict:
    """
    Reads a JSON file from the given path and returns the corresponding Python object.

    Args:
        path (Path): The path to the JSON file.

    Returns:
        dict: The Python object representing the JSON data.
    """
    with open(path) as p:
        return load(p)


def write_json_file(path: Path, data, indent = 4):
    """
    Writes a Python object as JSON to the given path.

    Args:
        path (Path): The path to the file where the JSON will be written.
        data: The Python object to be written as JSON.
        *args: Additional arguments to pass to the json.dump function.
    """
    with open(path, 'w') as f:
        dump(data, fp=f, indent = indent)

def generate_qr_base64(data):
    qr = qrcode.make(data)

    # Save to a bytes buffer
    buffered = BytesIO()
    qr.save(buffered, format="PNG")

    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_str