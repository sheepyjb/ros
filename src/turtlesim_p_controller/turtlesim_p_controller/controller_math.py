import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ControllerConfig:
    goal_x: float
    goal_y: float
    linear_gain: float
    angular_gain: float
    max_linear_speed: float
    max_angular_speed: float
    goal_tolerance: float


@dataclass(frozen=True)
class TurtlePose:
    x: float
    y: float
    theta: float


@dataclass(frozen=True)
class VelocityCommand:
    linear_x: float
    angular_z: float


def normalize_angle(angle: float) -> float:
    two_pi = 2.0 * math.pi
    while angle > math.pi:
        angle -= two_pi
    while angle < -math.pi:
        angle += two_pi
    return angle


def _clamp(value: float, limit: float) -> float:
    return max(-limit, min(limit, value))


def compute_velocity_command(
    pose: TurtlePose,
    config: ControllerConfig,
) -> VelocityCommand:
    dx = config.goal_x - pose.x
    dy = config.goal_y - pose.y
    distance_error = math.hypot(dx, dy)
    if distance_error < config.goal_tolerance:
        return VelocityCommand(linear_x=0.0, angular_z=0.0)

    target_angle = math.atan2(dy, dx)
    angle_error = normalize_angle(target_angle - pose.theta)
    linear_x = min(config.max_linear_speed, config.linear_gain * distance_error)
    angular_z = _clamp(config.angular_gain * angle_error, config.max_angular_speed)
    return VelocityCommand(linear_x=linear_x, angular_z=angular_z)
