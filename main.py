import itertools
import numpy as np
import matplotlib.pyplot as plt
import music21
from madmom.audio.chroma import DeepChromaProcessor

class ChrombigramSymbolic(object):
    def __init__(self, segment=False):
        self.chrombigram = {}
        pcs = range(12)
        for r in range(13):
            pcsets = itertools.combinations(pcs, r)
            pcsets = [frozenset(x) for x in pcsets]
            for x in pcsets:
                if segment:
                    self.chrombigram[x] = r
                else:
                    self.chrombigram[x] = 0

    def clean(self):
        for x in self.chrombigram:
            self.chrombigram[x] = 0

    def fill(self, fingerprint):
        for pc in fingerprint:
            self.chrombigram[pc] += 1

    def get_as_box_array(self):
        arr = list(self.chrombigram.values())
        arr = np.array(arr).reshape(64, -1)
        return arr


class ChrombigramAudio(object):
    def __init__(self):
        self.chrombigram = {}
        self.chrombigram_templates = {}
        pcs = range(12)
        for r in range(13):
            pcsets = itertools.combinations(pcs, r)
            pcsets = [frozenset(x) for x in pcsets]
            for x in pcsets:
                self.chrombigram_templates[x] = self.get_template(x)
                self.chrombigram[x] = 0.0

    def get_template(self, pcset):
        template = np.array([0.0] * 12)
        if pcset:
            for pc in pcset:
                template[pc] = 1.0
            template = template / np.amax(template)
        return template

    def clean(self):
        for x in self.chrombigram:
            self.chrombigram[x] = 0.0

    def fill(self, chromagram):
        for chroma in chromagram:
            chroma = np.array(chroma)
            for pcset, template in self.chrombigram_templates.items():
                dot = np.dot(chroma, template)
                if dot > 0.3:
                    self.chrombigram[pcset] += dot

    def get_as_box_array(self):
        arr = list(self.chrombigram.values())
        arr = np.array(arr).reshape(64, -1)
        return arr


def getpcs_music21(m21):
    allpcs = []
    for x in m21.chordify().flat.notes:
        pcs = []
        for n in x:
            pcs.append(n.pitch.pitchClass)
        pcs = frozenset(pcs)
        allpcs.append(pcs)
    return allpcs


if __name__ == '__main__':
    chrombigram = ChrombigramSymbolic()
    bach = music21.converter.parse('ebminor.mxl')
    bachpcs = getpcs_music21(bach)
    chrombigram.fill(bachpcs)
    box = chrombigram.get_as_box_array()
    # deepchroma = DeepChromaProcessor()
    # x = deepchroma('scale.wav')
    # chrombigram.fill(x)
    # box = chrombigram.get_as_box_array()
    plt.imshow(box, cmap='gray')
    print(chrombigram.chrombigram)
    plt.show()
