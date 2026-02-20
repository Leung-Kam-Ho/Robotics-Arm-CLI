from robotics_arm_cli.robot_arm.robot_arm import RobotArm
import argparse


def connectToRobotArm(ip_address: str, base_offset: int, speed: float = 0.4) -> RobotArm:
    ra = RobotArm(host=ip_address, base_offset=base_offset)
    ra.set_speed(speed)  # set speed to value from args.speed
    print("---- Robot Arm Connection Details ---")
    print(f"Connected to robot arm at {ip_address}.")
    print(f"Current Speed: {speed} m/s")
    print(f"Current position: {ra.read_cartesian_pos()}")
    return ra


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
    parser = argparse.ArgumentParser(description="Run the robotics arm behavior tree example.")
    parser.add_argument("--ip", type=str, required=True, help="IP address of the robot arm")
    parser.add_argument("--offset", type=int, required=True, help="Base offset for the robot arm in degrees")
    parser.add_argument("--speed", type=float_range(0.1, 1.0), default=0.4, help="Speed for the robot arm (default: 0.4 m/s)")
    args = parser.parse_args()
    ra = connectToRobotArm(args.ip, args.offset, args.speed)


if __name__ == "__main__":
    main()