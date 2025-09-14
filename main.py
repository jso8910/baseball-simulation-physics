from objects.stadium import Stadium
from engine.ball_path import Ball, NOMINAL_CIRCUMFERENCE, NOMINAL_MASS
import math

if __name__ == "__main__":
    launch_angle = 28
    spray_angle = 0
    exit_velo = 105
    backspin_rpm = 1000
    sidespin_rpm = 00
    wind_speed = 0
    wind_direction = 0

    stadium = Stadium(name="Dummy", location="Nowhere", capacity=0, dimensions={})
    ball = Ball(stadium, exit_velo, math.radians(launch_angle), math.radians(spray_angle), backspin_rpm, sidespin_rpm, wind_speed, math.radians(wind_direction), NOMINAL_CIRCUMFERENCE, NOMINAL_MASS)
    ball.calculate_locations()
    print(f"Travel distance: {(ball.location_times[-1][1]**2 + ball.location_times[-1][2]**2) ** 0.5:.2f} feet")
    print(f"Hang time: {ball.location_times[-1][0]:.2f} seconds")
    print(f"Final location: ({ball.location_times[-1][1]:.2f}, {ball.location_times[-1][2]:.2f}, {ball.location_times[-1][3]:.2f})")