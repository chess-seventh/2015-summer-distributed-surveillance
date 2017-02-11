#!/bin/sh

mysql -u root -e "DROP DATABASE video_system"
mysql -u root -e "CREATE DATABASE video_system"
mysql -u root video_system < create.sql
