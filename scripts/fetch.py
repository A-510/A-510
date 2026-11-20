"""Collect the numbers the page shows. Every call is optional: on failure the default stays."""
import os, json, sys, urllib.request, datetime
U = os.environ.get("GH_USER", "A-510"); T = os.environ.get("GITHUB_TOKEN")
def get(p):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-build"}
    if T: h["Authorization"] = "Bearer " + T
    return json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/" + p, headers=h), timeout=30))
d = {"user": U, "stars": 0, "followers": 0, "repos": 0, "pushes": 0, "push_repos": 0, "last_repo": "", "langs": []}
try:
    u = get(f"users/{U}"); d["followers"] = u["followers"]; d["repos"] = u["public_repos"]
except Exception as e: print("user:", e)
try:
    it = get(f"search/repositories?q=user:{U}+fork:false&sort=stars&per_page=100")["items"]
    d["stars"] = sum(i["stargazers_count"] for i in it)
    w = {}
    for i in it:
        if i.get("language"): w[i["language"]] = w.get(i["language"], 0) + 1 + i["stargazers_count"] ** .5
    tot = sum(w.values()) or 1
    d["langs"] = [(k, round(v / tot, 4)) for k, v in sorted(w.items(), key=lambda x: -x[1])[:6]]
except Exception as e: print("repos:", e)
try:
    cut = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24); seen = []
    for page in (1, 2, 3):
        ev = get(f"users/{U}/events/public?per_page=100&page={page}")
        if not ev: break
        for e in ev:
            if e["type"] != "PushEvent": continue
            when = datetime.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00"))
            name = e["repo"]["name"].split("/")[-1]
            if not d["last_repo"] and name != U: d["last_repo"] = name
            if when >= cut: d["pushes"] += 1; seen.append(name)
    d["push_repos"] = len(set(seen))
except Exception as e: print("events:", e)
d["activity"] = d["pushes"]
try:
    q = {"query": 'query{user(login:"%s"){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}' % U}
    r = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(q).encode(), headers={"Authorization": "Bearer " + (T or ""), "User-Agent": "profile-build"})
    weeks = json.load(urllib.request.urlopen(r, timeout=30))["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [x for w in weeks for x in w["contributionDays"]]
    d["activity"] = sum(x["contributionCount"] for x in days[-2:])
except Exception as e: print("calendar:", e)
json.dump(d, open(sys.argv[1], "w")); print(d)
