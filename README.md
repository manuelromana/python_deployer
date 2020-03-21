# Groupe de romana_m

## my_deployer project : files

### config.py : ssh credential + commands bash

### ssh.py : class for the remote connexion and channel

### mydeployer.py : CLI with argparse

## problems : commands python to bash  :

- problems of debconf front end interactive

- problem of commands with \

        example 1 
        apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common

    did 5 different commands 

        example 2 :
        add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/debian \
        $(lsb_release -cs) \
        stable"
    problems with the $ had to take it off 

-problems of some return of bash error don’t go to stderr
(add-apt-repository : return in stdout)

-warning with parsing key for depot


- problems parsarg :

    if no subcommand entered error , I would like help message
