apt update
apt upgrade
apt install tinyproxy
sed -i "s/Allow 127.0.0.1/Allow 0.0.0.0" /etc/tinyproxy/tinyproxy.conf
/etc/init.d/tinyproxy restart