## Websocket api

import os
import json
import getpass
import uuid
import hashlib
from pprint import pprint
from collections import OrderedDict
import time
import thread
from functools import partial
from thread import allocate_lock

s_print_lock = allocate_lock()

import sys

import ScriptResources
reload(ScriptResources)

CURRENT_DIR  = ScriptResources.scriptsRoot()
sys.path.append(os.path.abspath(CURRENT_DIR))

import websocket
reload(websocket)

# 1ms polling rate, do not go lower than this value.
minSleepTime = .01

def toPrettyJson(data):
    return json.dumps(data, indent=2, separators=(',', ': '))

# https://stackoverflow.com/questions/40356200/python-printing-in-multiple-threads/50882022#50882022
def threadPrint(text):
    """Thread safe print function"""
    with s_print_lock:
        print(text)

class JSONRPCWebsocket:

    def __init__(self, socketURL):

        self.socketURL = socketURL
        self.callbackMap = {}
        self.currentSyncMessageID = None
        self.currentSyncMessageResponse = None
        self.socket = None
        self.isConnected = False

    def send_message(self, message):
        if self.currentSyncMessageID != None:
            print "JSONRPCWebsocket error, cannot send sync message, as busy with a sync message already..."
            return ""
        if message != "":
            messageID = str(uuid.uuid4())

            payload = {
                    "from": "html",
                    "to": "engine",
                    "jsonrpc": "2.0",
                    "id": messageID
            }

            # add payload to message
            payload.update(message)

            payloadJSON = toPrettyJson(payload)

            # update the current sync message ID
            self.currentSyncMessageID = messageID

            self.socket.send(payloadJSON)

            print "Waiting for sync response."
            i = 0
            while True:
                i = i + 1
                if i == 1000:
                    print "Sync response timed out"
                    self.currentSyncMessageResponse = None
                    self.currentSyncMessageID = None
                    return
                time.sleep(minSleepTime)
                if self.currentSyncMessageID == None:
                    return self.currentSyncMessageResponse

            #return self.currentSyncMessageResponse

        else:
            print "JSONRPCWebsocket empty message, nothing to send"
            return ""


    def send_message_async(self, message, callback):
        if not self.isConnected:
            print "JSONRPCWebsocket not connected, cannot send."
            return None

        if message != "":
            messageID = str(uuid.uuid4())

            payload = {
                    "from": "html",
                    "to": "engine",
                    "jsonrpc": "2.0",
                    "id": messageID
            }

            self.callbackMap[messageID] = callback

            # add payload to message
            payload.update(message)

            payloadJSON = toPrettyJson(payload)

            self.socket.send(payloadJSON)

            while True:
                time.sleep(.0001)
                if APIWebsocket.isConnected():
                    print "MateriaAPI connected"
                    break

        else:
            print "JSONRPCWebsocket empty message, nothing to send"
        return messageID


    def connect(self):
        print "JSONRPCWebsocket connecting..."
        def run(*args):
            websocket.enableTrace(True)
            self.socket  = websocket.WebSocketApp(self.socketURL,
                                      on_message = self.on_message,
                                      on_error = self.on_error,
                                      on_close = self.on_close
                                      )
            self.socket.on_open = self.on_open
            self.socket.run_forever()
            print "JSONRPCWebsocket after websocket forever run disconnect/exit"

        thread.start_new_thread(run, ())

    def on_error(self, ws, error):
        print "JSONRPCWebsocket error... " + error

    def on_open(self, ws):
        print "JSONRPCWebsocket open"
        self.isConnected = True

    def on_message(self, ws, message):
        responseJSON = json.loads(message)


        # expose message in MateriaAPI
        # self.setMessage(message)

        messageID = None
        if "id" in responseJSON:
            messageID = responseJSON["id"]
            # debug log success/error for received response
            if "result" in responseJSON:
                print "success response for API call with id " + messageID
            else:
                print "error response for API call with id " + messageID

            # check if message is an async message
            if messageID in self.callbackMap:
                print "received ASYNC message response"
                callbackFunction = self.callbackMap[messageID]
                if callbackFunction != None:
                    print "callback f" + str(callbackFunction)
                    del self.callbackMap[messageID]
                    callbackFunction(responseJSON)
                else:
                    print "callback none"
            elif messageID == self.currentSyncMessageID:
                print "received SYNC message response"
                self.currentSyncMessageResponse = responseJSON
                self.currentSyncMessageID = None
            else:
                print "received response for UNKNOWN message"

    def on_close(self, ws):
        print "JSONRPCWebsocket closed. "
        self.isConnected = False

    def disconnect(self):
        print "JSONRPCWebsocket disconnect..."
        self.socket.close()

    def hello(self):
        print "JSONRPCWebsocket hello"

