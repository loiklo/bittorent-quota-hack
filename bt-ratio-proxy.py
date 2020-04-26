#!/usr/bin/env python3

# This filtering proxy is a man-in-the-middle for the bittorrent protocol.
# It interepts the requests sent to the tracker to update you download/upload ratio and apply a multiplier.
# Use this script as a proxy for you bittorrent client.
# To be sure to stay under the radar of anti cheat system:
#   - Don't cheat on the download ratio. From a tracker perspective, 99% of the time, a torrent started will finish. Be smart.
#   - Adjust the upload multiplier following the popularity of the torrent. Setting up a x20 multiplier on a file with 5 seeders and 2 leachers is stupid.

from twisted.web import http, proxy
from twisted.internet import error, reactor
import argparse
import re

class BtProxyRequest(proxy.ProxyRequest):
  request_number      = 0
  download_multiplier = 1
  upload_multiplier   = 7.3
 
  def process(self):
    uristr = self.uri.decode() # bytes to string
    print(">>> real["+str(BtProxyRequest.request_number)+"]: " + uristr)
 
    # Download
    dlregex = re.compile('downloaded=(\d+)')
    dl_match = re.search(dlregex, uristr)
    if dl_match != None:
      dlvalue = int(dl_match.group(1))
      fake_dl_value = int(dlvalue * BtProxyRequest.download_multiplier)
      uristr = re.sub("downloaded="+str(dlvalue), "downloaded="+str(fake_dl_value), uristr)
 
    # Upload
    ulregex = re.compile('uploaded=(\d+)')
    ul_match = re.search(ulregex, uristr)
    if ul_match != None:
      ul_value = int(ul_match.group(1))
      fake_ul_value = int(ul_value * BtProxyRequest.upload_multiplier)
      uristr = re.sub("uploaded="+str(ul_value), "uploaded="+str(fake_ul_value), uristr)
 
    print("<<< fake["+str(BtProxyRequest.request_number)+"]: " + uristr)
    self.uri = uristr.encode() # string to bytes
    BtProxyRequest.request_number = BtProxyRequest.request_number + 1
    proxy.ProxyRequest.process(self)

class BtProxy(proxy.Proxy):
  requestFactory = BtProxyRequest

class BtProxyFactory(http.HTTPFactory):
  protocol = BtProxy

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', default=BtProxyRequest.download_multiplier, help='Download multiplier')
  parser.add_argument('-u', default=BtProxyRequest.upload_multiplier, help='Upload multiplier')
  args = parser.parse_args()

  BtProxyRequest.download_multiplier = float(args.d)
  BtProxyRequest.upload_multiplier   = float(args.u)

  reactor.listenTCP(8080, BtProxyFactory())
  reactor.run()

