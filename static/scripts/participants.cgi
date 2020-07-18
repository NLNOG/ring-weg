#!/usr/bin/env python
import random, simplejson, urllib

API="https://api.ring.nlnog.net/1.0/"
PARTICIPANTS=API + '/participants'
NODES=API + '/nodes'

counters = {'orgs': 0, 'nodes': 0, 'asns': 0, 'countries': 0 }
pcounters = {}

print("Content-Type: text/plain\n\n")
try:
    _countries = {}
    _asns = {}
    response = simplejson.load(urllib.urlopen(PARTICIPANTS))
    participants = response['results']['participants']
    response2 = simplejson.load(urllib.urlopen(NODES))
    allnodes = response2['results']['nodes']

    for participant in participants:
        _pmachines = {}
        _pasns = {}
        nodes = filter(lambda x: x['participant'] == participant['id'], allnodes)
        if len(nodes) > 0:
            counters['orgs'] = counters['orgs'] + 1
            pcounters[participant['id']] = {}
            pcounters[participant['id']]['name'] = participant['company']
            pcounters[participant['id']]['url'] = participant['url']
        for node in nodes:
            counters['nodes'] = counters['nodes'] + 1
            pcounters[participant['id']]['logo'] = node['hostname'].split('.')[0][:-2] + '.png'
            _countries[node['countrycode']] = True
            _asns[node['asn']] = True
            _pmachines[node['hostname'].split('.')[0]] = True
            _pasns[node['asn']] = True
        if participant['id'] in pcounters.keys():
            pcounters[participant['id']]['machines'] = _pmachines.keys()
            pcounters[participant['id']]['asns'] = _pasns.keys()

    # Gather total counters
    counters['countries'] = len(_countries.keys())
    counters['asns'] = len(_asns.keys())

except:
    counters['orgs'] = 'NaN'
    counters['nodes'] = 'NaN'
    counters['asns'] = 'NaN'
    counters['countries'] = 'NaN'
    pcounters = {}

print(simplejson.dumps({'counters': counters, 'participants': pcounters}))