from abc import ABC, abstractmethod
from datetime import datetime as dt
from pathlib import Path
import os 

import PySimpleGUI as sg

LOG_PATH = Path(__file__).parent.parent / 'configuration\\log.log'

COMPUTER_NAME = os.getenv('COMPUTERNAME')

class Log(ABC):
    @abstractmethod
    def _log(self, msg):
        pass

    def log_error(self, msg, debug=False):
        if debug:
            sg.Print(f'Error: {msg} ({self.__class__.__name__})',colors=('black','red'))
        print(f'Error: {msg} ({self.__class__.__name__})')
        return self._log(f'{dt.now()} - Log Error: {COMPUTER_NAME} - {msg}')

    def log_success(self, msg, debug=False):
        if debug:
            sg.Print(f'Success: {msg} ({self.__class__.__name__})',colors=('black','green'))
        print(f'Success: {msg} ({self.__class__.__name__})')
        return self._log(f'{dt.now()} - Log Success: {COMPUTER_NAME} - {msg}')

class LogFileMixin(Log):
    def _log(self, msg):
        formated_msg = f'{msg} ({self.__class__.__name__})'
        with open(LOG_PATH, 'a') as archive:
            archive.write(formated_msg)
            archive.write('\n')

if __name__ == "__main__":
    lf = LogFileMixin()

    lf.log_success('testing log success')
    lf.log_error('testing log error')

