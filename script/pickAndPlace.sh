while true; do
rac 192.168.1.64 init
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 185 15 0 0 0 0
rac 192.168.1.64 move --coords 185 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 185 15 0 0 0 0

rac 192.168.1.64 move --coords 241 15 0 0 0 0
rac 192.168.1.64 move --coords 241 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 241 15 0 0 0 0
rac 192.168.1.64 init

rac 192.168.1.64 move --coords 241 15 0 0 0 0
rac 192.168.1.64 move --coords 241 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 241 15 0 0 0 0

rac 192.168.1.64 move --coords 185 15 0 0 0 0
rac 192.168.1.64 move --coords 185 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 185 15 0 0 0 0
rac 192.168.1.64 init
done