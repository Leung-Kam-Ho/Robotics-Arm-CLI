from robotics_arm_cli.robot_arm.robot_arm import RobotArm
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run the robotics arm behavior tree example.")
    parser.add_argument("--ip", type=str, required=True, help="IP address of the robot arm")
    parser.add_argument("--offset", type=float, required=True, help="Base offset for the robot arm in degrees")
    args = parser.parse_args()
    ra = RobotArm(host=args.ip, base_offset=args.offset)
    ra.set_speed(0.4)  # set speed to 40mm/s
    print(f"Connected to robot arm at {args.ip}.")
    print(f"Current position: {ra.read_cartesian_pos()}")


if __name__ == "__main__":
    main()