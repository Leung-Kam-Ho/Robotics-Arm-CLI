# RAC CLI Skill

This skill provides detailed guidance on using the rac CLI tool to control robotic arms. It includes coordinate definitions, working ranges, setup instructions, and practical examples.

## Coordinate System

| Axis | Direction |
|------|-----------|
| +X | Forward |
| +Y | Right |
| +Z | Down |

### Working Range

| Axis | Range |
|------|-------|
| X | -535mm to +535mm |
| Y | -410mm to +410mm |
| Z | -50mm to 30mm |

## Robot Arms

| Arm | IP Address | Offset |
|-----|------------|--------|
| Arm 1 | 192.168.1.49 | -30 (required) |
| Arm 2 | 192.168.1.64 | 0 (default) |

## Usage

```bash
rac <ip_address> <action> [options]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `ip` | IP address of the robot arm (required) |
| `action` | Action to perform: `init`, `move`, `joint`, `gripper` (default: `init`) |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--offset` | int | 0 | Base offset for the robot arm in degrees |
| `--gripper-angle` | int | 90 | Gripper angle: 0 = close, 90 = open |
| `--speed` | float | 0.4 | Speed for the robot arm (range: 0.1 - 1.0 m/s) |
| `--coords` | float[] | - | Coordinates for move or joint action (6 values) |

## Examples

### Initialize robot arms to home position
```bash
rac 192.168.1.49 init --offset -30   # Arm 1 (offset required)
rac 192.168.1.64 init                # Arm 2
```

### Move to absolute cartesian position
```bash
rac 192.168.1.49 move --offset -30 --coords 100 0 200 0 90 0
rac 192.168.1.64 move --coords 100 0 200 0 90 0
```
Values: `x y z rx ry rz`

### Move to absolute joint positions
```bash
rac 192.168.1.49 joint --offset -30 --coords 0 0 0 0 0 0
rac 192.168.1.64 joint --coords 0 0 0 0 0 0
```
Values: `j1 j2 j3 j4 j5 j6` (in degrees)

### Control gripper
```bash
rac 192.168.1.49 gripper --offset -30 --gripper-angle 90  # Open
rac 192.168.1.49 gripper --offset -30 --gripper-angle 0    # Close
rac 192.168.1.64 gripper --gripper-angle 90                # Open
rac 192.168.1.64 gripper --gripper-angle 0                 # Close
```

### With custom speed
```bash
rac 192.168.1.49 move --offset -30 --speed 0.8 --coords 100 50 200 0 45 90
rac 192.168.1.64 move --speed 0.8 --coords 100 50 200 0 45 90
```
