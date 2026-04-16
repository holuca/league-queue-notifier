import cv2
import mss
import numpy as np


def capture_full_screen() -> np.ndarray:
    """
    Capture the full virtual desktop and return it as a BGR image.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # all monitors combined
        screenshot = sct.grab(monitor)
        image = np.array(screenshot)

    return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)