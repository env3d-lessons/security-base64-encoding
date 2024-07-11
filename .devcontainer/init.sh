#!/bin/bash

sudo rm -r /usr/lib/cgi-bin
sudo ln -s $(pwd) /usr/lib/cgi-bin
sudo a2enmod cgid
sudo service apache2 start
