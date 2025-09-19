class Batter:
    def __init__(self, name: str, team: str, bat_handedness: str, throw_handedness: str):
        self.name = name
        self.team = team
        self.position = "Batter"
        self.bat_handedness = bat_handedness
        self.throw_handedness = throw_handedness

        # Instead of calculating stats, construct everything from "events"
        self.batting_events = []
        self.fielding_opportunity_events = []

        # TODO: All these ratings need to be fine tuned but honestly I think that this can be done with
        # TODO: real MLB data in mind, trying to match it as closely as possible
        # TODO: Certain measurements should probably be kept constant (to match real world data), but other stuff like standard deviations, etc can be adjusted
        # Batting ratings (1-1000, MLB players are generally in the top 200 of this scale)
        self.batting_ratings = {
            # Ability to get the bat to the ball and make contact with pitches, square them up, etc
            # This is used to derive whether a batter squares up a pitch. The more movement in a pitch, the harder it is
            "Contact": 900,
            # Ability to swing at good pitches in the strike zone and avoid pitches outside of the zone
            # Even if a pitch is in the zone, if it's early in the count and isn't in a great location, a batter may not swing at it
            "Eye": 900,
            # Ability to foul off pitches. If a batter is consciously trying to foul off a pitch, they may swing slower (maybe, not sure if I want to do that)
            "Avoid Strikeouts": 900
        }

        # Empirical measurements of a hitter's swing
        self.swing_characteristics = {
            # Parameters for a skew normal distribution of swing speed
            # Mean swing speed in MPH
            "Swing Speed": 72,
            "Swing Speed StdDev": 3,    # TODO: fine tune
            # This is most commonly going to be NEGATIVE (ie left skewed)
            "Swing Speed Skew": 0,
            # Swing attack angle in degrees (normal distribution)
            "Attack Angle": 5,
            "Attack Angle StdDev": 2,   # TODO: fine tune
            # Swing attack direction (ie direction the bat is facing at time of contact) in degrees
            # This will be affected by things like timing, whether the pitch is fast or slow (ie pitcher fooling hitter),
            # etc but it is generally what the hitter is *trying* to do
            # Positive is pull side depending on what handedness a batter is batting
            "Attack Direction": 8,  # TODO: fine tune
            "Attack Direction StdDev": 20   # TODO: fine tune
        }

        # Empirical measurements of a fielder's abilities
        # For all of these, standard deviation is constant
        # TODO decide what to use for stddev
        # NOTE should I include spin difficulty on infield plays? Like balls that spin a lot are harder to field
        # NOTE Also how do I continue the trajectory of infield balls after they hit the ground? Should I just 
        # TODO: There needs to be some infielder or outfielder specific characteristics because obviously a good infielder
        # Isn't the same as a good outfielder. Do some research into what's different, especially wrt range (eg maybe one relies on acceleration more).
        self.fielding_characteristics = {
            "Reaction Time": 0.2,   # seconds, average MLB player is around 0.2 seconds
            "Speed": 28.0,   # feet per second, TODO fine tune
            "Arm Strength": 85.0,   # MPH throw speed

            # Reaction direction (where the fielder runs in the first couple seconds after the ball is hit)
            # is determined by a normal distribution with the mean being the optimal direction (based on projected landing spot)
            # (yes I know the fielder doesn't know the landing spot, but this is a simplification and it's probably valid for MLB level players)
            # and the stddev being this value in degrees
            "Reaction Direction Stddev": 10.0,    # TODO fine tune

            # 0-1, how often a fielder reacts in the wrong direction (like bruh why are you running forward on a ball hit behind you)
            "Reaction Error Frequency": 0.05,   # TODO fine tune

            # 0-1 how often a fielder makes routine catches
            # This is then adjusted based on difficulty of play based on
            # the speed the fielder is running, how far they have to extend (like a diving ball through the infield), etc
            # It will generally be a number between 0.98 TODO and 0.995 TODO for most players.
            # Small differences are heavily amplified over the course of a season and on difficult plays
            "Routine Catch Frequency": 0.99,

            # 0-1 how often a fielder makes throws that are off target
            # This can just be binary because the game chooses to not allow a fielder to
            # throw significantly faster (which would normally decrease accuracy) on difficult plays
            # which means that the lack of decrease in accuracy is canceled by the lack of increase in speed
            # This is different for infielders and outfielders. For infielders, the difficulty of the range of the play
            # increases the odds of an off target throw
            # For infielders, this also isn't the probability of an infielder throwing a
            # difficult throw (eg one that hops), but it's based on this
            "Throwing Error Frequency": 0.05,  # TODO fine tune
            # How good a first baseman is at receiving difficult throws (as a probability)
            "First Baseman Receiving Ability": 0.95,  # TODO fine tune

            # How good a catcher is at blocking pitches (as a probability)
            # This includes pitches in the dirt, pitches high, outside, etc.
            "Catcher Blocking Ability": 0.95,  # TODO fine tune

            # How good a catcher is at throwing out runners (as a probability)
            "Catcher Throwing Ability": 0.25,   # TODO fine tune

            # How good a catcher is at framing pitches
            # The way pitch calling works is that there's a sigmoid curve that determines
            # the probability of a pitch being called a strike and the "transition region" of the curve
            # is moved either closer to the plate (worse framing) or further from the plate (better framing)
            # This is measured in inches. 0 is the default just by definition (that's average).
            "Catcher Framing Ability": 0.0,   # TODO fine tune
        }
        # This is the stuff that needs to be calculated
        # self.batting_stats = {
        #     "PA": 0,
        #     "AB": 0,
        #     "H": 0,
        #     "1B": 0,
        #     "2B": 0,
        #     "3B": 0,
        #     "HR": 0,
        #     "R": 0,
        #     "RBI": 0,
        #     "BB": 0,
        #     "SO": 0,
        #     "HBP": 0,
        #     "SB": 0,
        #     "CS": 0,
        #     "PO": 0
        # }

        # self.fielding_stats = {
        #     "Opportunities": 0,
        #     ""
        # }
