## ooc.rpy
## 管理 OOC（Out-of-Character / 出戏度）变量
## 范围：0 ~ 100，由选项与小游戏结果增减，影响最终结局

# 当前周目 OOC 值，新游戏时重置，会随存档保存
default ooc = 100

#ooc 上下限
define OOC_MIN = 0
define OOC_MAX = 100

init python:
    def set_ooc(value: int):
        global ooc
        if value < OOC_MIN:
            ooc = OOC_MIN
        elif value > OOC_MAX:
            ooc = OOC_MAX
        else:   
            ooc = value     
