from math import *
import sys

class GCodeContext:
    def __init__(self, xy_feedrate, start_delay, stop_delay, x_home, y_home, register_pen, num_pages, continuous, file):
      self.xy_feedrate = xy_feedrate
      self.start_delay = start_delay
      self.stop_delay = stop_delay
      self.x_home = x_home
      self.y_home = y_home
      self.register_pen = register_pen
      self.num_pages = num_pages
      self.continuous = continuous
      self.file = file
      
      self.drawing = False
      self.last = None

      self.preamble = [
        "(Scribbled version of %s @ %.2f)" % (self.file, self.xy_feedrate),
        "( %s )" % " ".join(sys.argv),
        "G21 (metric ftw)",
        "G90 (absolute mode)",
        "G92 X%.2f Y%.2f Z0.00 (you are here)" % (self.x_home, self.y_home),
	"M5",
        "(laser off)"
      ]

      self.postscript = [
				"(end of print job)",
				"M5",
                                "(laser off)",
				"G4 P%d" % (self.stop_delay),
                                "(wait %dms)" % (self.stop_delay),
				"G1 X0 Y0 F%0.2F" % self.xy_feedrate,
				"G1 X%0.2F Y%0.2F F%0.2F (go home)" % (self.x_home, self.y_home, self.xy_feedrate)
      ]

      self.registration = [
        "M5",
        "(laser off)",
        "G4 P%d (wait %dms)" % (self.start_delay, self.start_delay),
        "M5",
        "(laser off)",
        "G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay),
        "M18 (disengage drives)",
        "M01 (Was registration test successful?)",
        "M17 (engage drives if YES, and continue)"
      ]

      self.sheet_header = [
        "(start of sheet header)",
        "G92 X%.2f Y%.2f Z0.00 (you are here)" % (self.x_home, self.y_home)
      ]
      if self.register_pen == 'true':
        self.sheet_header.extend(self.registration)
      self.sheet_header.append("(end of sheet header)")

      self.sheet_footer = [
        "(Start of sheet footer.)",
        "M5",
        "(laser off)",
        "G4 P%d" % (self.stop_delay),
        "(wait %dms)" % (self.stop_delay),
        "G0 X%0.2f Y%0.2f F%0.2f" % (self.x_home, self.y_home, self.xy_feedrate),
        "M01 (Have you retrieved the print?)",
        "(machine halts until 'okay')",
        "G4 P%d" % (self.start_delay),
        "(wait %dms)" % (self.start_delay),
        "(End of sheet footer)"
      ]

      self.loop_forever = [ "M30 (Plot again?)" ]

      self.codes = []

    def generate(self):
      if self.continuous == 'true':
        self.num_pages = 1

      codesets = [self.preamble]
      if (self.continuous == 'true' or self.num_pages > 1):
        codesets.append(self.sheet_header)
      elif self.register_pen == 'true':
        codesets.append(self.registration)
      codesets.append(self.codes)
      if (self.continuous == 'true' or self.num_pages > 1):
        codesets.append(self.sheet_footer)

      if self.continuous == 'true':
        codesets.append(self.loop_forever)
        for codeset in codesets:
          for line in codeset:
            print line
      else:
        for p in range(0,self.num_pages):
          for codeset in codesets:
            for line in codeset:
              print line
          for line in self.postscript:
            print line

    def start(self):
      self.codes.append("M3")
      self.codes.append("(laser on)")
      self.drawing = True

    def stop(self):
      self.codes.append("M5")
      self.codes.append("(laser off)")
      self.codes.append("G4 P%d" % (self.stop_delay))
      self.codes.append("(wait %dms)" % (self.stop_delay))
      self.drawing = False

    def go_to_point(self, x, y, stop=False):
      if self.last == (x,y):
        return
      if stop:
        return
      else:
        if self.drawing: 
            self.codes.append("M5")
            self.codes.append("(laser off)")
            self.codes.append("G4 P%d" % (self.stop_delay))
            self.codes.append("(wait %dms)" % (self.stop_delay))
            self.drawing = False
        self.codes.append("G1 X%.2f Y%.2f F%.2f" % (x,y, self.xy_feedrate))
      self.last = (x,y)
	
    def draw_to_point(self, x, y, stop=False):
      if self.last == (x,y):
          return
      if stop:
        return
      else:
        if self.drawing == False:
            self.codes.append("M3")
            self.codes.append("(laser on)")
            self.codes.append("G4 P%d" % (self.start_delay))
            self.codes.append("(wait %dms)" % (self.start_delay))
            self.drawing = True
        self.codes.append("G1 X%0.2f Y%0.2f F%0.2f" % (x,y, self.xy_feedrate))
      self.last = (x,y)
