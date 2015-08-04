import spherogram, backtrack, snappy

links = snappy.HTLinkExteriors

def test_one(steps=100):
    M = links.random()
    L = M.link()
    L = L.backtrack(steps)
    print M.name(), L
    L.simplify()
    matches = [N.name() for N in links.siblings(L.exterior())]
    assert M.name() in matches


while True:
    test_one()
