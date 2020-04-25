#!/usr/bin/env python3

# This filtering proxy only allows "start" bittorrent events. It prevents your bittorent client to update the tracker, so the tracker don't update your quota.
# Use this script as a proxy for you bittorrent client

# Warnings:
# - You will only receive 1 list of peers when the download starts.
#     If the torrent doesn't complete with this initial list, you need to cancel the download and restart it from scratch
# - When the bittorrent client starts, it leaks "start" events to the tracker even for already finished download (left param = 0).
#     Be sure to have your torrents download list empty before exiting your client or the tracker will know you are cheating on the next client start.
# - If the tracker is smart, with a little bit a data science, it's easy to see you are cheating because the ratio "start event" vs "complete event"
#     To prevent being ban, do real small download to keep a good start/complete ratio.

from twisted.web import http, proxy
from twisted.internet import error, reactor
import re

class BtProxyRequest(proxy.ProxyRequest):
  request_number = 0

  def process(self):
    uristr = self.uri.decode() # bytes to string
    print(">>> req["+str(BtProxyRequest.request_number)+"]: " + uristr)

    event_regex = re.compile('event=started')
    event_match = re.search(event_regex, uristr)
    if event_match != None:
      self.uri = uristr.encode() # string to bytes
      proxy.ProxyRequest.process(self)
      print(">>> act["+str(BtProxyRequest.request_number)+"]: Request allowed")
    else:
      print(">>> act["+str(BtProxyRequest.request_number)+"]: Only 'started' event allowed => request blocked")
    
    BtProxyRequest.request_number = BtProxyRequest.request_number + 1

class BtProxy(proxy.Proxy):
  requestFactory = BtProxyRequest

class BtProxyFactory(http.HTTPFactory):
  protocol = BtProxy

if __name__ == '__main__':
  reactor.listenTCP(8080, BtProxyFactory())
  reactor.run()
