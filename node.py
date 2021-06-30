from __future__ import annotations
import time


class Message:
    def __init__(self, writer: Node, content):
        self.likes = 0
        self.forwards = 0
        self.comments = 0
        self.writer = writer
        self.content = content
        self.timestamp = time.time()


class Node:
    def __init__(self, pid):
        self.pid = pid
        self.relationList = []  # 社会关系列表
        self.totalThumb = 0  # 总点赞数
        self.totalComments = 0  # 总评论数
        self.totalForwarding = 0  # 总转发数
        self.influence = 0  # 影响力
        self.receiveList = []  # 接收的文章列表
        self.articles = []  # 自己发布的原创性文章

    def build_relation(self, node: Node):
        self.relationList.append(node.pid)

    def calculate_influence(self):
        self.influence = self.totalForwarding + \
            pow(self.totalComments, 1/2) + pow(self.totalThumb, 1/3)

    def sendMessage(self, message: Message, node: Node):
        node.receiveList.append(message)

    def forwardMessage(self, message: Message):
        message.forwards += 1
        message.writer.totalForwarding += 1
        for i in self.relationList:
            self.sendMessage(message, i)

    def likeMessage(self, message: Message):
        message.likes += 1
        message.writer.totalThumb += 1

    def commitMessage(self, message: Message):
        message.comments += 1
        message.writer.totalComments += 1

    def follow_someone(self, node: Node):
        self.following.append(node)
        node.follower.append(self)


class Viewer(Node):
    def __init__(self):
        super().__init__()
        self.following = []  # 关注了谁

    def forwardMessage(self, message: Message):
        message.forwards += 1
        for i in self.relationList:
            self.sendMessage(message, i)

    def releaseMessage(self, content: str):
        message = Message(self, content)
        self.articles.append(message)
        for i in self.relationList:
            self.sendMessage(message, i)


class Blogger(Node):
    def __init__(self):
        super().__init__()
        self.follower = []  # 谁关注了我

    def forwardMessage(self, message: Message):
        message.forwards += 1
        for i in self.relationList:
            self.sendMessage(message, i)
        for i in self.follower:
            self.sendMessage(message, i)

    def releaseMessage(self, content: str):
        message = Message(self, content)
        self.articles.append(message)
        for i in self.relationList:
            self.sendMessage(message, i)
        for i in self.follower:
            self.sendMessage(message, i)