import requests
import json
import sys
import getopt

cmd_url = "http://117.185.16.231:8010/v1/task/sync"
data_url = "http://117.185.16.231:8010/v1/device"

headers = {
    'x-auth-token': "12345",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "b288f774-3cf5-735a-3d71-6c4ad4b374b4"
    }

class postboy():
    def __init__(self):
        self.payload = {}
        self.payload['method'] = 0
        self.payload['relativeUri'] = '/alive'
        self.payload['deviceUuid'] = ''
        self.payload['expireTime'] = 10
        self.payload['content'] = ''
        self.payload['type'] = 'RPC'
        self.prop = ''

    def do_post(self):
        met = "POST"
        url = cmd_url
        pl = ''
        if len(self.prop) > 0:
            met = "GET"
            url = data_url + '/' + self.payload['deviceUuid'] + '/properties/' + self.prop + '/latest';
        else:
            pl = json.JSONEncoder().encode(self.payload)

        response = requests.request(met, url, data=pl, headers=headers)
        print url + ' RESPONSES:'
        print json.dumps(json.loads(response.text), indent=4)

    def calc_arg(self, obj):
        for op, val in obj:
            if op == '-d':
                self.prop = val
            elif op == '-t':
                self.payload['content'] = val
            elif op == '-r':
                self.payload['relativeUri'] = val
            elif op == '-u':
                self.payload['deviceUuid'] = val
            elif op == '-p':
                self.payload['method'] = 1
            elif op == '-g':
                self.payload['method'] = 0

def usage():
    print 'usage: postboy.py -u someuuid [-d property] [-gp] [-r uri] [-t content]'
    print '\t -u \tdevice uuid'
    print '\n\t -d \tget latest report data, property value REQUIRED'
    print '\n\t -g \tcontrol device with method GET, default method'
    print '\t -p \tcontrol device with method PUT'
    print '\t -r \tthe relative URI to control device with, default is /alive'
    print '\t -t \tthe content to control device with, default is nil'

def main(opts):
    pb = postboy()
    pb.calc_arg(opts)
    pb.do_post()

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'cgpt:r:u:d:')
    if len(opts) <= 0:
        usage()
        exit()
    main(opts)