#!/usr/bin/env python
# encoding: utf-8
"""
conductorscoremarker.py

Created by Alan Fineberg on 2009-05-19.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import basescoremarker
import staff

class ConductorScoreMarker(basescoremarker.BaseScoreMarker):
    def addStaff(self, instrument):
        self.score.staffs.append(staff.Staff(instrument=instrument))
        return self.score.staffs[-1]
    
    def staffMeasures(self):
        self._updatePosition()

        result = {}
        for measure in self.score_slices.current():
            result[measure.parent] = measure

        return result

