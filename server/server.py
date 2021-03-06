#!/usr/bin/env python3

import sys
import os
from time import sleep
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = True
HREFHOSTURL = "http://localhost:6969"
AUTH = "put some secret string in here"

clients = {}

banners = {
    "alpine": [
        "<span class=\"blue\">        /\\            </span>",
        "<span class=\"blue\">       /  \\           </span>",
        "<span class=\"blue\">      / /\\ \\  /\\      </span>",
        "<span class=\"blue\">     / /  \\ \\/  \\     </span>",
        "<span class=\"blue\">    / /    \\ \\/\\ \\    </span>",
        "<span class=\"blue\">   / / /|   \\ \\ \\ \\   </span>",
        "<span class=\"blue\">  /_/ /_|    \\_\\ \\_\\  </span>",
        "<span class=\"blue\">               </span>"
    ],
    "debian": [
        "<span class=\"red\">    _____    </span>",
        "<span class=\"red\">   /  __ \\   </span>",
        "<span class=\"red\">  |  /    |  </span>",
        "<span class=\"red\">  |  <span class=\"bold\">\\___-   </span></span>",
        "<span class=\"red bold\">  -_         </span>",
        "<span class=\"red bold\">    --_      </span>",
        "<span class=\"red bold\">    --_      </span>",
        "<span class=\"red bold\">               </span>"
    ],
    "ubuntu": [
        "<span class=\"orange\">           _   </span>",
        "<span class=\"orange\">       ---(_)  </span>",
        "<span class=\"orange\">   _/  ---  \\  </span>",
        "<span class=\"orange\">  (_) |   |    </span>",
        "<span class=\"orange\">    \\  --- _/  </span>",
        "<span class=\"orange\">       ---(_)  </span>",
        "<span class=\"orange\">               </span>",
        "<span class=\"orange\">               </span>"
    ],
    "fedora": [
        "<span class=\"white\">        _____     </span>",
        "<span class=\"white\">       /   __)</span><span class=\"blue\">\\   </span>",
        "<span class=\"white\">       |  /  </span><span class=\"blue\">\\ \\  </span>",
        "<span class=\"blue\">    __</span><span class=\"white\">_|  |_</span><span class=\"blue\">_/ /  </span>",
        "<span class=\"blue\">   / </span><span class=\"white\">(_    _)</span><span class=\"blue\">_/   </span>",
        "<span class=\"blue\">  / /  </span><span class=\"white\">|  |       </span>",
        "<span class=\"blue\">  \\ \\</span><span class=\"white\">__/  |       </span>",
        "<span class=\"blue\">   \\</span><span class=\"white\">(_____/       </span>"
    ],
    "gentoo": [
        "<span class=\"magenta\">    .-----.      </span>",
        "<span class=\"magenta\">  .\`    _  \`.    </span>",
        "<span class=\"magenta\">  \`.   (<span class=\"bold\">_)   </span></span>",
        "<span class=\"magenta\">    \`<span class=\"bold\">.        /  </span></span>",
        "<span class=\"magenta bold\">   .\`       .\`   </span>",
        "<span class=\"magenta bold\">  /       .\`     </span>",
        "<span class=\"magenta bold\">  \____.-\`       </span>",
        "<span class=\"magenta bold\">               </span>"
    ],
    "suse": [
        ""
    ],
    "void": [
        ""
    ],
    "linux": [
        ""
    ]
}
colors = {
    "alpine": "blue",
    "debian": "red",
    "ubuntu": "orange",
    "fedora": "blue",
    "gentoo": "magenta",
    "suse": "green",
    "void": "green",
    "linux": "white"
}

@app.route('/')
def index():
    return render_template("index.html", clients=clients)

@app.route('/<auth>/<hostname>', methods=['POST'])
def register(auth, hostname):
    if auth != AUTH:
        return make_response(jsonify({"message": "Unauthorized", "redirect": "/unauthorized"}), 401)
    clients[hostname] = {
        hostname = hostname,
        chassis = request.form["chassis"],
        os = request.form["os"],
        cpu = request.form["cpu"],
        kernel = request.form["kernel"],
        shell = request.form["shell"]
        pkgs = request.form["pkgs"],
        disk = request.form["disk"],
        thermals = request.form["thermals"],
        mem = request.form["mem"],
        load1 = request.form["load1"],
        load5 = request.form["load5"],
        load15 = request.form["load15"],
        uptime = request.form["uptime"]
    }

if __name__ == '__main__':
    userdb = load_userdb()
    latest20vids = load_latest20vids()
    app.run(host='0.0.0.0' if PUBLIC else '127.0.0.1', port=4545, debug=True)
