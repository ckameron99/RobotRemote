import deepspeech as ds
import numpy as np
import pyaudio
import time

# DeepSpeech parameters
model_file_path = 'deepspeech-0.9.3-models.pbmm'
'''https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm '''
model = ds.Model(model_file_path)

scorer_file_path = 'deepspeech-0.9.3-models.scorer'
"""https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"""
model.enableExternalScorer(scorer_file_path)

lm_alpha = 0.75
lm_beta = 1.85
model.setScorerAlphaBeta(lm_alpha, lm_beta)

beam_width = 500
model.setBeamWidth(beam_width)


def speech_recognise():
    # Create a Streaming session
    context = model.createStream()

    # Encapsulate DeepSpeech audio feeding into a callback for PyAudio
    global text_so_far
    text_so_far = ''

    def process_audio(in_data, frame_count, time_info, status):
        global text_so_far
        data16 = np.frombuffer(in_data, dtype=np.int16)
        context.feedAudioContent(data16)
        text = context.intermediateDecode()
        if text != text_so_far:
            print('Interim text = {}'.format(text))
            # The line above prints the interim text for the duration of the period.
            text_so_far = text
        return (in_data, pyaudio.paContinue)

    # PyAudio parameters-

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK_SIZE = 1024

    # Feed audio to deepspeech in a callback to PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        stream_callback=process_audio
    )

    print('Please start speaking, when done press Ctrl-C ...')
    stream.start_stream()

    time.sleep(7)  # This is how long the microphone is recording. This can be changed as required.
    stream.stop_stream()
    stream.close()
    audio.terminate()
    text = context.finishStream()
    print(text)
    return text
