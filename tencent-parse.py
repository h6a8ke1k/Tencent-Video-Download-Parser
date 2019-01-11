'''
Copyright 2019 and onwards h6a8ke1k @ GitHub.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import requests
import json
import sys

if len(sys.argv) != 2:
    print('You must enter only 1 argument (vid)!')
    exit()

vid = sys.argv[1]
for definition in ('fhd', 'shd', 'hd', 'sd'):
    params = {
        'isHLS': False,
        'charge': 1,
        'vid': vid,
        'defn': definition,
        'defnpayver': 1,
        'otype': 'json',
        'platform': 10901,
        'sdtfrom': 'v1010',
        'host': 'v.qq.com',
        'fhdswitch': 0,
        'show1080p': 1,
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': '', # to download vip-only videos, you must add cookies here after login in the browers.
    }
    r = requests.get('http://h5vv.video.qq.com/getinfo', params=params, headers=headers)
    data = json.loads(r.content[len('QZOutputJson='):-1])
 
    url_prefix = data['vl']['vi'][0]['ul']['ui'][0]['url']
    for stream in data['fl']['fi']:
        if stream['name'] != definition:
            continue
        stream_id = stream['id']
        urls = []
        for d in data['vl']['vi'][0]['cl']['ci']:
            keyid = d['keyid']
            filename = keyid.replace('.10', '.p', 1) + '.mp4'
            params = {
                'otype': 'json',
                'vid': vid,
                'format': stream_id,
                'filename': filename,
                'platform': 10901,
                'vt': 217,
                'charge': 0,
            }
            r = requests.get('http://h5vv.video.qq.com/getkey', params=params, headers=headers)
            data = json.loads(r.content[len('QZOutputJson='):-1])
            try:
                url = '%s/%s?sdtfrom=v1010&vkey=%s' % (url_prefix, filename, data['key'])
            except:
                url = '[ERROR]'
            urls.append(url)
 
        print('stream:' + stream['name'])
        for url in urls:
            print(url)
