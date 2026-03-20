default ooc = 20
default cheat_count = 0

init python:
    def set_ooc(value):
        """绝对值设置 OOC"""
        # 用 store 变量，兼容 Ren'Py rollback。
        store.ooc = max(0, min(100, value))
        check_ooc_death()

    def add_ooc(amount):
        """相对增减 OOC (正数为增加，负数为减少)，避免Screen提前求值陷阱"""
        # 用 store 变量，避免直接 global 带来的状态同步问题。
        store.ooc = max(0, min(100, store.ooc + amount))
        check_ooc_death()

    def check_ooc_death():
        """将死亡检测独立，避免在Screen执行环境中的栈残留"""
        if store.ooc >= 100:
            # 先隐藏 HUD，避免跳转 BE 时残留在屏幕上。
            renpy.hide_screen("ooc_overlay")
            renpy.jump("be")
