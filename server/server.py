#!/usr/bin/env python3

import sys
import os
from time import sleep
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = True
HREFHOSTURL = "http://localhost:6969"
AUTH = "secret"

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
        "<span class=\"blue\">                      </span>"
    ],
    "debian": [
        "<span class=\"red\">    _____    </span>",
        "<span class=\"red\">   /  __ \\   </span>",
        "<span class=\"red\">  |  /    |  </span>",
        "<span class=\"red\">  |  <span class=\"bold\">\\___-   </span></span>",
        "<span class=\"red bold\">  -_         </span>",
        "<span class=\"red bold\">    --_      </span>",
        "<span class=\"red bold\">             </span>",
        "<span class=\"red bold\">             </span>"
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
        "<span class=\"green\">      _______    </span>",
        "<span class=\"green\">  -___|   __ \\   </span>",
        "<span class=\"green\">         / </span><span class=\"bold white\">.</span><span class=\"green\">\\ \\  </span>",
        "<span class=\"green\">         \\__/ |  </span>",
        "<span class=\"green\">       _______|  </span>",
        "<span class=\"green\">       \\_______  </span>",
        "<span class=\"green\">  --__________/  </span>",
        "<span class=\"green\">                 </span>"
    ],
    "void": [
        "<span class=\"green bold\">      _______      </span>",
        "<span class=\"green\">      <span class=\"bold\">\\_____ `-    </span></span>",
        "<span class=\"green\">   /\\   <span class=\"bold\">___ `- \\   </span></span>",
        "<span class=\"green\">  | |  <span class=\"bold\">/   \  | |  </span></span>",
        "<span class=\"green\">  | |  <span class=\"bold\">\___/  | |  </span></span>",
        "<span class=\"green\">   \\ `-_____  <span class=\"bold\">\\/   </span></span>",
        "<span class=\"green\">    `-______\\      </span>",
        "<span class=\"green\">                   </span>"
    ],
    "linux": [
        "<span class=\"black\">      ___     </span>",
        "<span class=\"black\">     (</span><span class=\"white\">.. </span><span class=\"black\">\    </span>",
        "<span class=\"black\">     (</span><span class=\"yellow\"><> </span><span class=\"black\">|    </span>",
        "<span class=\"black\">    /</span><span class=\"white\">/  \\ </span><span class=\"black\">\\   </span>",
        "<span class=\"black\">   ( </span><span class=\"white\">|  | </span><span class=\"black\">/|  </span>",
        "<span class=\"yellow\">  _</span><span class=\"black\">/\\ </span><span class=\"white\">__)</span><span class=\"black\">/</span><span class=\"yellow\">_</span><span class=\"black\">)  </span>",
        "<span class=\"yellow\">  \/</span><span class=\"black\">-____</span><span class=\"yellow\">\/   </span>",
        "<span class=\"black\">              </span>"
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
    return render_template("index.html", clients=list(clients.values()))

@app.route('/<auth>/<hostname>', methods=['POST'])
def register(auth, hostname):
    if auth != AUTH:
        return make_response(jsonify({"message": "Unauthorized", "redirect": "/unauthorized"}), 401)
    osname = request.form["os"].lower()
    logo = banners["linux"]
    color = colors["linux"]
    if "debian" in osname or "devuan" in osname:
        logo = banners["debian"]
        color = colors["debian"]
    elif "alpine" in osname:
        logo = banners["alpine"]
        color = colors["alpine"]
    elif "ubuntu" in osname:
        logo = banners["ubuntu"]
        color = colors["ubuntu"]
    elif "fedora" in osname or "centos" in osname:
        logo = banners["fedora"]
        color = colors["fedora"]
    elif "gentoo" in osname or "funtoo" in osname:
        logo = banners["gentoo"]
        color = colors["gentoo"]
    elif "suse" in osname:
        logo = banners["suse"]
        color = colors["suse"]
    elif "void" in osname:
        logo = banners["void"]
        color = colors["void"]
    clients[hostname] = {
        "hostname": hostname,
        "chassis": request.form["chassis"],
        "os": request.form["os"],
        "cpu": request.form["cpu"].replace(" Quad-Core", "").replace(" Dual-Core", "").replace(" Eight-Core", "").replace(" Hexa-Core", "").replace(" Processor", ""),
        "kernel": request.form["kernel"],
        "shell": request.form["shell"],
        "pkgs": request.form["pkgs"],
        "disk": request.form["disk"],
        "thermals": request.form["thermals"],
        "mem": request.form["mem"],
        "load1": request.form["load1"],
        "load5": request.form["load5"],
        "load15": request.form["load15"],
        "uptime": request.form["uptime"],
        "logo": logo,
        "color": color
    }
    return make_response(jsonify({"message": "OK"}), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0' if PUBLIC else '127.0.0.1', port=6969, debug=True)
