import requests
from time import sleep
#from importlib import import_module
from VTReport.settings import api_key
#from django.conf import settings
from getrep.models import VTReport

#SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

def prune_and_dummy(hashlist):
    """ Given a list of hash digests, prunes the list of hashes for which records are already present in the database and leaves a list of hashes that should be queried. A dummy record with response code -99 is added to the database for any hash without a cached record. """

    for x in hashlist:
        h= hashtype(x)
        if VTReport.objects.filter(h=x).exists():
            hashlist.pop(x)
        else:
            VTReport(h=x, res_code=-99).save()


def cache_grab(hashlist):
    """ Passed a list of hashes, collects the corresponding records from the database and returns them in a list. """

    reclist = []
    cached = VTReport.objects.none() ## WHY???
    for x in hashlist:
        h = hashtype(x)
        if VTReport.objects.filter(h=x).exists(): ## do a try: get this and then just pass the DoesNotExist exception instead
            reclist.append((VTReport.objects.get(h=x))
        # if len(x) == 32:
        #     if VTReport.objects.filter(md5=x).exists():
        #         reclist.append((VTReport.objects.filter(md5=x).values(), hashlist.pop(x)))
        # elif len(x) == 40:
        #     if VTReport.objects.filter(sha1=x).exists():
        #         reclist.append((VTReport.objects.filter(sha1=x).values(), hashlist.pop(x)))
        # elif len(x) == 64:
        #     if VTReport.objects.filter(sha256=x).exists():
        #         reclist.append((VTReport.objects.filter(sha256=x).values(), hashlist.pop(x)))

    return reclist

def make_rec(json_rec):
    """ Creates a database entry from the passed json record as obtained from VirusTotal and returns it. """

    if json_rec['response_code'] == 1:
        return VTReport(num_engines=json_response['total'], md5= json_response['md5'], sha1=json_response['sha1'], sha256=json_response['sha256'],
        fortinet_name= json_response['scans']['Fortinet']['result'] if json_response['scans']['Fortinet']['detected'] else "No name",
        scandate=json_response['scan_date'],
        res_code=1)
    else:
        return VTReport(hashtype(json_response['resource'])=json_response['resource'], res_code=json_response['response_code'])

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
