from queue import Queue, Empty
import jack
import time


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

    def onenote(self, pitchx, pitchy, color=60):
        pitch = pitchx + (pitchy * 16)
        note = ((self.NOTEON << 4) + 0, pitch, color)
        self.queue_out.put(note)

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


            # use:
            # import midifeedback
            # test = midifeedback.midifeedback()
            # test.lightFancy()
            # test.blackall()
            # test.closeall()
            # reload(midifeedback)
            # test.onenote(x,y)
