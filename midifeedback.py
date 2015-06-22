from queue import Queue, Empty
import jack
import time
from PyQt5.QtGui import QImage, QColor


class midifeedback:
    NOTEON = 0x9
    NOTEOFF = 0x8
    MIDICTRL = 11
    NOTE_NAME = ['C', 'C#',
                 'D', 'D#',
                 'E',
                 'F', 'F#',
                 'G', 'G#',
                 'A', 'A#',
                 'B']

    GREEN = 60
    RED = 15
    AMBER = 63
    BLACK = 12

    def __init__(self):
        self.queue_out = Queue()

        self.client = jack.Client("Launchpad Midi Feedback")
        self.midi_out = self.client.midi_outports.register("output")
        self.client.set_process_callback(self.my_callback)
        self.client.activate()

    def my_callback(self, frames):
        self.midi_out.clear_buffer()
        try:
            i = 1
            while True:
                note = self.queue_out.get(block=False)
                self.midi_out.write_midi_event(i, note)
                i += 1
        except Empty:
            pass

        return jack.CALL_AGAIN

    def blackall(self):
        for pitch in range(128):
            note = ((self.NOTEON << 4) + 0, pitch, 12)
            self.queue_out.put(note)

    def closeall(self):
        self.client.deactivate()
        self.client.close()

    def onenote(self, pitchx, pitchy, color=GREEN):
        pitch = pitchx + (pitchy * 16)
        note = ((self.NOTEON << 4) + 0, pitch, color)
        self.queue_out.put(note)

    def drawImg(self, path):
        img = QImage(path)
        for x in range(img.width()):
            for y in range(img.height()):
                red, green, blue, a = QColor(img.pixel(x, y)).getRgb()
                if red > green and red > blue:
                    color = midifeedback.RED
                elif green > red and green > blue:
                    color = midifeedback.GREEN
                elif red == green and green > blue:
                    color = midifeedback.AMBER
                else:
                    color = midifeedback.BLACK
                print(
                    "r:{},g:{},b:{},color:{}".format(red, green, blue, color))
                self.onenote(x, y, color)
                time.sleep(0.03)

    def lightFancy(self):
        color = 60
        fancylist = [19, 18, 33, 50, 67, 82, 81, 36, 37, 54, 69, 86, 101, 100,
                     84, 68, 52]
        for pitch in fancylist:
            note = ((self.NOTEON << 4) + 0, pitch, color)
            self.queue_out.put(note)

    def blink(self):
        for pitch in range(128):
            note = ((self.NOTEON << 4) + 0, pitch, 60)
            self.queue_out.put(note)
            time.sleep(0.1)
            note = ((self.NOTEON << 4) + 0, pitch, 12)
            self.queue_out.put(note)
            time.sleep(0.1)

    def tetris(self):
        color = 60
        fancylist = [(2, 0), (3, 0), (4, 0), (2, -1)]
        for row in range(8):
            l = [(x, y + row) for x, y in fancylist]
            for x, y in l:
                if min(x, y) >= 0:
                    # print("x%s y%s" % (x, y))
                    self.onenote(x, y)
            time.sleep(1)
            self.blackall()


            # use:
            # import midifeedback
            # test = midifeedback.midifeedback()
            # test.lightFancy()
            # test.blackall()
            # test.closeall()
            # reload(midifeedback)
            # test.onenote(x,y)
            # test.onenote(2,2,midifeedback.midifeedback.RED)
