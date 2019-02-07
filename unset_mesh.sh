./ssh_pi.sh GroupA sudo mv /etc/network/interfaces /etc/network/interfaces.mesh
./ssh_pi.sh GroupA sudo mv /etc/network/interfaces.backup /etc/network/interfaces
./ssh_pi.sh GroupA sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.mesh
./ssh_pi.sh GroupA sudo mv /etc/wpa_supplicant/wpa_supplicant.conf.backup /etc/wpa_supplicant/wpa_supplicant.conf
#./ssh_pi.sh GroupA sudo service wpa_supplicant restart
./ssh_pi.sh GroupA sudo ifdown wlan0
./ssh_pi.sh GroupA sudo ifup wlan0
./ssh_pi.sh GroupA sudo iwconfig
