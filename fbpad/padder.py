import requests
import json

host = "https://pad.spro.ink"
apikey = "7e5b927d259e3f97235ec1418f9bcd3efe6737a8121d2fa3e2f331d277185c6c"
verify = False
header = {"X-Apikey": apikey}
input_dir = "grabbed"
ctf_id = 2

def get(path):
    return requests.get(host + path, headers=header, verify=verify)

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
    ctf = json.loads(get("/ctfs/%d" % ctf_id))
    print "CTF %d: %s" % (ctf['id'], ctf['name'])

    # Get available tasks on server
    existing_tasks = []
    tasks_req = get("/ctfs/%d/challenges")
    tasks_req = json.loads(tasks_req)
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
        # Create new pad
        os = ""
        cdata = challenges[i]
        os += "%s: %s (%s)\n" % (i, cdata['title'], cdata['category'])
        os += "Points: %d (%d)\n" % (cdata['points'], cdata['bonus'])
        os += "Type: %s\n" % cdata['type']
        os += "Completed: %d (%s)\n" % (len(cdata['completed']), cdata['owner'])
        os += "Hint: %s (%d)\n" % (cdata['hint'], cdata['hint_cost'])
        os += "Files:\n"
        for j in range(len(cdata['attachments'])):
            os += "%d. %s\n" % (j+1, cdata['attachments'][j])
            # Upload file
        os += "Links:\n"
        for j in range(len(cdata['links'])):
            os += "%d. %s\n" % (j+1, cdata['links'][j])
        os += "\n"
        print os





if __name__ == "__main__":
    main()
