#!/usr/bin/env python
from twisted.internet import reactor
from autonomotorrent.BTApp import BTApp, BTConfig
import sys

torrent_file = sys.argv[1]

if __name__ == '__main__':
    app = BTApp()
    config = BTConfig(torrent_file)
    app.add_torrent(config)
    app.start_reactor()

