Implementation ideas:
1. Calculate where the ball either lands or hits a wall
2. Then, pass to a model the xyz coordinates, whether the ball hit a wall, velocity and angle of velocity (or just components of velocity), and hang time before hitting ground/wall, which then calculates probability of various outcomes
    - This step seems hard as fuck.... not sure the exact data even exists (esp for wall balls—does data exist on where the ball hit the wall, what height, etc?) and creating the model is probably above my ability level.
    - Also one problem with this is it doesn't allow me to take into account fielder quality, batter quality, etc. So maybe a more custom implementation for this? Not sure how to go about that
3. Before step 2, can also automatically detect home runs


# Figuring out what the outcome of a batted ball is?
Perhaps in figuring out whether something is a hit or out, I could do a simulation of running speed. I could give each outfielder the following properties:
1. Peak sprint speed
2. Acceleration (burst)
    - How should this work? Because acceleration isn't always constant. Perhaps I can transition after the first couple/few seconds away from their initial burst acceleration towards their sustained acceleration? Sustained acceleration would be calculated based on the force required to maintain the peak sprint speed (air resistance, friction, etc.... idk biomechanics lol)
3. Reaction time
4. Reaction distance standard deviation (standard deviation of direction fielder starts running in when they react)
5. Error rate
Then from this I could insert random variation and calculate whether a fielder makes it to a ball. And perhaps if a fielder is within 3 feet, they can have a slight chance of jumping/diving (defined by another rating?) to get the ball

Not sure how this would translate to infielders at all, since it's just overall VERY different to get to an infield ball, lots more skill involved in fielding the ball (vs outfield where getting to the ball is the primary difficulty), variation in hops, etc.

I really think that somehow calculating probabilities using a model of the various outcomes is the best, because it can take into account these random variation things like how the ball bounces. But idk how to take into account fielder skill, ESPECIALLY given there are multiple facets of fielder skill. Manual tweaking might be the only way. But how would I verify that a formula produces reasonable results?