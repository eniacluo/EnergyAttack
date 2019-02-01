for i in 1 3 5 7; do echo "--- This is pi$i ---"; scp "$1" pi@pi$i:"$2"; done;
