import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# WIDTH = largura da amostra de audio desejada em bytes
# CHUNKS = pedaços fragmentados do audio para um melhor fluxo dos dados
# RATE = Especifica a taxa desejada de 44kHz (são gerados 44kHz a partir dos sinais
# de audio analogico)
# CHANNELS = canais de audio

#Open abre uma nova transmissão de audio
stream_input = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#Open abre uma nova transmissão de audio
stream_output = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

#Escreve amostras de audio na transmissão
def play(bytes):
    stream_output.write(bytes,CHUNK)
    pass

# Le amostras de audio da transmissão  
def record():
    return stream_input.read(CHUNK, exception_on_overflow= False)



