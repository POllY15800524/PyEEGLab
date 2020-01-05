import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyeeglab

PATH = './tests/samples/tuh_eeg_abnormal/v2.0.0/edf'

def test_index():
    pyeeglab.TUHEEGAbnormalLoader(PATH)

def test_loader():
    loader = pyeeglab.TUHEEGAbnormalLoader(PATH)
    print(loader.get_dataset())
    print(loader.get_dataset_text())
    print(loader.get_channelset())
    print(loader.get_lowest_frequency())

def test_dataset():
    dataset = pyeeglab.TUHEEGAbnormalDataset(PATH, frames=8)
    dataset.load('graphs', 0.7, 25, 75, True)

def test_text_miner():
    loader = pyeeglab.TUHEEGAbnormalLoader(PATH)
    text = loader.get_dataset_text()
    miner = pyeeglab.TextMiner(text)
    print(miner.get_dataset())