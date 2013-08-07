from flask import Flask, request, make_response
app = Flask(__name__)

#from bittorrent.bencode_jrs import encode, decode

import bencode

torrents = {}

@app.route("/announce")
def announce():
    # print request.args.keys()

    info_hash = request.args['info_hash']
    peer_id = request.args['peer_id']

    compact = bool(request.args["compact"][0])
    ip = request.remote_addr
    port = request.args["port"]
    left = request.args["left"]
    is_seeder = False
    if left == 0:
        is_seeder = True

    # for k,v in request.args.items():
    #     print k,v

    if 'info_hash' in torrents and (peer_id, ip, port) not in torrents[info_hash]:
        torrents[info_hash].append((peer_id, ip, port))
    # Otherwise, add the info_hash and the peer
    else:
        torrents[info_hash] = [(peer_id, ip, port)]
    # print torrents

    import urlparse
    queryargs = dict(urlparse.parse_qsl(urlparse.urlparse(request.url).query))
    bencoded

    return make_response(encode({'hi':'hi'}))

@app.route("/torrent")
def torrent():
    return

@app.route("/scrape")
def scrape():
    return

@app.route("/content")
def content():
    return

if __name__ == "__main__":
    app.run(debug=True)
