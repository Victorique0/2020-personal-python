import json
import os
import argparse
from time import *
#Date 类：用于处理 json 数据和返回指令要求的数据
class Data:
    def __init__(self, dict_address : str = None, reload : int = 0):
        if reload == 1:
            # reload=1 即初始化的时候执行
            self.__init(dict_address)
        # dict_address为Node意味着执行的不是init指令，此时如果在文件中找不到init操作生成的json文件的话意味着出现错误
        if dict_address is None and not os.path.exists("ver2.json"):
            raise RuntimeError("error: init failed")
        # 打开 init 操作所生成的 json 文件，并将其读取到 Date 类的数据成员 json 中
        x = open('ver2.json', 'r', encoding='utf-8').read()
        self.json = json.loads(x)

    def __init(self,dict_address):
        # 存储的 json 数据中每一项都是以 user:{repo1:{event1:(int), event2:(int)...},repo2:{...},... } 格式存储， 整个json文件只有一条 json 数据
        user_repo_event = {}
        # 遍历整个文件夹，找到所有后缀为 .json 的文件
        for root, dic, files in os.walk(dict_address):
            for f in files:
                if f[-5:] == ".json":
                    event = ["PushEvent","IssueCommentEvent","IssuesEvent","PullRequestEvent"]
                    #print("读取" + str(f))
                    json_path = f
                    # 用 readlines 读取周到的 json 文件， 将每一条 json 数据转化为 string 并存到列表中
                    x = open(dict_address + "/" + json_path, "r", encoding="UTF-8").readlines()
                    for i in x:
                        # 将每一个 string 转化为 json 数据并中分析出有用的参数，按照上述的格式存储到 user_repo_event 中
                        i = json.loads(i)
                        if i["type"] in event:
                            self.add_user_repo_event(i, user_repo_event)
        # 将处理好的数据保存为另一个文件，以便于后续指令调用
        with open("ver2.json", "a") as f_json:
            json.dump(user_repo_event, f_json)

    # 将读取到的一条 json 数据进行处理并存入 user_repo_event 中
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

    def analysis(self,user=None,repo=None,event=None):
        num = 0
        if user:
            if repo:
                return self.json[user][repo][event]
            else:
                dic = self.json[user]
                for key in dic:
                    num += dic[key][event]
                return num
        else:
            for key in self.json:
                if repo in self.json[key]:
                    num += self.json[key][repo][event]
            return num

#Run 类：用于接收指令并传递给 Date 类执行
class Run:
    def __init__(self):
        # 添加命令行参数
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-i', '--init',type=str)
        self.parser.add_argument('-u', '--user',type=str)
        self.parser.add_argument('-r', '--repo',type=str)
        self.parser.add_argument('-e', '--event',type=str)
        self.next()

    # 根据接收到的参数来判断时哪种指令并返回指令要求的数据
    def next(self):
        args = self.parser.parse_args()
        if args.init:
            date = Data(args.init, 1)
        else:
            data = Data()
            print(data.analysis(user=args.user, repo=args.repo, event=args.event))

if __name__ == '__main__':
    a = Run()
