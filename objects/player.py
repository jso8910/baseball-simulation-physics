class Player:
    # Superclass for the batter and pitcher types
    def __init__(self, name: str, team: str, bat_handedness: str = None, throw_handedness: str = None):
        self.name = name
        self.team = team
        self.position = None
        self.bat_handedness = bat_handedness
        self.throw_handedness = throw_handedness