#dfa算法 用来判断该字段是否是一个体检项目
import os
SensitiveWord_Path = "worddata.txt"
class DFA(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定
        self.parse(SensitiveWord_Path)

    def add(self, keyword):
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:  # 最后一个字
            level[self.delimit] = 0
        # print(level)

    def parse(self, path):
        with open(path, encoding='utf-8') as f:
            for keyword in f:
                keyword = keyword.replace('\n', '')
                self.add(str(keyword).strip())

    def filter(self, message, repl="*"):
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    # 特定字符不在当前字的value值里，嵌套遍历下一个
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        return True
            start += 1
        return False