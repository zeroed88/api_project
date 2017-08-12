import requests

#ROOT_URL = 'http://192.168.0.201/ExpressApi/hs/'
ROOT_URL = 'http://91.144.162.221:6405/ExpressApi/hs/'
PERCENT_URL ='Percents/'
CRED = ('admin', 'admin')


def getPercent(zalog, lastName):
    queryStr = r'{rt}{url}{ln}/{zg}'.format(
            rt=ROOT_URL,
            url=PERCENT_URL,
            ln=lastName,
            zg=zalog
        )
    r = requests.get(queryStr, auth=CRED)
    if r.status_code == 200:
        return r.json()
    else:
        raise ValueError('Bad input data')
