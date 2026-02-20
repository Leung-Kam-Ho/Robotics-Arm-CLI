---
name: robotics-arm-control
description: Control 6-DOF robotic arms using the rac CLI, including coordinate system, working ranges, required offsets, and safe usage examples.
compatibility: Requires network access to robot arm IPs on the 192.168.1.x subnet; rac CLI must be installed and in PATH.
---

# RAC Robotic Arm Control Skill

Use this skill to **control** 6‑DOF robotic arms via the `rac` CLI.  
It defines the coordinate system, safe working ranges, arm configurations, and recommended command patterns for initialization, motion, and gripper control.

## Coordinate System

All cartesian coordinates and poses are expressed in millimetres and degrees in a right‑handed base frame.

| Axis | Direction |
|------|-----------|
| +X   | Forward   |
| +Y   | Right     |
| +Z   | Down      |

Pose values for `move` actions follow:

- Position: `x y z` in millimetres.
- Orientation: `rx ry rz` in degrees (rotation about X, Y, Z, respectively).

## Working Range (Recommended)

Commands should keep the tool center point (TCP) within the following cartesian bounds unless you are certain the hardware can safely exceed them:

| Axis | Range            |
|------|------------------|
| X    | -535 mm to +535 mm |
| Y    | -410 mm to +410 mm |
| Z    | -50 mm to +30 mm   |

If in doubt, start with smaller moves near the home position and gradually extend the workspace.

## Robot Arm Configuration

Each arm is addressed by IP and may require a base joint offset.

| Arm   | IP Address   | Offset (deg) | Notes                    |
|-------|--------------|--------------|--------------------------|
| Arm 1 | 192.168.1.49 | -30          | Offset required for base |
| Arm 2 | 192.168.1.64 | 0            | Default (no extra offset)|

- Apply `--offset -30` whenever controlling Arm 1.
- Omit `--offset` or use `--offset 0` for Arm 2.

## Command Syntax

Basic command pattern:

```bash
rac <ip> [action] [options]
```

- `ip` (required): IP address of the robot arm, for example `192.168.1.49`.
- `action` (optional): One of `init`, `move`, `joint`, `gripper`.  
  - Defaults to `init` if omitted.

## Arguments

| Argument | Description |
|----------|-------------|
| `ip`     | IP address of the target robot arm (required). |
| `action` | Operation to perform: `init`, `move`, `joint`, `gripper` (defaults to `init`). |

## Options

| Flag             | Type    | Default | Description |
|------------------|---------|---------|-------------|
| `--offset`       | int     | 0       | Base joint offset in degrees (use `-30` for Arm 1). |
| `--gripper-angle`| int     | 90      | Gripper angle: `0` = fully closed, `90` = fully open. |
| `--speed`        | float   | 0.4     | Motion speed in m/s (recommended range: `0.1`–`1.0`). |
| `--coords`       | float[] | -       | Coordinate list: 6 values, format depends on action. |

### Coordinate Formats

- `move` (cartesian): `x y z rx ry rz`
- `joint` (joint space): `j1 j2 j3 j4 j5 j6` (degrees)

## Usage Examples

### Initialize Robot Arms to Home Position

```bash
# Arm 1 (offset required)
rac 192.168.1.49 init --offset -30

# Arm 2
rac 192.168.1.64 init
```

### Move to Absolute Cartesian Position

```bash
# Format: x y z rx ry rz
rac 192.168.1.49 move --offset -30 --coords 100 0 200 0 90 0
rac 192.168.1.64 move --coords 100 0 200 0 90 0
```

### Move to Absolute Joint Positions

```bash
# Format: j1 j2 j3 j4 j5 j6 (degrees)
rac 192.168.1.49 joint --offset -30 --coords 0 0 0 0 0 0
rac 192.168.1.64 joint --coords 0 0 0 0 0 0
```

### Control Gripper

```bash
# Arm 1 with offset
rac 192.168.1.49 gripper --offset -30 --gripper-angle 90  # Open
rac 192.168.1.49 gripper --offset -30 --gripper-angle 0   # Close

# Arm 2
rac 192.168.1.64 gripper --gripper-angle 90               # Open
rac 192.168.1.64 gripper --gripper-angle 0                # Close
```

### Use Custom Speed

```bash
# Faster motion with cartesian target
rac 192.168.1.49 move --offset -30 --speed 0.8 --coords 100 50 200 0 45 90
rac 192.168.1.64 move --speed 0.8 --coords 100 50 200 0 45 90
```

## Safety and Troubleshooting

- Always test new poses at low `--speed` (e.g., `0.1`) and near the home position before moving further.
- Keep coordinates within the listed working ranges unless you fully understand the hardware limits.
- If a command fails, check:
  - Network connectivity (ping the IP).
  - That `rac` is installed and in `PATH`.
  - That the correct `--offset` is used for the target arm.