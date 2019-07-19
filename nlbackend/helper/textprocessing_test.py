import textprocessing as tp

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


