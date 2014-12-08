#!/usr/bin/python3.4


"""Tests for module 'sigproc'.
"""


import numpy as np
import scipy.io.wavfile as wavf
import matplotlib.pyplot as plt
import sys

import math
import os, os.path, shutil

from useful import CORPORA_DIR, IMAGES_SIGPROC_DIR, testplot
import sigproc


if os.path.exists(IMAGES_SIGPROC_DIR):
        shutil.rmtree(IMAGES_SIGPROC_DIR)
os.mkdir(IMAGES_SIGPROC_DIR)


#Reading signal from base and plotting
voice = ('enroll_2', 'f08', 54)
(enroll, speaker, speech) = voice
(samplerate, signal) = wavf.read('%smit/%s/%s/phrase%02d_16k.wav' % (CORPORA_DIR, enroll,
                                                                   speaker, speech))
numsamples = len(signal)
time = np.linspace(0, numsamples/samplerate, numsamples, False)
testplot(time, signal, '%s\n%d Hz' % (voice, samplerate), 't (seconds)',
         'signal[t]', 'sigproc/0-signal-%s-%s-%02d-%dHz' % (enroll, speaker, speech, samplerate))

#Pre emphasized signal with coefficient 0.97
presignal = sigproc.preemphasis(signal)
testplot(time, presignal, '%s\n%d Hz, preemph 0.97' % (voice, samplerate),
         't (seconds)', 'presignal[t]', 'sigproc/1-signal-%s-%s-%02d-%dHz-preemph0.97' %
         (enroll, speaker, speech, samplerate))

NFFT = 512
freq = np.linspace(0, samplerate/2, math.floor(NFFT/2 + 1))

#Magnitude of presignal's spectrum
magspec = sigproc.magspec(presignal, NFFT)
testplot(freq, magspec, '%s\n%d Hz, preemph 0.97, |FFT|' % (voice, samplerate),
         'f (Hz)', '|FFT[f]|', 'sigproc/2-signal-%s-%s-%02d-%dHz-preemph0.97-magspec' %
         (enroll, speaker, speech, samplerate), True)

#Squared magnitude of presignal's spectrum
powspec = sigproc.powspec(presignal, NFFT)
testplot(freq, powspec, '%s\n%d Hz, preemph 0.97, |FFT|²' % (voice, samplerate),
         'f (Hz)', '|FFT[f]|²', 'sigproc/3-signal-%s-%s-%02d-%dHz-preemph0.97-powspec' %
         (enroll, speaker, speech, samplerate), True)

#samples = sec * (samples/sec)
framelen = 0.02
framestep = 0.01

#Framing pre emphasized signal using a Hamming window
frames = sigproc.framesignal(presignal, framelen*samplerate, framestep*samplerate)
numframes = len(frames)
print('#frames = %d' % numframes)
for i in range(0, numframes, 30):
    frametime = np.linspace(i*framestep, (i*framestep + framelen), framelen*samplerate, False)
    testplot(frametime, frames[i], '%s\n%d Hz, preemph 0.97, Hamming %d' %
             (voice, samplerate, i), 't (seconds)', 'framedpresignal[t]',
             'sigproc/4-signal-%s-%s-%02d-%dHz-preemph0.97-hamming%02d' %
             (enroll, speaker, speech, samplerate, i))

#            #Magnitude spectrum
#            if 'magspec' in args:
#                magframes = sigproc.magspec(frames, NFFT)
#                magspec = np.zeros(len(magframes[0]))
#                for magframe in magframes:
#                    magspec = np.maximum(magspec, magframe)
#                testplot(freq, magspec, xlabel='frequency (Hz)', ylabel='magspec[f]', fill=True,
#                         suptitle='Magnitude of framed spectrum\n(preemph = %.2f, win = %s)' %
#                                    (preemph, winname))
#
#            #Squared magnitude spectrum
#            if 'powspec' in args:
#                powframes = sigproc.powspec(frames, NFFT)
#                powspec = np.zeros(len(powframes[0]))
#                for powframe in powframes:
#                    powspec = np.maximum(powspec, powframe)
#                testplot(freq, powspec, xlabel='frequency (Hz)', ylabel='powspec[f]', fill=True,
#                         suptitle='Squared magnitude of framed spectrum\n(preemph = %.2f, win = %s)' %
#                                    (preemph, winname))