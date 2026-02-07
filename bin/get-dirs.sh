# $1 = root
# $2 = filter
find "${1:-.}" \( -path '*/.*' -o -name '__pycache__' -o -path '*/target' \) -prune -o -type d -print | fzf -q "$2" --select-1 > /tmp/get-dirs.out
