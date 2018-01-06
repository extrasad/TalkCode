import os

APP_DIR = os.path.dirname(__file__)

def get_signing_key():
  path = open(APP_DIR + "/../../tmp/app.rsa", 'r')
  signing_key = path.read()
  path.close()
  return signing_key

def get_verify_key():
  path = open(APP_DIR + "/../../tmp/app.rsa.pub", 'r')
  verify_key = path.read()
  path.close()
  return verify_key