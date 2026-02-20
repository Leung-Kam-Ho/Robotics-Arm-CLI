from robotics_arm_cli.robot_arm.robot_arm import RobotArm
from robotics_arm_cli.robot_arm.position import Cartesian, JPosition
from robotics_arm_cli.example.robot_action_node import (
    MoveJoint,
    MoveLinear,
    MoveGripper,
)
import py_trees
import argparse
import time


def move_cartesian(ra: RobotArm, x, y, z, rx, ry, rz):
    current = ra.read_cartesian_pos()
    if current is None:
        print("Error: Unable to read current cartesian position.")
        return
    target = Cartesian(
        x=current.x + x,
        y=current.y + y,
        z=current.z + z,
        rx=current.rx + rx,
        ry=current.ry + ry,
        rz=current.rz + rz,
    )
    ra.move_linear(target)
    while ra.is_moving():
        pass
    print(f"Reached target position: {target}")


def move_joint(ra: RobotArm, j1, j2, j3, j4, j5, j6):
    target = JPosition(j1, j2, j3, j4, j5, j6)
    ra.move_joint(target)
    while ra.is_moving():
        pass
    print(f"Reached target joint position: {target.__dict__}")


def position_init(ra: RobotArm):
    ra.move_joint(ra.Init_pose)
    while ra.is_moving():
        pass
    print("Reached initial position.")


def connectToRobotArm(
    ip_address: str, base_offset: int, speed: float = 0.4
) -> RobotArm:
    ra = RobotArm(host=ip_address, base_offset=base_offset)
    ra.set_speed(speed)  # set speed to value from args.speed
    print("---- Robot Arm Connection Details ---")
    print(f"Connected to robot arm at {ip_address}.")
    print(f"Current Speed: {speed} m/s")
    print(f"Current position: {ra.read_cartesian_pos()}")
    print("-----------------------------------")
    return ra


# -- Helper function for argument parsing --


def float_range(min_value, max_value):
    def checker(arg):
        try:
            f = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("must be a floating point number")
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(
                f"must be in range [{min_value} .. {max_value}]"
            )
        return f

    return checker


def main():
    parser = argparse.ArgumentParser(
        description="Run the robotics arm behavior tree example."
    )
    parser.add_argument(
        "--ip", type=str, required=True, help="IP address of the robot arm"
    )
    parser.add_argument(
        "--offset",
        type=int,
        required=True,
        help="Base offset for the robot arm in degrees",
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=["init", "move", "joint", "gripper"],
        default="init",
        help="Action to perform: init position, move (absolute cartesian), joint (abs joint angles), gripper (open/close)",
    )
    parser.add_argument(
        "--gripper-angle",
        type=int,
        choices=[0, 90],
        default=90,
        help="Gripper angle: 0 = close, 90 = open",
    )
    parser.add_argument(
        "--speed",
        type=float_range(0.1, 1.0),
        default=0.4,
        help="Speed for the robot arm (default: 0.4 m/s)",
    )
    parser.add_argument(
        "coords", nargs="*", type=float, help="Coordinates for move or joint action"
    )

    args = parser.parse_args()

    # -- input validation and processing --
    match args.action:
        case "move":
            if len(args.coords) < 6:
                parser.error("move action requires 6 values: x y z rx ry rz")
            args.x, args.y, args.z, args.rx, args.ry, args.rz = args.coords[:6]

        case "joint":
            if len(args.coords) < 6:
                parser.error("joint action requires 6 values: j1 j2 j3 j4 j5 j6")
            args.j1, args.j2, args.j3, args.j4, args.j5, args.j6 = args.coords[:6]
        case "gripper":
            pass
        case "init":
            pass
        case _:
            pass

    # -- connect to robot arm and execute action --
    root = py_trees.composites.Sequence("Main", memory=True)
    ra = connectToRobotArm(args.ip, args.offset, args.speed)
    match args.action:
        case "move":
            root.add_child(
                MoveLinear(
                    "MoveCartesian",
                    ra,
                    Cartesian(args.x, args.y, args.z, args.rx, args.ry, args.rz),
                    relative=False,
                )
            )
        case "joint":
            root.add_child(
                MoveJoint(
                    "MoveJoint",
                    ra,
                    JPosition(args.j1, args.j2, args.j3, args.j4, args.j5, args.j6),
                    relative=False,
                )
            )
        case "gripper":
            root.add_child(MoveGripper(ra, args.gripper_angle, "GripperAction"))
        case "init":
            root.add_child(MoveJoint("InitPosition", ra, ra.Init_pose, relative=False))
        case _:
            pass
    tree = py_trees.trees.BehaviourTree(root)

    while not (
        tree.root.status
        in [py_trees.common.Status.SUCCESS, py_trees.common.Status.FAILURE]
    ):
        tree.tick()
        time.sleep(0.1)  # small delay to prevent busy waiting

    print(f"Behavior tree execution completed with status: {tree.root.status}")


if __name__ == "__main__":
    main()
