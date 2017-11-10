EFFECTS = {
    "miss": "MISS",
    "encumbered": "ENCUMBERED",
    "bleeding": "BLEEDING",
    "exhausted": "EXHAUSTED",
    "injured(head)": "INJURED(HEAD)",
    "injured(hand)": "INJURED(HAND)",
    "injured(off-hand)": "INJURED(OFF-HAND)",
    "injured(torso)": "INJURED(TORSO)",
    "injured(legs)": "INJURED(LEGS)",
    "wounded": "WOUNDED",
    "disarmed": "DISARMED"
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
