from deepspeech import speech_recognise


def action():
    text = speech_recognise()
    lst_of_commands = ["left", "right", "up", "down"]
    for command in lst_of_commands:
        if command in text:
            print(command)