## ooc.rpy
## 管理 OOC（Out-of-Character / 出戏度）变量
## 范围：0 ~ 100，由选项与小游戏结果增减，影响最终结局

# 当前周目 OOC 值，新游戏时重置，会随存档保存
default ooc = 0

#ooc 上下限
define OOC_MIN = 0
define OOC_MAX = 100

#增加ooc值
init python:
    def add_ooc(value):
        global ooc
        ooc = max(OOC_MIN, min(ooc + value, OOC_MAX))

#减少ooc值
init python:
    def subtract_ooc(value):
        global ooc
        ooc = max(OOC_MIN, min(ooc - value, OOC_MAX))

#获取ooc值
init python:
    def get_ooc():
        return ooc