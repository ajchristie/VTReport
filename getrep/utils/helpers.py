import requests
from time import sleep
#from importlib import import_module
from VTReport.settings import api_key
#from django.conf import settings
from getrep.models import VTReport
#SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

def prune_and_dummy(hashlist, sess):
    """ Given a list of hash digests, prunes the list of hashes for which records are already present in the database and leaves a list of hashes that should be submitted to VirusTotal. """

    for x in hashlist:
        h= hashtype(x)
        if VTReport.objects.filter(h=x).exists():
            VTReport.objects.get(h=x).sessions.add(sess)
            hashlist.pop(x)


def cache_grab(sess):
    """ Passed a session, collects the previously cached records from the database and returns them in a list. """

    recset = sess.vtreport_set.all() # this is a Queryset
    return recset[::1] # slice evaluates the QS and returns a list; might be good to delay this

def make_rec(json_rec):
    """ Creates a database entry from the passed json record as obtained from VirusTotal and returns it. """

    if json_rec['response_code'] == 1:
        return VTReport(num_engines=json_rec['total'],
                        md5= json_rec['md5'], sha1=json_rec['sha1'], sha256=json_rec['sha256'], fortinet_name= json_rec['scans']['Fortinet']['result'] if json_response['scans']['Fortinet']['detected'] else "No name", scandate=json_response['scan_date'],
                        res_code=1)
    else:
        return VTReport(hashtype(json_rec['resource'])=json_rec['resource'],
                        res_code=json_response['response_code'])

def hashtype(digest):
    """ Determines (based solely on length) and returns as a string the hashtype of a digest. """

    if len(digest) == 32:
        return 'md5'
    elif len(digest) == 40:
        return 'sha1'
    elif len(digest) == 62:
        return 'sha256'
    else:
        return 'unk'

def get_is(thelist, i):
    return [x[i] for x in thelist]
