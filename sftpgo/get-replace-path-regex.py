from urllib.request import urlopen
import re
import json

sftpgo_version = json.loads(input())["sftpgo_version"]

url = f"https://raw.githubusercontent.com/drakkan/sftpgo/{sftpgo_version}/internal/httpd/httpd.go"
with urlopen(url) as response:
    content: str = response.read().decode("utf-8")
    output = {}
    output["replace_admin_path_regex"] = "^/({})".format(
        "|".join(re.findall(r'"/web/admin/(.*)"', content))
    )
    output["replace_client_path_regex"] = "^/({})".format(
        "|".join(re.findall(r'"/web/client/(.*)"', content))
    )
    print(json.dumps(output))
