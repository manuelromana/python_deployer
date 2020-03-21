"""This file is to set config for the ssh connection """
__author__ = "romana_m"


HOST = "192.168.0.21"
USERNAME = "root"
PASSWORD = "Manuel1982"
TIMEOUT = 10
DEBCONF = "debconf-set-selections"
DEBIAN_DOCKER_REPOS = "https://download.docker.com/linux/debian"
CURL_DOCKER = "curl -fsSL https://download.docker.com/linux/debian/gpg"
COMMANDS = ["apt-get update",
            "echo 'debconf debconf/frontend select Noninteractive'|{}".format(
                DEBCONF),
            "apt-get install apt-transport-https",
            "apt-get install -y curl ",
            "apt-get install ca-certificates",
            "apt-get install -y gnupg2",
            "apt-get install -y software-properties-common",
            " {}| sudo apt-key add -".format(CURL_DOCKER),
            "apt-key fingerprint 0EBFCD88",
            "add-apt-repository 'deb [arch=amd64] {} buster stable'".format(
                DEBIAN_DOCKER_REPOS),
            "apt-get update",
            "apt-get install -y docker-ce docker-ce-cli containerd.io"
            ]
CHECKER_LIST_FILES = ["/checker/app.py", "/checker/run.py"]
