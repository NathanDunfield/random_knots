import spherogram
from spherogram.links.links import Link

def backtrack(self, steps=10):
    import backtrackfunctions
    return spherogram.links.links.Link(backtrackfunctions.backtrack(self,num_steps = steps))

spherogram.links.links.Link.backtrack = backtrack
