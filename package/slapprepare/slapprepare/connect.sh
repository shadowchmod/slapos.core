#!/bin/bash


TEMP_DIR="/tmp/slaptemp/"
BASEURL="https://www.vifib.net"

while :; do
    read -p "Enter your user name: " USERNAME
    read -s -p "Enter your password: " PASSWORD
    echo ""
    curl -k --location --cookie cookie.txt  --user $USERNAME:$PASSWORD "$BASEURL" | grep logout > /dev/null
    if [[ $? != 0 ]]; then
	echo "Wrong login/password"
    else
	echo ""
	break
    fi
done

echo "Enter Computer name: "
read COMPUTERNAME
    
curl -k -o "$TEMP_DIR/certificate_key.html" --location --cookie cookie.txt --user $USERNAME:$PASSWORD "https://www.vifib.net/add-a-server/WebSection_registerNewComputer?dialog_id=WebSection_viewServerInformationDialog&dialog_method=WebSection_registerNewComputer&title=$COMPUTERNAME&object_path=/erp5/web_site_module/hosting/add-a-server&update_method=&cancel_url=https%3A//www.vifib.net/add-a-server/WebSection_viewServerInformationDialog&Base_callDialogMethod=&field_your_title=Essai1&dialog_category=None&form_id=view"

