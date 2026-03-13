while true; do
# d7d5
rac 192.168.1.64 init
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 185 15 -40 0 0 0
rac 192.168.1.64 move --coords 185 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 185 15 -40 0 0 0

rac 192.168.1.64 move --coords 297 15 -40 0 0 0
rac 192.168.1.64 move --coords 297 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 297 15 -40 0 0 0
rac 192.168.1.64 init

# g8f6
rac 192.168.1.64 move --coords 129 -158 -40 0 0 0
rac 192.168.1.64 move --coords 129 -158 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 129 -158 -40 0 0 0

rac 192.168.1.64 move --coords 241 -102 -40 0 0 0
rac 192.168.1.64 move --coords 241 -102 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 241 -102 -40 0 0 0
rac 192.168.1.64 init

# d5d7
rac 192.168.1.64 move --coords 297 15 -40 0 0 0
rac 192.168.1.64 move --coords 297 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 297 15 -40 0 0 0

rac 192.168.1.64 move --coords 185 15 -40 0 0 0
rac 192.168.1.64 move --coords 185 15 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 185 15 -40 0 0 0
rac 192.168.1.64 init

# f6g8
rac 192.168.1.64 move --coords 241 -102 -40 0 0 0
rac 192.168.1.64 move --coords 241 -102 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 0
rac 192.168.1.64 move --coords 241 -102 -40 0 0 0

rac 192.168.1.64 move --coords 129 -158 -40 0 0 0
rac 192.168.1.64 move --coords 129 -158 65 0 0 0
rac 192.168.1.64 gripper --gripper-angle 60
rac 192.168.1.64 move --coords 129 -158 -40 0 0 0
rac 192.168.1.64 init
done