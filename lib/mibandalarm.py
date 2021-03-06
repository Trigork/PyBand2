import struct

# Class to represent MiBand (2 and 3) alarm format
# Has hour and minute as basic parameters to define an alarm
# Advanced parameters are enabled (if the alarm is ON/OFF)
# and repetition mask, an 8-bit array indicating which days the alarm rings
# If no repetition, this repetition mask is 128 (1000 0000)
# If repetition, single bits (from 0 to 7) are set to 1
# The less significant bit means monday
# If any of the bits from 0 to 7 are set to 1, the most significant bit should be
# set to 0. If set to 1, the alarm won't repeat

class MiBandAlarm:
    def __init__ (self, hour, minute, enabled=True, repetitionMask=128):
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.repetitionMask = repetitionMask

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def toggleDay(self, day):
        mask = (self.repetitionMask ^ (2**day))
        if mask == 0:
            mask = 128
        if mask > 128:
            mask ^= 128
        self.repetitionMask = mask

    def getRepetitionMask(self):
        return self.repetitionMask

    def getMessage(self, index):
        base = 0
        if self.enabled:
            base = 128

        mask = self.getRepetitionMask()

        return b'\x02' + struct.pack('4B', (base+index), self.hour, self.minute, mask)

    def __str__(self):
        repr = "[{0}] ".format("E" if self.enabled else "D")
        repr += "{0:02d}:{1:02d}".format(self.hour, self.minute)
        if self.getRepetitionMask() != 128:
            mask = self.getRepetitionMask()
            repr += " ({0}{1}{2}{3}{4}{5}{6})".format(
                        "MON" if mask & (2**0) else "",
                        " TUE" if mask & (2**1) else "",
                        " WED" if mask & (2**2) else "",
                        " THU" if mask & (2**3) else "",
                        " FRI" if mask & (2**4) else "",
                        " SAT" if mask & (2**5) else "",
                        " SUN" if mask & (2**6) else "")
        else:
            repr += " (SINGLE SHOT)"
        return repr
