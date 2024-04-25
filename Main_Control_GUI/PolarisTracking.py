#! /user/bin/python

"""
Example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers.
"""

import time
import six
from sksurgerynditracker.nditracker import NDITracker
import RobotControl as rbt

class Polaris():
    def __init__(self, tracker):
        self.track = False
        self.tracker = tracker
    
    def get_track_status(self):
        return self.track
    
    def set_track_status(self, value):
        self.track = value

tracker = None
track = False

def setup():
    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ['C:/Users/aaron/Desktop/LooLab/Polaris/ToolDefs/PhantomFlatUniqueSegPass2.rom']}
    tracker = NDITracker(settings_polaris)
    global camera
    camera = Polaris(tracker)


def start():
    print("Starting Tracking")
    camera.tracker.start_tracking()
    camera.set_track_status(True)
    record()
    
def record():
    track = camera.get_track_status()
    while track:
        six.print_(camera.tracker.get_frame())
        time.sleep(0.300333)
        move_status = rbt.get_move_status()
        print("MOVE_STATUS: ", move_status)
        if move_status:
            camera.set_track_status(False)
            track = camera.get_track_status()
    stop()

def stop():
    print("Stopping tracking")
    camera.tracker.stop_tracking()
    camera.tracker.close()




def run():
    """Demonstration program

    Example showing how to initialise, configure, and communicate
    with NDI Polaris, Vega, and Aurora trackers.
    Configuration is by python dictionaries, edit as necessary.

    Dictionaries for other systems:

    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ["../data/8700339.rom"]}

    settings_aurora = {
        "tracker type": "aurora",
        "ports to probe": 2,
        "verbose": True,
    }

    settings_dummy = {"tracker type": "dummy",}

    """

    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ['C:/Users/aaron/Desktop/LooLab/Polaris/ToolDefs/PhantomFlatUniqueSegPass2.rom']}
    tracker = NDITracker(settings_polaris)

    tracker.start_tracking()

    #six.print_(tracker.get_tool_descriptions())
    for _ in range(20):
        print('bruh')
        six.print_(tracker.get_frame())
        time.sleep(0.300333)

    tracker.stop_tracking()
    tracker.close()

if __name__ == "__main__":
    run()