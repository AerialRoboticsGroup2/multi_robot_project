#!/usr/bin/env python3

class MissionManager:

    def __init__(self):
        self.mode = 'FORMATION'

    def switch_mode(self, condition):

        if condition == 'coverage':
            self.mode = 'COVERAGE'

        elif condition == 'danger':
            self.mode = 'AVOIDANCE'

        else:
            self.mode = 'FORMATION'

        return self.mode
