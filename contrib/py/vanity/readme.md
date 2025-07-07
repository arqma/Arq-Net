# arqnet vanity address generator

installing deps:

    sudo apt install libsodium-dev
    pip3 install --user -r requirements.txt

to generate a nonce with a prefix `^4rq` using 8 cpu threads:

    python3 arqnet-vanity.py keyfile.private 4rq 8
