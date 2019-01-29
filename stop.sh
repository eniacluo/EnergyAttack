ps aux | grep 'python read' | grep -v 'grep' | awk '{system("kill "$2)}'
