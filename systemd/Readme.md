# Usage

1. copy example hiveos-exporter.service to /etc/systemd/system/

    `cp /path/to/hiveos-exporter.service /etc/systemd/system/`

2. Edit `hiveos-exporter.service` to match your settings:

    `Environment="RIG_NAME=Default"`
   
    `ExecStart=/usr/bin/python3  /root/hiveos-exporter/promstat.py`
3. Reload systemd

    `systemctl daemon-reload`
4. Enable hiveos-exporter.service

    `systemctl enable hiveos-exporter.service`
5. Start hiveos-exporter.service

    `systemctl start hiveos-exporter.service`
6. Check status of service

    `systemctl status hiveos-exporter.service`
