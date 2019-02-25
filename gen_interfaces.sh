for i in 1 2 3 4 5 6 7 8
do
    cp interfaces.mesh interfaces$i.mesh
    sed -i "/192.168.1./ s/192.168.1.*/192.168.1.12$i/" interfaces$i.mesh
    scp interfaces$i.mesh pi@pia$i:~/interfaces.mesh
    ssh pi@pia$i sudo mv interfaces.mesh /etc/network/
done
