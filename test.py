import json

class ExamOCR():
    def __init__(self, dfa, path):
        with open(path, 'rb') as f:
            data = json.load(f)
            self.data_l = [words['text'] for words in data['data']['ocr_comm_res']['items'] if words['text'] not in ['↑', '↓', '标志']]
            self.dfa = dfa

    def main_logic(self):
        starter = ['项目名称', '检验项目']
        starter_index = 0
        value = ['结果', '测定结果']
        value_index = 0

        # 找到starter的index
        for i in range(len(self.data_l)):
            if self.data_l[i] in starter:
                # print(i)
                if (starter_index != 0):
                    raise Exception('multiple starter found 不支持的格式')
                starter_index = i
            if self.data_l[i] in value:
                # print(i)
                if (value_index != 0):
                    raise Exception('multiple value found 不支持的格式')
                value_index = i

        if (starter_index == 0 or value_index == 0 or (value_index <= starter_index)):
            raise Exception('starter or value not found')

        # 确定有多少列
        column_names = starter + value
        column_names += ['英文名称', '代码', '英文缩写', '缩写']
        column_names += ['单位']
        column_names += ['参考范围', '参考区间']
        column_names += ['检测方法\仪器']
        column_num = 0
        for i in range(len(self.data_l)):
            if self.data_l[i] in column_names:
                column_num += 1

        gap = value_index - starter_index
        line_length = column_num

        def remove_special_ch(s):
            sp_ch = [' ', '↑', '↓', '★', '*']
            for ch in sp_ch:
                s = s.replace(ch, '')
            return s

        def convert_str_to_num(s):
            try:
                return float(s)
            except ValueError:
                return 0
        
        dic = {}
        # 从starter_index开始，每隔gap个，取一个值，然后增加line_length个
        # for j in range(starter_index + line_length, len(self.data_l), line_length):
        #     k = remove_special_ch(self.data_l[j])

        #     if (j + gap > len(self.data_l)):
        #         raise Exception('not a valid item')
        #     v = remove_special_ch(self.data_l[j + gap])
        #     #可能是到结尾了或者识别错误
        #     if (not self.dfa.filter(k)):
        #         # print(k)
        #         print('识别到非检测项目, 可能是到结尾或者OCR结果错误:' + k)
        #     dic[k] = v
        
        # 遍历所有词，当获取到dfa通过的词时，增加gap个获取值
        for j in range(starter_index + line_length, len(self.data_l)):
            k = remove_special_ch(self.data_l[j])
            if (self.dfa.filter(k)):
                # print(k)
                # print('识别到非检测项目, 可能是到结尾或者OCR结果错误:' + k)
                if (j + gap >= len(self.data_l)):
                    dic[k] = 0
                    break
                v = remove_special_ch(self.data_l[j + gap])
                dic[k] = convert_str_to_num(v)

        return dic

from dfa import DFA 

ocr = ExamOCR(DFA(), 'C://Users//bale//Documents//报告及解析结果20231209/报告5.json')
result = ocr.main_logic()
for _r in result:
    print(_r, result[_r])

with open('结果5.txt', 'w') as f:
    for _r in result:
        f.write(_r + ": " + str(result[_r]) + "\n")