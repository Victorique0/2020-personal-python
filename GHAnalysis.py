import json
import os
import argparse
class Date:
    def __init__(self, dict_address : str = None, reload : int = 0):
        if reload == 1:
            self.__init(dict_address)
        if dict_address is None and not os.path.exists("1.json") and not os.path.exit("2.json") and not os.path.exists("3.path"):
            raise RuntimeError("error: init failed")
        x = open('1.json', 'r', encoding='utf-8').read()
        self.__4Events4PerP = json.loads(x)
        x = open('2.json', 'r', encoding='utf-8').read()
        self.__4Events4PerR = json.loads(x)
        x = open('3.json', 'r', encoding='utf-8').read()
        self.__4Events4PerPPerR = json.loads(x)

    def get_user_event(self):
        return self.__4Events4PerP

    def get_repo_event(self):
        return self.__4Events4PerR

    def get_user_repo_event(self):
        return  self.__4Events4PerPPerR

    def __init(self,dict_address):
        json_list = []
        for root, dic, files in os.walk(dict_address):
            for f in files:
                if f[-5:] == ".json":
                    user_event = {}
                    repo_event = {}
                    user_repo_event = {}
                    event = ["PushEvent","IssueCommentEvent","IssuesEvent","PullRequestEvent"]
                    json_path = f
                    x = open(dict_address + "\\" + json_path, "r", encoding="UTF-8").readlines()
                    num = 0
                    for i in x:
                        i = json.loads(i)
                        if i["type"] in event:
                            self.add_user_event(i, user_event)
                            self.add_repo_event(i, repo_event)
                            self.add_user_repo_event(i, user_repo_event)
                    with open("./1.json", "a") as f:
                        f.write(json.dumps(user_event))
                    with open("./2.json", "a") as f:
                        json.dump(repo_event,f)
                    with open("./3.json", "a") as f:
                        json.dump(user_repo_event, f)

    def add_user_event(self, dic, user_event):
        id = dic["actor"]["id"]
        event = dic["type"]
        if id not in user_event:
            user_event[id] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_event[id][event] += 1

    def add_repo_event(self, dic, user_event):
        repo = dic["repo"]["id"]
        event = dic["type"]
        if repo not in user_event:
            user_event[repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_event[repo][event] += 1

    def add_user_repo_event(self, dic, user_repo_event):
        id = dic["actor"]["id"]
        repo = dic["repo"]["id"]
        event = dic["type"]
        if id not in user_repo_event:
            user_repo_event[id] = {}
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        if repo not in user_repo_event[id]:
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_repo_event[id][repo][event] += 1


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
            json = date.get_user_event()
            #print(json[args.user])
            print(json[args.user][args.event])
        elif args.repo and args.event and not args.user:
            date = Date()
            json = date.get_repo_event()
            #print(json[args.repo])
            print(json[args.repo][args.event])
        elif args.user and args.repo and args.event:
            date = Date()
            json = date.get_user_repo_event()
            #print(json[args.user][args.repo])
            print(json[args.user][args.repo][args.event])


if __name__ == '__main__':
    a = Run()
