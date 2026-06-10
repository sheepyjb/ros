import math


def validate_goal_coordinates(x: float, y: float) -> tuple[bool, str]:
    """Validate coordinates received by the SetGoal service."""

    if not math.isfinite(x) or not math.isfinite(y):
        return False, "目标坐标必须是有限数字。"

    return True, f"目标点已更新为 ({x:.2f}, {y:.2f})。"
