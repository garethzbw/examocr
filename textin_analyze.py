import json
import re
from dfa import DFA 

class TableResult(object):
    def __init__(self, no):
        self.no = no
        self.cate = ''
        self.result = -1
        self.range = ''
        self.unit = ''
    def check(self):
        return self.cate and self.result != -1 and self.range and self.unit
    def __str__(self) -> str:
        return f'{self.no}: {self.cate}: {self.result} {self.range} {self.unit}'

class textAnalyze(object):
    def __init__(self, jsonObj) -> None:
        self.data = jsonObj
        self.category_text = ['项目名称', '检验项目']
        self.result_text = ['结果', '测定结果']
        self.range_text = ['参考范围', '参考区间']
        self.unit_text = ['单位']
        self.category_col_start = -1
        self.category_col_end = -1
        self.result_col = -1
        self.range_col = -1
        self.unit_col = -1
        self.dfa = DFA()
    
    # def remove_special_ch(self, s):
    #         sp_ch = [' ', '↑', '↓', '★', '*', '-']
    #         for ch in sp_ch:
    #             s = s.replace(ch, '')
    #         return s
    
    def remove_special_ch(self, s):
        return re.sub(r'[^a-zA-Z\u4e00-\u9fa5()/\\]', '', s)

    def remove_nondigits(self, s):
        return re.sub(r'[^\d.]', '', s)

    def convert_str_to_num(self, s):
        try:
            return float    (s)
        except ValueError:
            return 0
    
    def is_match(self, s, words):
        for word in words:
            if word in s:
                return True
        return False

    def find_col(self, cell):
        # if (cell['start_col'] != cell['end_col']):
        #     return
        if (self.is_match(cell['text'], self.category_text)):
            self.category_col_start = cell['start_col']
            self.category_col_end = cell['end_col']
        elif (self.is_match(cell['text'], self.result_text)):
            self.result_col = cell['start_col']
        elif (self.is_match(cell['text'], self.range_text)):
            self.range_col = cell['start_col']
        elif (self.is_match(cell['text'], self.unit_text)):
            self.unit_col = cell['start_col']
    
    def do(self):
        rt = []
        for table in self.data['result']['tables']:
            if table['type'] in ['table_without_line', 'table_with_line']:
                for cell in table['table_cells']:
                    self.find_col(cell)
                if (self.category_col_start == -1 or self.category_col_end == -1 or self.result_col == -1 or self.range_col == -1 or self.unit_col == -1):
                    continue #可能有多个表格
                row = -1
                t = TableResult(-1)
                for cell in table['table_cells']:
                    # if (cell['start_row'] != row):
                    #     row = cell['start_row']
                    #     print (row, ": ", category, result, range, unit)

                    # if (category and result and range and unit):
                    #     print (row, ": ", category, result, range, unit)
                    #     category = ''
                    #     result = ''
                    #     range = ''
                    #     unit = ''

                    if (cell['start_col'] == self.category_col_start or cell['end_col'] == self.category_col_end):
                        if (t.check()):
                            rt.append(t)
                            t = TableResult(-1)

                        k = self.remove_special_ch(cell['text'])
                        if (self.dfa.filter(k)):
                            t = TableResult(cell['start_row'])
                            row = cell['start_row']
                            t.cate = k
                        else:
                            print (f'category dont match: {k}, ignore row', cell['start_row'])
                    elif (cell['start_col'] == self.result_col and cell['start_row'] == row): # 取同一行数据
                        result = self.convert_str_to_num(self.remove_nondigits(cell['text']))
                        t.result = result
                    elif (cell['start_col'] == self.range_col and cell['start_row'] == row):
                        t.range = cell['text']
                    elif (cell['start_col'] == self.unit_col and cell['start_row'] == row):
                        t.unit = cell['text']
                if (row != -1 and t.check()):
                    # print (row + 1, ": ", category, result, range, unit)
                    rt.append(t)
        return rt

if __name__ == "__main__":
    with open('E:\\code\\report\\examocr\\result\\6.json', 'rb') as f:
        data = json.load(f)
    t = textAnalyze(data)
    l = t.do()
    for ll in l:
        print (ll)