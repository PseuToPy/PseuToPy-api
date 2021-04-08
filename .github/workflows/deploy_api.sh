pkill gunicorn
gunicorn -w 4 -b 192.168.1.110:5000 src.app:app &