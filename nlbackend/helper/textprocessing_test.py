import textprocessing as tp
import numpy as np
import pandas as pd

def test_empty_updatelexicon():
    assert tp.updatelexicon({}, ['Hallo','Welt', 'Das', 'Das']) == {'Hallo': 1, 'Welt': 1, 'Das': 2 }

def test_updatelexicon():
    assert tp.updatelexicon(
        {'Hallo': 1, 'Welt': 1},
        ['Hallo', 'Welt', 'wir', 'kommen', 'in', 'frieden']
    ) == {'Hallo': 2, 'Welt' : 2, 'wir':1, 'kommen': 1,'in':1,'frieden': 1}

def test_removestopwords():
    artikeltext = 'Die Welt ist kein gerechter Ort für kleine Kinder, schwache, gerechte und Starke.'
    assert tp.removestopwords(artikeltext) == ['welt', 'gerechter', 'ort', 'kleine', 'kinder', 'schwache', 'gerechte','starke']



n = tp.NewsItemProcessingFactory()
df = pd.DataFrame(n.docvectors()[0].todense())


def test_euclidieandistance():
    v1 = np.array((1, 2, 3))
    v2 = np.array((1, 2, 3))
    assert n.euclidieandistance(v1, v2) == 0

def test_getvector():
    print(df[0])

def test_rowtovector():
    print('')