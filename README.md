# Talkcode

[![Build Status](https://travis-ci.org/CharlyJazz/TalkCode.svg?branch=master)](https://travis-ci.org/CharlyJazz/TalkCode)

Status: **building** :construction:

Building:
  * openssl genrsa -out tmp/app.rsa 2048
  * openssl rsa -in tmp/app.rsa -pubout > tmp/app.rsa.pub
  * Create credentials.txt with the enviroment and exports with ```set -a  && . ./credentials.txt && set +a```