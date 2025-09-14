Implementation ideas:
1. Calculate where the ball either lands or hits a wall
2. Then, pass to a model the xyz coordinates, whether the ball hit a wall, velocity and angle of velocity (or just components of velocity), and hang time before hitting ground/wall, which then calculates probability of various outcomes
    - This step seems hard as fuck.... not sure the exact data even exists (esp for wall balls—does data exist on where the ball hit the wall, what height, etc?) and creating the model is probably above my ability level.
    - Also one problem with this is it doesn't allow me to take into account fielder quality, batter quality, etc. So maybe a more custom implementation for this? Not sure how to go about that
3. Before step 2, can also automatically detect home runs 