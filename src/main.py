#For modules
import logging.handlers
import os
import sys
#For async functionalities
import asyncio
from PyQt5.QtWidgets import QApplication
import qasync
#Classes for Praximedes tools
from Praximedes import Praximedes
#For Logging
import traceback, logging
#For ML
import re

def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(run_prax())

#Function to handle commands
async def run_prax(action = None):
    pass