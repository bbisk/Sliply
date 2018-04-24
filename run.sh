#!/bin/bash
. credit.sh
gnome-terminal -e "celery -A sliply_project worker -l info"
gnome-terminal -e "redis-server"
./manage.py runsslserver localhost:9000



