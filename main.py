import itertools
import numpy as np
import matplotlib.pyplot as plt
import music21

class Chrombigram(object):
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

    def fill_sets(self, fingerprint):
        for pc in fingerprint:
            self.chrombigram[pc] += 1

    def fill_distribution(self, chroma):
        for pc in

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
    chrombigram = Chrombigram(segment=False)
    bach = music21.converter.parse('pathetique.krn')
    bachpcs = getpcs_music21(bach)
    chrombigram.fill(bachpcs)
    box = chrombigram.get_as_box_array()
    plt.imshow(box, cmap='gray')
    plt.show()
