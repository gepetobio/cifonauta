#!/usr/bin/env bash

echo "--- Good morning, master. Let's get to work. Installing now. ---"

echo "--- Updating packages list ---"
sudo apt-get update

echo "--- Installing base packages ---"
sudo apt-get install -y python python-dev python-pip python-imaging libpq-dev git rsync postgresql nginx apache2 yui-compressor python-pyexiv2 imagemagick python-markdown python-memcache gettext libapache2-mod-wsgi

echo "--- Installing packages with pip ---"
pip install django==1.7 south django-debug-toolbar django-haystack django-mptt django-rosetta johnny-cache oauth2 psycopg2 -e git+https://github.com/toastdriven/pyelasticsearch.git@master#egg=pyelasticsearch requests sorl-thumbnail==12.1c pillow suds -e git+https://github.com/citylive/django-datatrans.git@master#egg=django_datatrans fabric —upgrade

echo "--- All set to go! Let's do this!!! ---"