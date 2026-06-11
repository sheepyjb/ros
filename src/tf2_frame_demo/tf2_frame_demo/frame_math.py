import math  # Python 标准数学库，用来计算 sin、cos、atan2、pi 等。
from dataclasses import dataclass  # dataclass 用来定义只保存数据的小对象。


@dataclass(frozen=True)
class Quaternion:
    """平面 yaw 角对应的四元数。"""

    x: float  # 绕 x 轴旋转相关的四元数分量；本课只绕 z 轴转，所以恒为 0。
    y: float  # 绕 y 轴旋转相关的四元数分量；本课只绕 z 轴转，所以恒为 0。
    z: float  # 绕 z 轴旋转相关的四元数分量，对应平面 yaw 角。
    w: float  # 四元数的实部，和 z 分量一起表示 yaw 旋转。


@dataclass(frozen=True)
class PlanarPose:
    """平面位姿：x/y 位置和 yaw 朝向。"""

    x: float  # 在父坐标系中的 x 坐标。
    y: float  # 在父坐标系中的 y 坐标。
    yaw: float  # 在平面内绕 z 轴的朝向角，单位是弧度。


def normalize_angle(angle: float) -> float:
    """把角度归一化到 [-pi, pi] 附近。"""

    # atan2(sin(angle), cos(angle)) 会返回与 angle 等价的最短方向角。
    # 例如 3.3 rad 会被转成接近 -2.98 rad，方便 RViz 和日志阅读。
    return math.atan2(math.sin(angle), math.cos(angle))


def yaw_to_quaternion(yaw: float) -> Quaternion:
    """把平面 yaw 角转换成绕 z 轴旋转的四元数。"""

    # 四元数表达旋转时使用半角公式：
    # z = sin(yaw / 2), w = cos(yaw / 2)。
    half_yaw = yaw / 2.0
    return Quaternion(
        x=0.0,  # 没有 roll，所以 x 分量为 0。
        y=0.0,  # 没有 pitch，所以 y 分量为 0。
        z=math.sin(half_yaw),  # 平面 yaw 旋转写到 z 分量。
        w=math.cos(half_yaw),  # w 分量和 z 分量共同表示 yaw。
    )


def quaternion_to_yaw(quaternion) -> float:
    """从四元数中取出平面 yaw 角。"""

    # 这是从四元数提取 yaw 的标准公式。
    # frame_listener 用它把 TransformStamped.rotation 转成更容易看的 yaw。
    siny_cosp = 2.0 * (
        quaternion.w * quaternion.z + quaternion.x * quaternion.y
    )
    cosy_cosp = 1.0 - 2.0 * (
        quaternion.y * quaternion.y + quaternion.z * quaternion.z
    )
    return math.atan2(siny_cosp, cosy_cosp)


def circular_pose(
    time_seconds: float,
    radius: float = 1.5,
    angular_speed: float = 0.4,
) -> PlanarPose:
    """生成一个沿圆周逆时针运动的平面位姿。"""

    angle = angular_speed * time_seconds  # 当前在圆上的相位角：时间越长，角度越大。
    x = radius * math.cos(angle)  # 圆周运动的 x 坐标。
    y = radius * math.sin(angle)  # 圆周运动的 y 坐标。
    # 位置角为 angle 时，逆时针圆周运动的切线方向是 angle + pi/2。
    # 这里让 base_link 的 x 轴始终朝向运动方向。
    yaw = normalize_angle(angle + math.pi / 2.0)
    return PlanarPose(x=x, y=y, yaw=yaw)
