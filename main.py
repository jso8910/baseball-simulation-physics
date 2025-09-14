import plotly.graph_objects as go
from objects.stadium import Stadium
from engine.ball_path import Ball, NOMINAL_CIRCUMFERENCE, NOMINAL_MASS
import math

def mph_to_fps(n: float) -> float:
    return n * 5280 / 3600

if __name__ == "__main__":
    launch_angle = 80
    spray_angle = 0
    exit_velo = 105
    backspin_rpm = 1000
    sidespin_rpm = 1000
    wind_speed = mph_to_fps(15)
    wind_direction = 90

    stadium = Stadium(name="Dummy", location="Nowhere", capacity=0, dimensions={})
    ball = Ball(stadium, exit_velo, math.radians(launch_angle), math.radians(spray_angle), backspin_rpm, sidespin_rpm, wind_speed, math.radians(wind_direction), NOMINAL_CIRCUMFERENCE, NOMINAL_MASS)
    ball.calculate_locations()
    print(f"Travel distance: {(ball.location_times[-1][1]**2 + ball.location_times[-1][2]**2) ** 0.5:.2f} feet")
    print(f"Hang time: {ball.location_times[-1][0]:.2f} seconds")
    print(f"Final location: ({ball.location_times[-1][1]:.2f}, {ball.location_times[-1][2]:.2f}, {ball.location_times[-1][3]:.2f})")

    xs = [t[1] for t in ball.location_times]
    ys = [t[2] for t in ball.location_times]
    zs = [t[3] for t in ball.location_times]

    fig = go.Figure(data=go.Scatter3d(x=xs, y=ys, z=zs, mode='lines+markers',
                                     line=dict(width=4, color='blue'),
                                     marker=dict(size=2)))
    fig.update_layout(scene=dict(xaxis_title='X (ft)', yaxis_title='Y (ft)', zaxis_title='Z (ft)'),
                      title="Ball trajectory (3D)")
    fig.show()
    # optional: save a standalone interactive HTML
    fig.write_html("trajectory.html")