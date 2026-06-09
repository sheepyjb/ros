import math  # Python 标准数学库，用来计算距离、角度、圆周率等。
from dataclasses import dataclass  # dataclass 用来快速定义“只保存数据”的类。


@dataclass(frozen=True)
class ControllerConfig:
    """控制器参数：目标点、比例系数、速度上限和停止阈值。"""

    goal_x: float  # 目标点的 x 坐标。
    goal_y: float  # 目标点的 y 坐标。
    linear_gain: float  # 线速度比例系数：距离误差越大，前进速度越大。
    angular_gain: float  # 角速度比例系数：角度误差越大，转向速度越大。
    max_linear_speed: float  # 最大线速度，防止乌龟冲得太快。
    max_angular_speed: float  # 最大角速度，防止乌龟转得太猛。
    goal_tolerance: float  # 距离目标多近就认为已经到达。


@dataclass(frozen=True)
class TurtlePose:
    """乌龟当前位姿：位置 x/y 和朝向 theta。"""

    x: float  # 乌龟当前 x 坐标。
    y: float  # 乌龟当前 y 坐标。
    theta: float  # 乌龟当前朝向角，单位是弧度。


@dataclass(frozen=True)
class VelocityCommand:
    """控制器算出的速度命令。"""

    linear_x: float  # 前进速度，对应 geometry_msgs/Twist.linear.x。
    angular_z: float  # 旋转速度，对应 geometry_msgs/Twist.angular.z。


def normalize_angle(angle: float) -> float:
    """把角度归一化到 [-pi, pi] 附近，方便选择最短转向方向。"""

    two_pi = 2.0 * math.pi  # 一整圈的弧度值。
    while angle > math.pi:  # 如果角度大于 pi，说明可以减去一整圈。
        angle -= two_pi  # 减去一整圈后，角度回到更小的等价角。
    while angle < -math.pi:  # 如果角度小于 -pi，说明可以加上一整圈。
        angle += two_pi  # 加上一整圈后，角度回到更大的等价角。
    return angle  # 返回归一化后的角度误差。


def _clamp(value: float, limit: float) -> float:
    """把 value 限制在 [-limit, limit] 之间。"""

    return max(-limit, min(limit, value))  # 先限制上限，再限制下限。


def compute_velocity_command(
    pose: TurtlePose,
    config: ControllerConfig,
) -> VelocityCommand:
    """根据当前位姿和目标点，计算应该发布到 /turtle1/cmd_vel 的速度。"""

    dx = config.goal_x - pose.x  # 目标点和当前位置在 x 方向的差值。
    dy = config.goal_y - pose.y  # 目标点和当前位置在 y 方向的差值。
    distance_error = math.hypot(dx, dy)  # 到目标点的直线距离。
    if distance_error < config.goal_tolerance:  # 如果已经足够接近目标点。
        return VelocityCommand(linear_x=0.0, angular_z=0.0)  # 停止前进和转向。

    target_angle = math.atan2(dy, dx)  # 从当前位置指向目标点的方向角。
    angle_error = normalize_angle(target_angle - pose.theta)  # 目标方向和当前朝向的差。
    linear_x = min(config.max_linear_speed, config.linear_gain * distance_error)
    angular_z = _clamp(config.angular_gain * angle_error, config.max_angular_speed)
    return VelocityCommand(linear_x=linear_x, angular_z=angular_z)
