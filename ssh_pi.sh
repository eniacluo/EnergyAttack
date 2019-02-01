for i in 1 3 5 7; do echo "--- This is pi$i ---"; ssh pi@pi$i "$@"; done;
