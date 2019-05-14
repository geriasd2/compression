import re

def convertWord(word):
    vowels = ["a", "e", "i", "o", "u"]
    word = re.sub(r"[^a-z]", "", word)
    for char in word:
        if char in vowels:
            return word[0:3]
    return ""


def convertLines(lines):
    timeRegex = r".*?(\[.*?\])"
    agentRegex = r".*\"(.*)\""
    for idx, line in enumerate(lines):
        line = line.lower()
        time = re.search(timeRegex, line).group(1)
        line = line.replace(time, time[1:15])
        agent = re.search(agentRegex, line).group(1)
        agent = agent.split(" ")
        usefulAgentInfo = set()
        for word in agent:
            word = convertWord(word)
            if word:
                usefulAgentInfo.add(word)
        agent = '"{}"'.format(" ".join(agent))
        usefulAgentInfo = "".join(usefulAgentInfo)
        line = line.replace(agent, usefulAgentInfo)
        lines[idx] = line
    return lines
    
    
def categorizeByIp(lines):
    categorized = {}
    ipRegex = r"(\d+\.\d+\.\d+\.\d+) - - "
    for line in lines:
        ip = re.findall(ipRegex, line)[0]
        line =  line.replace(ip + " - - ", "")
        if ip in categorized:
            categorized[ip].append(line)
            continue
        categorized[ip] = [line]
    return categorized

def categorizeByReqType(categorized):
    regularMethodRouteRegex = r"(\"(get|post|head) (\/.*?) (.*?)\")"
    for ip, lines in categorized.items():
        requests = {}
        for line in lines:
            match = re.search(regularMethodRouteRegex, line)
            if not match:
                statusCode = re.search(r".*?\".*?\" (\d+).*", line).group(1)
                if statusCode[0] == "2":
                    if "problem" in requests:
                        requests["problem"].append(line)
                    else:
                        requests["problem"] = [line]
                continue
            method = match.group(2).strip()
            route = match.group(3).strip()
            line = route + re.sub(regularMethodRouteRegex, "", line)
            if method in requests:
                requests[method].append(line)
                continue
            requests[method] = [line]
        categorized[ip] = requests
    return categorized


if __name__ == "__main__":
    with open("access.log.14", "r") as f:
        lines = f.read().strip().split("\n")
    lines = convertLines(lines)
    categorized = categorizeByIp(lines)
    categorized = categorizeByReqType(categorized)

    for ip, v in categorized.items():
        if "problem" in v:
            print(ip)
