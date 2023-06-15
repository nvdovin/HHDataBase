import requests


my_url = "https://dev.hh.ru/admin"
authorization_code = "JTKNPR59R5BUDR9PLP9C8C43MDBNI6Q6FG57Q62I8LPLBDBSBKDL2EHQTUT3PVGT"
client_id = "VVA1DE9SJFT10F1I2UFFK6QKUD17O4U6FSCK36IT2S0NQFJBMJ7N1N67PKS2AP0T"
client_secret = "GVNLR2P9QVNE957TUKH2EBBPMBCQHPEU4V7LPM9GMCG2HSBKL5P9M8CKBNC5NJ4T"
get_request = "https://hh.ru/oauth/token"

params = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authorization_code,
    "redirect_uri": my_url
}

data = requests.post(
    get_request,
    params=params
)
