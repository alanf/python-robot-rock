#!/usr/bin/env python
''' score.py
    Author: Alan Fineberg (af@cs.washington.edu)
    The Score is a living sheet music document.
    It is edited by Musician and read by a Parser to generate audio.
'''
from staff import Staff
from scoreslice import ScoreSlice
from expandinglist import ExpandingList

class Score(object):
    def __init__(self, **score_info):
        self.__dict__.update(score_info)
        self.staffs = ExpandingList(Staff)
        self.scoreslices = ScoreSlice(self.staffs)
    
if __name__ == '__main__':
    score = Score(band='Jazz')