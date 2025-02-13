#!/bin/bash

echo 'content-type: text/html'
echo 

QUERY_STRING=$1

if [ -z "$QUERY_STRING" ]; then
  echo "<html><head><title>Error</title></head><body>"
  echo "<h1>Error: No string provided!</h1>"
  echo "<p>You are supposed to add a string that you want to encode after cgi-bin/qrcode.sh</p>"
  echo "</body></html>"
  exit 1
fi

ENCODED_QR=$(qrencode -o - "$QUERY_STRING" | base64 -w 0)

echo "<html>"
echo "<head><title>QR Code</title></head>"
echo "<body>"
echo "<img src=\"data:image/png;base64,$ENCODED_QR\" />"
echo "</body>"
echo "</html>"
