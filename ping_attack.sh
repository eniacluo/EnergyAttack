for a in 10 20 40 80 160 320 640 1280 2560 5120 10240 20480 40960 81920 163840
do
    for b in 100 200 400 800 1600 3200 6400 12800 25600 51200
    do
        ./do.sh ssh pi@10.42.0.20 sudo ping localhost -f -c $a -s $b
        sleep 5
    done
done

