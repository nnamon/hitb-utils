import requests
import json

host = "https://192.168.0.117"
cookies = "Teams=close; Leaderboard=close; Announcements=close; Activity=close; Filter=close; Game Clock=close; FBCTF=129f54b3568b7b59a50e42bd8b7477ae"
verify = False
output_dir = "grabbed"

def main():
    # Create the cookie jar and the session
    cj = requests.utils.cookiejar_from_dict(dict(p.split('=') for
                                                 p in cookies.split('; ')))
    session = requests.Session()
    session.cookies = cj

    # Get tasks
    country_data = session.get(host + "/data/country-data.php", verify=verify)
    if country_data.status_code != 200:
        print "Bad cookies"
        exit()
    country_data = json.loads(country_data.text)
    file(output_dir + "/tasks.json", 'w').write(json.dumps(country_data))

    # Get configuration
    config_data = session.get(host + "/data/configuration.php", verify=verify)
    config_data = json.loads(config_data.text)
    file(output_dir + "/config.json", 'w').write(json.dumps(config_data))

    # New list for files
    files = []

    # Output
    os = ""

    # Write a summary
    for i in country_data.keys():
        cdata = country_data[i]
        os += "%s: %s (%s)\n" % (i, cdata['title'], cdata['category'])
        os += "Points: %d (%d)\n" % (cdata['points'], cdata['bonus'])
        os += "Type: %s\n" % cdata['type']
        os += "Completed: %d (%s)\n" % (len(cdata['completed']), cdata['owner'])
        os += "Hint: %s (%d)\n" % (cdata['hint'], cdata['hint_cost'])
        os += "Files:\n"
        for j in range(len(cdata['attachments'])):
            os += "%d. %s\n" % (j+1, cdata['attachments'][j])
            files.append(cdata['attachments'][j])
        os += "Links:\n"
        for j in range(len(cdata['links'])):
            os += "%d. %s\n" % (j+1, cdata['links'][j])
        os += "\n"

    # Write the summary
    file(output_dir + "/summary.txt", 'w').write(os)

    # Get all the files
    for i in files:
        filename = i.split("/")[-1]
        raw = session.get(host + i, verify=verify).content
        file(output_dir + "/" + filename, 'w').write(raw)

if __name__ == "__main__":
    main()
