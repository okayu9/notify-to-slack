import sys
import json
import requests
import fileinput
import configparser

def main():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    if 2 <= len(sys.argv):
        profile = sys.argv[1]
    else:
        profile = "default"

    if profile not in config:
        print("Error: No such profile you specified.", file=sys.stderr)
        sys.exit(1)

    if "webhook_url" not in config[profile]:
        print("Error: webhook_url is not specified.", file=sys.stderr)
        sys.exit(1)
    webhook_url = config[profile]["webhook_url"]

    config_dict = dict(config[profile])
    del config_dict["webhook_url"]

    if "per_line" in config[profile] and config[profile]["per_line"] == "1":
        del config_dict["per_line"]
        for line in fileinput.input("-"):
            config_dict["text"] = line
            requests.post(webhook_url, data=json.dumps(config_dict))
    else:
        config_dict["text"] = "".join(sys.stdin.readlines())
        requests.post(webhook_url, data=json.dumps(config_dict))


if __name__ == "__main__":
    main()
