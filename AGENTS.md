# AGENTS.md - Guidelines for Agents Working in This Repository

This file provides guidance for agentic coding agents operating in the Robotics-Arm-CLI repository.

## Project Overview

A CLI tool for controlling robotics arms using behavior trees (py-trees). The codebase provides a Python interface to communicate with robot arms via TCP sockets.

## Project Structure

```
src/robotics_arm_cli/
├── __init__.py           # Package entry point, exports main
├── app.py                # CLI application entry point
├── robot_arm/
│   ├── robot_arm.py      # Main RobotArm class
│   ├── tcp.py            # TCP socket communication
│   ├── position.py       # Position classes (Cartesian, JPosition)
│   └── ra_error.py       # Custom exceptions (RAError, RAConnectionError)
└── example/              # Example usage scripts
```

## Build, Lint, and Test Commands

This project uses `uv` for package management.

### Installation
```bash
uv pip install -e .
```

### Running the CLI
```bash
uv run rac
```

### Running Examples
```bash
uv run python src/robotics_arm_cli/example/Checkerboard_Test.py
uv run python src/robotics_arm_cli/example/Checkerboard_Test_Twin.py
```

### Type Checking
```bash
uv run mypy src/robotics_arm_cli
```

### Linting
```bash
uv run ruff check src/robotics_arm_cli
uv run ruff format src/robotics_arm_cli  # Format code
```

### Running a Single Test
If you add tests using pytest:
```bash
uv run pytest tests/                           # Run all tests
uv run pytest tests/test_robot_arm.py           # Run specific test file
uv run pytest tests/test_robot_arm.py::test_name  # Run specific test
```

### Running All Checks
```bash
uv run mypy src/robotics_arm_cli && uv run ruff check src/robotics_arm_cli
```

---

## Code Style Guidelines

### General Principles

- **Be Pythonic**: Follow PEP 8 and common Python conventions
- **Be Explicit**: Prefer explicit over implicit
- **Keep It Simple**: Write simple, readable code first
- **No Premature Optimization**: Optimize only when necessary

### Imports

```python
# Standard library first
import socket
from typing import Optional

# Third-party libraries
from py_trees import BehaviorTree, Tree

# Local application imports
from .tcp import Tcp
from .ra_error import RAError, RAConnectionError
from .position import Cartesian, JPosition
```

- Use absolute imports within the package (`from robotics_arm_cli.robot_arm import ...`)
- Group imports: stdlib → third-party → local
- Sort imports alphabetically within each group
- Use explicit imports instead of `from module import *`

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | lowercase snake_case | `robot_arm.py` |
| Classes | PascalCase | `RobotArm`, `RAError` |
| Functions/methods | lowercase snake_case | `move_joint()`, `read_joint_pos()` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_HOST = "192.168.1.1"` |
| Variables | lowercase snake_case | `host`, `cartesian` |

### Type Hints

Always use type hints for function signatures:

```python
# Good
def move_joint(self, jPos: JPosition) -> None:
    ...

def get_speed(self) -> float:
    ...

def read_input_io(self, io_index: int) -> int:
    ...

# Good - using Optional for nullable returns
def find_robot(self, timeout: Optional[float] = None) -> Optional[RobotArm]:
    ...
```

### Error Handling

- Use custom exception classes for domain-specific errors
- Catch specific exceptions, not bare `except:`
- Raise informative error messages

```python
# Good - custom exception hierarchy
class RAError(Exception):
    pass

class RAConnectionError(RAError):
    pass

# Good - specific exception handling
def _validate(self, reply: str) -> None:
    values = reply.split(',')
    if len(values) < 2:
        raise RAError(f"Received invalid response: {reply}")
    if values[1] != 'OK':
        raise RAError(f"Received error: {reply}")
```

### Documentation

- Add docstrings for public classes and functions
- Keep docstrings concise but informative
- Use Google-style or NumPy-style docstrings

```python
def set_tool_coordinate(self, mode: int) -> None:
    """
    SetToolCoordinateMotion - Enable tool coordinate motion.
    
    Args:
        mode: 1 for tool coordinate, 0 for base coordinate
    
    Raises:
        RAError: If the robot returns an error response
    """
```

### Code Formatting

- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Add spaces around operators: `x = 1` not `x=1`
- Use blank lines sparingly to separate logical sections

```python
# Good - logical sections separated by blank lines
class RobotArm:
    def __init__(self, host: str, base_offset: float = 0):
        self.tcp = Tcp(host)
        self.base_offset = base_offset

    # ---------------- Core System Control ----------------
    def power_on(self) -> None:
        reply = self.tcp.send("Electrify,;")
        self._validate(reply)

    # ---------------- Motion Control ----------------
    def move_joint(self, jPos: JPosition) -> None:
        msg = f"MoveJ,0,{jPos.j1},..."
```

### File Headers

Every Python file should have:
1. Appropriate imports
2. Module-level docstring (optional for internal modules)

### Performance Considerations

- Lazy imports when possible
- Reuse TCP connections instead of creating new ones
- Use appropriate data structures

### Testing

When adding tests:
- Place tests in a `tests/` directory at the project root
- Use pytest as the test framework
- Follow naming: `test_module_name.py`
- Use descriptive test names: `test_robot_arm_moves_to_home_position`

### Adding New Features

1. Follow the existing class structure (e.g., `RobotArm` for robot operations)
2. Add appropriate type hints
3. Use the `_validate()` method for robot responses
4. Document the robot command being sent
5. Add example usage if it's a significant feature
