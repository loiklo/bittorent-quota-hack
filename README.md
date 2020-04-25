# bittorent-quota-hack

How to (Ubuntu 20.04):
- apt install python3-twisted
- ./bt-noquota-proxy.py or ./bt-ratio-proxy.py
- set 127.0.0.1:8080 as a proxy in your bittorent client

bt-noquota-proxy.py
- Pevent the quota (download and upload) to be updated on the tracker

bt-ratio-proxy.py
- Add a multiplier to the quota (download and upload) before updating the tracker
