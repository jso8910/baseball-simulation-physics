from objects.stadium import Stadium
import math

# All science from Alan Nathan's papers
# https://baseball.physics.illinois.edu/TrajectoryAnalysis.pdf

STEP_SIZE = 0.005

# All constant units use imperial (feet, ounces)
GRAVITY = 32.174
NOMINAL_K = 1/(8*math.pi) * 0.0767 / (5.125/16) * (9.125/12)**2     # ft^-1
NOMINAL_CIRCUMFERENCE = 9.125   # inches
NOMINAL_MASS = 5.125    # ounces
NOMINAL_PRESSURE = 1.225  # kg/m^3

class Ball:
    def __init__(self, stadium: Stadium, velocity: float, launch_angle: float, spray_angle: float, backspin: float, sidespin: float, wind_speed: float, wind_direction: float, ball_circumference: float, ball_mass: float):
        # TODO: use stadium dimensions to stop the simulation when the ball hits a wall (or goes over)
        self.stadium = stadium
        self.velocity = velocity    # MPH
        self.launch_angle = launch_angle
        self.spray_angle = spray_angle  # Positive towards right side
        self.backspin = backspin    # RPM, +ve = backspin
        self.sidespin = sidespin    # RPM, +ve = breaking towards left side
        self.wind_speed = wind_speed    # feet per second
        self.wind_direction = wind_direction
        self.ball_circumference = ball_circumference    # inches
        self.ball_mass = ball_mass  # ounces

        self.location_times: list[tuple[float, float, float, float]] = []

        self.k = NOMINAL_K * (self.ball_circumference / NOMINAL_CIRCUMFERENCE) ** 2 * (NOMINAL_MASS / self.ball_mass) * (NOMINAL_PRESSURE / NOMINAL_PRESSURE)

        # Drag coefficient adjusted from a baseline of 1000 rpm
        self.coef_drag = 0.297 + 0.0292 * math.sqrt(self.backspin ** 2 + self.sidespin ** 2) / 1000

    def get_coef_lift(self, velocity: float, omega: float) -> float:
        # Lift coefficient dependent on velocity of ball
        # S = R * omega / v
        s_constant = (self.ball_circumference / 12 / (2 * math.pi)) * omega / velocity
        return 1.120 * s_constant / (0.583 + 2.333 * s_constant)

    def calculate_locations(self):
        time = 0.0
        x = 0.0
        y = 0.0
        # NOTE: Assuming approximately 6 feet starting height
        z = 6.0

        # Converted to feet per second
        v = self.velocity * 5280 / (60*60)
        vx = v * math.cos(self.launch_angle) * math.sin(self.spray_angle)
        vy = v * math.cos(self.launch_angle) * math.cos(self.spray_angle)
        vz = v * math.sin(self.launch_angle)

        total_rpm = math.sqrt(self.backspin**2 + self.sidespin**2)
        # Omega (rad / s)
        omega = total_rpm * 2 * math.pi / 60
        if omega == 0:
            omega = 1e-6  # Avoid division by zero
        omega_backspin = self.backspin * 2 * math.pi / 60
        omega_sidespin = self.sidespin * 2 * math.pi / 60

        omega_x = omega_backspin * math.cos(self.spray_angle) - omega_sidespin * math.sin(self.launch_angle) * math.sin(self.spray_angle)
        omega_y = -omega_backspin * math.sin(self.spray_angle) - omega_sidespin * math.sin(self.launch_angle) * math.cos(self.spray_angle)
        omega_z = omega_sidespin * math.cos(self.launch_angle)

        # Simulate until ball hits the ground
        while z >= 0:
            # Update positions based on physics calculations
            time += STEP_SIZE
            x += vx * STEP_SIZE
            y += vy * STEP_SIZE
            z += vz * STEP_SIZE

            dvxdt = -self.k * self.coef_drag * v * vx + self.k * self.get_coef_lift(v, omega) * v * (omega_y * vz - omega_z * vy) / omega
            dvydt = -self.k * self.coef_drag * v * vy + self.k * self.get_coef_lift(v, omega) * v * (omega_z * vx - omega_x * vz) / omega
            dvzdt = -self.k * self.coef_drag * v * vz + self.k * self.get_coef_lift(v, omega) * v * (omega_x * vy - omega_y * vx) / omega - GRAVITY

            vx += dvxdt * STEP_SIZE
            vy += dvydt * STEP_SIZE
            vz += dvzdt * STEP_SIZE

            v = math.sqrt(vx**2 + vy**2 + vz**2)

            self.location_times.append((time, x, y, z))
