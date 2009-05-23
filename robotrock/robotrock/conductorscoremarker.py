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
    ''' The Conductor keeps her place in the score and adds musicians
        using ConductorScoreMarker. 
    '''
    def addStaff(self, instrument):
        ''' After adding a musician to the ensemble, return their staff reference. '''
        self.score.staffs.append(staff.Staff(instrument=instrument))
        return self.score.staffs[-1]
    
    def staffMeasures(self):
        ''' Return a dictionary mapping of staff -> current measure. '''
        # Must call upadte position before taking further action, to ensure
        # our location is current.
        self._updatePosition()

        result = {}
        for measure in self.score_slices.current():
            result[measure.parent] = measure

        return result

