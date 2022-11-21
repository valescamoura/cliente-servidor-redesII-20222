import pyaudio

CHUNK = 512
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)



def play(bytes):
    stream.write(bytes,CHUNK)
    pass

def record():
    return stream.read(CHUNK, exception_on_overflow= False)
