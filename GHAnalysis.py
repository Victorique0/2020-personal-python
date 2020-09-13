import json
import os
import argparse
class Date:
    def __init__(self, dict_address : str = None, reload : int = 0):
        if reload == 1:
            self.__init(dict_address)
        if dict_address is None and not os.path.exists("ver2.json"):
            raise RuntimeError("error: init failed")
        x = open('ver2.json', 'r', encoding='utf-8').read()
        self.json = json.loads(x)

    def __init(self,dict_address):
        for root, dic, files in os.walk(dict_address):
            for f in files:
                if f[-5:] == ".json":
                    user_repo_event = {}
                    event = ["PushEvent","IssueCommentEvent","IssuesEvent","PullRequestEvent"]
                    json_path = f
                    x = open(dict_address + "\\" + json_path, "r", encoding="UTF-8").readlines()
                    num = 0
                    for i in x:
                        i = json.loads(i)
                        if i["type"] in event:
                            self.add_user_repo_event(i, user_repo_event)
                    with open("./ver2.json", "a") as f_json:
                        json.dump(user_repo_event, f_json)

    def add_user_repo_event(self, dic, user_repo_event):
        id = dic["actor"]["login"]
        repo = dic["repo"]["name"]
        event = dic["type"]
        if id not in user_repo_event:
            user_repo_event[id] = {}
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        if repo not in user_repo_event[id]:
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_repo_event[id][repo][event] += 1

    def get_user_event(self, user, event):
        dict = self.json[user]
        num = 0
        for key in dict:
            num += dict[key][event]
        return num

    def get_repo_event(self, repo, event):
        num = 0
        for key in self.json:
            if repo in self.json[key]:
                num += self.json[key][repo][event]
        return num

    def get_user_repo_event(self, user, repo, event):
        return self.json[user][repo][event]


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user',type=str)
        self.parser.add_argument('-r', '--repo',type=str)
        self.parser.add_argument('-e', '--event',type=str)
        self.next()

    def next(self):
        args = self.parser.parse_args()
        if args.init:
            print("init")
            date = Date(args.init, 1)
        elif args.user and args.event and not args.repo:
                date = Date()
                print(date.get_user_event(args.user, args.event))
        elif args.repo and args.event and not args.user:
                date = Date()
                print(date.get_repo_event(args.repo, args.event))
        elif args.user and args.repo and args.event:
                date = Date()
                print(date.get_user_repo_event(args.user, args.repo, args.event))

if __name__ == '__main__':
    a = Run()