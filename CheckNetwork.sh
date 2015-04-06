$WGET -q --tries=20 --timeout=10 http://www.google.com -O /tmp/google.idx &> /dev/null
if [ ! -s /tmp/google.idx ]
then
    sudo python /home/pi/crm/DisplayText.py Network Not_Connected
    echo "Not Connected..!"
else
    sudo python /home/pi/crm/DisplayText.py Network Connected
    echo "Connected..!"
fi
