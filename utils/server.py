from threading import Thread, Event
from httpx import get
from os import getenv
from dotenv import load_dotenv
from logging import error


def set_api(api_key: str, dev: bool = False) -> bool:
    """
    If dev is False, then the API key is stored in the API_URL environment variable.
    If dev is True, then the API key is stored in the API_URL_DEV environment variable.
    """

    if api_key is None or api_key == "":
        raise ValueError("API key cannot be None or empty")
    with open(".env", "w") as file:
        if dev:
            file.write(f"API_URL_DEV={api_key}")
        else:
            file.write(f"API_URL={api_key}")
    return True


def run_check_server_periodically():
    """
    Run the checkServer function periodically in a separate thread.

    The checkServer function will be called every 3 minutes.
    If any exception occurs, the error will be logged.
    The thread will be a daemon thread, so it will exit when the main program exits.
    """

    def check_server_task():
        while True:
            try:
                checkServer(verbose=False)
            except Exception as e:
                error(f"Error during server check: {e}", exc_info=True)
            Event().wait(180)  # Wait for 3 minutes (180 seconds)

    thread: Thread = Thread(target=check_server_task, daemon=True)
    thread.start()


def checkServer(verbose=True) -> bool:
    api :str = get_Api()
    try:
        req = get(api + "/connected", timeout=60)
        if req.status_code == 200:
            if verbose:
                print("CONNECTED")
            return True
        else:
            if verbose:
                print("NOT CONNECTED")
            return False
    except Exception:
        if verbose:
            print("NOT CONNECTED")
        return False


def get_Api(testing: bool = False) -> str:
    """Returns the API URL for the server"""
    load_dotenv()
    if testing:
        return getenv("API_URL_TEST")
    return getenv("API_URL")
