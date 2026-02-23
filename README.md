# Robotics Arm CLI

A CLI tool for controlling robotics arms using behavior trees (py-trees). The codebase provides a Python interface to communicate with robot arms via TCP sockets.

## Features

- **TCP Communication**: Connect to robot arms over TCP sockets
- **Motion Control**: Joint movement, linear movement, relative moves
- **Position Types**: Support for both Cartesian and Joint positions
- **IO Control**: Digital input/output control
- **Gripper Control**: Robotiq gripper support
- **Behavior Tree Integration**: Use py-trees for complex automation sequences
- **CLI Interface**: Command-line interface for quick actions

## Installation

```bash
# Install the package
uv sync
uv tool install -e .
```

## Usage

### CLI

The `rac` command provides a command-line interface:

```bash
# Initialize robot arm to home position
rac 192.168.1.1 init

# Move to absolute Cartesian position
rac 192.168.1.1 move 100 200 300 0 0 0

# Move to absolute joint positions
rac 192.168.1.1 joint 0 -40 -130 0 -90 0

# Control gripper (0 = close, 90 = open)
rac 192.168.1.1 gripper --gripper-angle 90

# Set speed
rac 192.168.1.1 init --speed 0.5
```

### Python API

```python
from robotics_arm_cli.robot_arm.robot_arm import RobotArm
from robotics_arm_cli.robot_arm.position import Cartesian, JPosition

# Connect to robot arm
ra = RobotArm(host="192.168.1.1", base_offset=0)

# Power on and enable servo
ra.power_on()
ra.start_master()
ra.servo_on()

# Move to joint position
ra.move_joint(JPosition(0, -40, -130, 0, -90, 0))

# Move to Cartesian position
ra.move_linear(Cartesian(100, 200, 300, 0, 0, 0))

# Control gripper
ra.move_gripper(90)  # Open
ra.move_gripper(0)   # Close

# Read positions
joint_pos = ra.read_joint_pos()
cartesian_pos = ra.read_cartesian_pos()
```

### Behavior Trees

Use py-trees for complex automation:

```python
from robotics_arm_cli.robot_arm.robot_arm import RobotArm
from robotics_arm_cli.robot_arm.position import Cartesian, JPosition
from robotics_arm_cli.example.robot_action_node import MoveJoint, MoveLinear, MoveGripper
import py_trees

ra = RobotArm(host="192.168.1.1")

# Create behavior tree
root = py_trees.composites.Sequence("Main", memory=True)
root.add_child(MoveJoint("MoveHome", ra, ra.Init_pose, relative=False))
root.add_child(MoveGripper(ra, 90, "OpenGripper"))
root.add_child(MoveLinear("MoveDown", ra, Cartesian(0, 0, -100, 0, 0, 0), relative=True))
root.add_child(MoveGripper(ra, 0, "CloseGripper"))

tree = py_trees.trees.BehaviourTree(root)

# Execute
while tree.root.status not in [py_trees.common.Status.SUCCESS, py_trees.common.Status.FAILURE]:
    tree.tick()
```

## Project Structure

```
src/robotics_arm_cli/
├── __init__.py           # Package entry point
├── app.py                # CLI application entry point
├── robot_arm/
│   ├── robot_arm.py      # Main RobotArm class
│   ├── tcp.py            # TCP socket communication
│   ├── position.py       # Position classes (Cartesian, JPosition)
│   └── ra_error.py       # Custom exceptions
└── example/
    ├── robot_action_node.py    # Behavior tree nodes
    ├── Checkerboard_Test.py    # Example usage
    └── Checkerboard_Test_Twin.py
```

## Commands Reference

### Core System Control

| Method | Description |
|--------|-------------|
| `power_on()` | Enable robot power |
| `power_off()` | Disable robot power |
| `start_master()` | Start master controller |
| `close_master()` | Close master controller |
| `servo_on()` | Enable servo motors |
| `servo_off()` | Disable servo motors |
| `stop()` | Stop all motion |
| `reset()` | Reset robot |

### Motion Control

| Method | Description |
|--------|-------------|
| `move_joint(jPos)` | Move to joint position |
| `move_linear(cartesian)` | Linear move to Cartesian position |
| `move_home()` | Move to home position |
| `move_relative_joint(...)` | Relative joint move |
| `move_relative_linear(...)` | Relative linear move |
| `set_speed(speed)` | Set motion speed (0.1-1.0) |
| `is_moving()` | Check if robot is moving |

### Position Reading

| Method | Description |
|--------|-------------|
| `read_joint_pos()` | Read current joint positions |
| `read_cartesian_pos()` | Read current Cartesian position |
| `read_state()` | Read robot state |

### IO Control

| Method | Description |
|--------|-------------|
| `set_output_io(index, state)` | Set digital output |
| `read_input_io(index)` | Read digital input |
| `read_output_io(index)` | Read digital output |

### Gripper Control

| Method | Description |
|--------|-------------|
| `move_gripper(position)` | Move gripper (0-140) |
| `read_gripper_pos()` | Read gripper position |
| `reset_gripper()` | Reset gripper |
| `is_gripper_moving()` | Check gripper status |

## Running Examples

```bash
uv run python src/robotics_arm_cli/example/Checkerboard_Test.py
uv run python src/robotics_arm_cli/example/Checkerboard_Test_Twin.py
```

## Development

```bash
# Type checking
uv run mypy src/robotics_arm_cli

# Linting
uv run ruff check src/robotics_arm_cli

# Format code
uv run ruff format src/robotics_arm_cli

# Run all checks
uv run mypy src/robotics_arm_cli && uv run ruff check src/robotics_arm_cli
```
