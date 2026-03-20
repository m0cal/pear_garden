default ooc = 20
default cheat_count = 0

init python:
    def set_ooc(value):
        """绝对值设置 OOC"""
        global ooc
        ooc = max(0, min(100, value))
        check_ooc_death()

    def add_ooc(amount):
        """相对增减 OOC (正数为增加，负数为减少)，避免Screen提前求值陷阱"""
        global ooc
        ooc = max(0, min(100, ooc + amount))
        check_ooc_death()

    def check_ooc_death():
        """将死亡检测独立，避免在Screen执行环境中的栈残留"""
        global ooc
        if ooc >= 100:
            renpy.jump("be")
