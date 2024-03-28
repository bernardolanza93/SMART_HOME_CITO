#!/bin/bash
sleep 30

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


python3 exic_code.py