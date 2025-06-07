
ssh -L 5901:127.0.0.1:5901 -N -f tandinh

# -L: Tunnel tandinh:5901 -> localhost:5901
# -N: No remote command, just connect
# -f: Background execution

