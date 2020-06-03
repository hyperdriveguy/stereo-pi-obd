import subprocess


def speak(words, speed=100):
    format_args = 'espeak -s {} "{}"'.format(speed, words)
    subprocess.Popen(format_args, shell=True)


def speak_wait(words, speed=100):
    format_args = 'espeak -s {} "{}"'.format(speed, words)
    subprocess.Popen(format_args, shell=True).wait()
