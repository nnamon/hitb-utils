import requests
import json
import urllib

host = "https://pad.spro.ink"
apikey = "7e5b927d259e3f97235ec1418f9bcd3efe6737a8121d2fa3e2f331d277185c6c"
verify = False
header = {"X-Apikey": apikey}
input_dir = "grabbed"
ctf_id = 8
e_apikey = "ecb17837c120b101fad678e9718721967596eed77fb1a46a9ecb1b5da3d0ddfe"
e_host = "https://pad.spro.ink:1235"
e_cookies = "ctfpad_hide=false; ctfpad=1be6aa4e60aac96b19cb2adaabca1c74; language=en-gb; express_sid=s%3AEOko2ot1sUnNANBb_5F7bJO2CeB_UEDs.IHxjUjjmgK607208vaI8Y%2BT0MTOeFhL7g%2FAIKZkHM%2FA; token=t.fZLXPGniB8d6q5YsVxWh; test=test"
cj = requests.utils.cookiejar_from_dict(dict(p.split('=') for
                                             p in e_cookies.split('; ')))
esession = requests.Session()
esession.cookies = cj

def get(path):
    return requests.get(host + path, headers=header, verify=verify)

def post(path, json_data):
    return requests.post(host + path, headers=header, verify=verify,
                         json=json_data)

def post_file(path, file_dict):
    return requests.post(host + path, headers=header, verify=verify,
                         files=file_dict)

def create_pad(pad_id, text):
    query = e_host
    query += "/api/1/createPad?apikey=" + e_apikey
    query += "&padID=" + pad_id
    query += "&text=" + urllib.quote(text)
    return esession.get(query, verify=verify)

def main():
    # Get the whoami
    whoami = get("/user/whoami")
    whoami = json.loads(whoami.text)['username']
    print "Who I am: %s" % whoami

    # Get team
    teamname = json.loads(file(input_dir + "/config.json").read())
    teamname = teamname['currentTeam']
    print "Team: %s" % teamname

    # Get CTF
    ctf = json.loads(get("/ctfs/%d" % ctf_id).text)
    ctf = ctf['ctf']
    print "CTF %d: %s" % (ctf['id'], ctf['name'])

    # Get available tasks on server
    existing_tasks = []
    tasks_req = get("/ctfs/%d/challenges" % ctf_id)
    tasks_req = json.loads(tasks_req.text)
    for i in tasks_req['challenges']:
        country = i['title'].split(": ")[0]
        existing_tasks.append(country)

    # Build challenge profile
    challenges = json.loads(file(input_dir + "/tasks.json").read())

    # Upload new tasks
    for i in challenges.keys():
        if i in existing_tasks:
            continue
        # Create new task
        cdata = challenges[i]
        new_task = {"challenge": {
            "title": "%s: %s" % (i, cdata['title']),
                        "category": cdata['category'],
                        "points": cdata['points']
                        }
                    }
        challenge = post("/ctfs/%d/challenges" % ctf_id, new_task)
        challenge = json.loads(challenge.text)
        challenge = challenge['challenge']
        chal_id = challenge['id']

        # Files to upload
        files = []

        # Create new pad
        os = ""
        os += "%s: %s (%s)\n" % (i, cdata['title'], cdata['category'])
        os += "Points: %d (%d)\n" % (cdata['points'], cdata['bonus'])
        os += "Type: %s\n" % cdata['type']
        os += "Completed: %d (%s)\n" % (len(cdata['completed']), cdata['owner'])
        os += "Hint: %s (%d)\n" % (cdata['hint'], cdata['hint_cost'])
        os += "Files:\n"
        for j in range(len(cdata['attachments'])):
            os += "%d. %s\n" % (j+1, cdata['attachments'][j])
            files.append(cdata['attachments'][j].split("/")[-1])
        os += "Links:\n"
        for j in range(len(cdata['links'])):
            os += "%d. %s\n" % (j+1, cdata['links'][j])
        os += "\n"
        p = create_pad("challenge%d" % chal_id, os)
        print os

        # Upload the files
        for j in files:
            files = {'files': open("%s/%s" % (input_dir, j),'rb')}
            x = post_file('/challenges/%d/files' % chal_id, files)


if __name__ == "__main__":
    main()
