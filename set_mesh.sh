./ssh_pi.sh GroupA sudo mv /etc/network/interfaces /etc/network/interfaces.backup
./ssh_pi.sh GroupA sudo mv /etc/network/interfaces.mesh /etc/network/interfaces
./ssh_pi.sh GroupA sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.backup
./ssh_pi.sh GroupA sudo mv /etc/wpa_supplicant/wpa_supplicant.conf.mesh /etc/wpa_supplicant/wpa_supplicant.conf
#./ssh_pi.sh GroupA sudo service wpa_supplicant restart
./ssh_pi.sh GroupA sudo ifdown wlan0
./ssh_pi.sh GroupA sudo ifup wlan0
./ssh_pi.sh GroupA sudo iwconfig
