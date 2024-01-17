import os
import matplotlib.pyplot as plt

#for loading and visualizing audio files
import librosa
import librosa.display
import scipy
import numpy
import time



x, sr = librosa.load('sounds/supraventricular_tachycardia.mp3')
total = 0
X, freq, t, im = plt.specgram(x, Fs=11025)
output = []
buffer = {}
for i in range(0, numpy.shape(X)[0] + 1):
    buffer[i] = 0
for i in range(0, numpy.shape(X)[1]):
    buf = []
    for j in range(0, numpy.shape(X)[0]):
        number = X[j][i] * 110250
        if abs((t[i] / 2) % (1/10)) < 0.00581:
            total += 1
            number += buffer[j]
            number /= 150
            buffer[j] = 0
            if number < 1:
                number = (1 - pow(2, -10 * number)) * 50
            buf.append(str(round(number, 2)))
        else:
            buffer[j] += number
    if buf != []:
        output.append(','.join(buf))
print(total, len(output))
time.sleep(3)
output = ';'.join(output)
file = open('D:/level_1_wave.txt', 'w')
file.write(output)
file.close()
print('done')
