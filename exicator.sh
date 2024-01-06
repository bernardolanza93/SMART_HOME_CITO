#!/bin/bash
cd
cd  SMART_HOME_CITO/

echo "CHECKK INTERNET CONNECTION... "
wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "ONLINE"
else
    echo "OFFLINE"
fi


git pull

echo  "SMART CITO UPDATED SUCCESFULLY"
echo "STARTING CITO SYSTEM "



echo ""

echo "       _                 _         "
echo " _   _| |__  _   _ _ __ | |_ _   _ "
echo "| | | | '_ \| | | | '_ \| __| | | |"
echo "| |_| | |_) | |_| | | | | |_| |_| |"
echo " \__,_|_.__/ \__,_|_| |_|\__|\__,_|"

echo ""


python3 exic_code.py