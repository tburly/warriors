EFFECTS = {
    "bleeding": "BLEEDING",
    "disarmed": "DISARMED",
    "encumbered": "ENCUMBERED",
    "exhausted": "EXHAUSTED",
    "injured(hand)": "INJURED(HAND)",
    "injured(head)": "INJURED(HEAD)",
    "injured(legs)": "INJURED(LEGS)",
    "injured(off-hand)": "INJURED(OFF-HAND)",
    "injured(torso)": "INJURED(TORSO)",
    "miss": "MISS",
    "wounded": "WOUNDED"
}


class Effect(object):
    """Has name"""

    def __init__(self, name):
        super(Effect, self).__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
