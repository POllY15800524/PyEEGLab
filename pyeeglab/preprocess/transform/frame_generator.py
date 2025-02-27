import json
import logging

from math import floor
from typing import List

import pandas as pd

from ...pipeline import Preprocessor


class StaticWindow(Preprocessor):

    def __init__(self, frames: int, length: float) -> None:
        super().__init__()
        self.frames = frames
        self.length = length
        logging.debug('Create static frames (%d of %d seconds each) generator', frames, length)

    def to_json(self) -> str:
        out = {
            self.__class__.__name__ : {
                'frames': self.frames,
                'length': self.length
            }
        }
        out = json.dumps(out)
        return out

    def run(self, data: pd.DataFrame, **kwargs) -> List[pd.DataFrame]:
        step = floor(self.length * kwargs['lowest_frequency'])
        if (step * self.frames > len(data)):
            raise RuntimeError('Error while creating static frames: not enough data.')
        return [data[t:t+step] for t in range(0, step * self.frames, step)]


class StaticWindowOverlap(Preprocessor):

    def __init__(self, frames: int, length: float, overlap: float) -> None:
        super().__init__()
        self.frames = frames
        self.length = length
        self.overlap = overlap
        logging.debug('Create static frames (%d of %d seconds each with %.2f overlap) generator', frames, length, overlap)

    def to_json(self) -> str:
        out = {
            self.__class__.__name__ : {
                'frames': self.frames,
                'length': self.length,
                'overlap': self.overlap
            }
        }
        out = json.dumps(out)
        return out

    def run(self, data: pd.DataFrame, **kwargs) -> List[pd.DataFrame]:
        step = floor(self.length * kwargs['lowest_frequency'])
        if (step * self.frames * (1 - self.overlap) > len(data)):
            raise RuntimeError('Error while creating static frames: not enough data.')
        return [data[t:t+step] for t in range(0, floor(step * self.frames * (1 - self.overlap)), floor(step * (1 - self.overlap)))]


class DynamicWindow(Preprocessor):

    def __init__(self, frames: int) -> None:
        super().__init__()
        self.frames = frames
        logging.debug('Create dynamic frames (%d) generator', frames)

    def to_json(self) -> str:
        out = {
            self.__class__.__name__ : {
                'frames': self.frames
            }
        }
        out = json.dumps(out)
        return out

    def run(self, data: pd.DataFrame, **kwargs) -> List[pd.DataFrame]:
        step = len(data)
        if self.frames > 1:
            step = floor(step/self.frames)
        return [data[t:t+step] for t in range(0, len(data) - step + 1, step)]


class DynamicWindowOverlap(Preprocessor):

    def __init__(self, frames: int, overlap: float) -> None:
        super().__init__()
        self.frames = frames
        self.overlap = overlap
        logging.debug('Create dynamic frames (%d with %.2f overlap) generator', frames, overlap)

    def to_json(self) -> str:
        out = {
            self.__class__.__name__ : {
                'frames': self.frames,
                'overlap': self.overlap
            }
        }
        out = json.dumps(out)
        return out

    def run(self, data: pd.DataFrame, **kwargs) -> List[pd.DataFrame]:
        step = len(data)
        if self.frames > 1:
            step = floor(step/self.frames)
        return [data[t:t+step] for t in range(0, len(data) - step + 1, floor(step * (1 - self.overlap)))]
