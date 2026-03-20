# 汉字描红（婚书两字）
# 返回： "success" 或 "cheat"（失败不 return，而是强制重试直到成功或作弊）

# 测试用：为 True 时用半透明色标出计分区域（默认关闭）
default show_hit_debug = False

init python:
    import time
    import pygame
    # 计分区域：(x1,y1,x2,y2) 1920x1080，全部收在“婚”“书”笔画内，不超出字外。
    HANZI_BOXES = [
        # ——“婚”字——
        # 女部（下压一点贴字，不悬空）
        (1002, 358, 1068, 398), (992, 388, 1078, 438), (982, 418, 1088, 468),
        (972, 448, 1098, 498), (982, 478, 1088, 538), (992, 508, 1078, 558),
        (1002, 538, 1068, 578), (1012, 568, 1058, 618),
        # 昏部（左收、上缘下压，不超出字右和字上）
        (912, 348, 1078, 408), (902, 388, 1088, 448), (892, 428, 1098, 488),
        (882, 468, 1108, 528), (902, 498, 1088, 558), (892, 538, 1098, 598),
        (882, 578, 1108, 638), (902, 608, 1088, 658), (912, 638, 1078, 668),
        (922, 658, 1038, 678), (912, 668, 1078, 688),
        # ——“书”字（收窄、底边上收，不超出字左右和字下）——
        # 上横
        (762, 378, 938, 418), (772, 398, 928, 438),
        # 竖
        (842, 418, 898, 468), (832, 458, 908, 518), (842, 498, 898, 548),
        (832, 538, 908, 578),
        # 中横
        (762, 458, 938, 498), (772, 478, 928, 518),
        # 下横
        (762, 538, 938, 578), (772, 558, 928, 598),
        # 左下点
        (752, 568, 828, 608), (742, 588, 838, 638), (752, 618, 818, 658),
        # 右下点
        (862, 568, 938, 608), (852, 588, 948, 638), (862, 618, 928, 658),
    ]

    def _in_box(x, y, box):
        x1, y1, x2, y2 = box
        return (x1 <= x <= x2) and (y1 <= y <= y2)

    # 按下状态（用 store 变量保存）
    if not hasattr(store, "_hanzi_down"):
        store._hanzi_down = False

    def _hanzi_disable_skip():
        """婚书小游戏显示时：关闭快进并标记正在小游戏（用于隐藏快捷菜单）"""
        store._skipping = False
        store._in_hanzi_trace = True

    def _hanzi_enable_skip():
        """婚书小游戏关闭时恢复"""
        store._skipping = True
        store._in_hanzi_trace = False

    # 可写字区域：仅在此矩形内按下/拖动才描红，之外点击不会触发写字（按钮可正常点）
    WRITE_ZONE = (750, 300, 1150, 680)  # (x1, y1, x2, y2) 覆盖中间“婚书”两字

    def _hanzi_in_write_zone(x, y):
        x1, y1, x2, y2 = WRITE_ZONE
        return (x1 <= x <= x2) and (y1 <= y <= y2)

    def _hanzi_score(scr):
        total = len(HANZI_BOXES)
        hit_n = len(scr.scope["hit"])
        return (hit_n * 100.0) / total if total else 0.0

    def _hanzi_sample_mouse():
        scr = renpy.get_screen("hanzi_trace")
        if scr is None:
            return
        x, y = renpy.get_mouse_pos()
        try:
            left_down = pygame.mouse.get_pressed()[0]
        except Exception:
            left_down = False
        # 仅在“写字区内且左键按住”时描红，否则不记录；不按左键时结束当前笔划
        if not left_down:
            store._hanzi_down = False
            return
        if not _hanzi_in_write_zone(x, y):
            return
        store._hanzi_down = True

        # 记录轨迹点（用于画笔迹）
        if "points" in scr.scope:
            scr.scope["points"].append((x, y))
            # 限制数量避免卡顿
            if len(scr.scope["points"]) > 800:
                scr.scope["points"].pop(0)

        hit = scr.scope["hit"]
        for i, box in enumerate(HANZI_BOXES):
            if i in hit:
                continue
            if _in_box(x, y, box):
                hit.add(i)

    def _hanzi_submit():
        scr = renpy.get_screen("hanzi_trace")
        if scr is None:
            return

        score = _hanzi_score(scr)

        # 成功：≥80%
        if score >= 80.0:
            add_ooc(-20)
            renpy.notify("OOC 值大幅降低（-20）")
            renpy.hide_screen("hanzi_trace")
            renpy.return_statement("success")
            return

        # 失败：<60%
        if score < 60.0:
            add_ooc(10)
            renpy.notify("字迹歪歪扭扭（OOC +10），重写！")
            _hanzi_reset()
            return

        # 60%~79%：不算失败，提示继续写
        renpy.notify("还差一点（≥80% 才算完成），继续描红。")

    def _hanzi_reset():
        scr = renpy.get_screen("hanzi_trace")
        if scr is None:
            return
        scr.scope["hit"] = set()
        scr.scope["points"] = []
        scr.scope["start_t"] = time.time()
        scr.scope["elapsed"] = 0.0
        scr.scope["overtime_added"] = 0

    def _hanzi_cheat_do():
        """一键开挂的副作用：OOC、通知、计数（界面由 Return 关闭）"""
        global cheat_count
        cheat_count += 1
        add_ooc(-50)
        renpy.notify("外挂生效：自动完成（OOC -50）")

    def _hanzi_overtime_tick():
        scr = renpy.get_screen("hanzi_trace")
        if scr is None:
            return

        elapsed = scr.scope["elapsed"]
        if elapsed <= 60.0:
            return

        # 超时：+5%/秒，累计最多 +30%
        if scr.scope["overtime_added"] >= 30:
            return

        can_add = min(5, 30 - scr.scope["overtime_added"])
        scr.scope["overtime_added"] += can_add
        add_ooc(can_add)

        if ooc >= 70:
            renpy.notify("OOC 已超过 70：进入危险区，重新开始该环节！")
            _hanzi_reset()


screen hanzi_trace():
    modal True
    tag hanzi_trace

    # 进入小游戏时禁用快进、隐藏快捷菜单，离开时恢复
    on "show" action Function(_hanzi_disable_skip)
    on "hide" action Function(_hanzi_enable_skip)

    # 每 0.1 秒强制关闭快进（防止进入前已开启或误触）
    timer 0.1 repeat True action Function(_hanzi_disable_skip)

    default start_t = time.time()
    default elapsed = 0.0

    # 命中的区域 index 集合
    default hit = set()
    # 鼠标轨迹点（用于画笔迹）
    default points = []

    # 本局超时累计加成（最多 +30）
    default overtime_added = 0

    # 每 0.1 秒更新用时显示
    timer 0.1 repeat True action SetScreenVariable("elapsed", time.time() - start_t)

    # 每 1 秒结算一次超时惩罚（符合 +5%/秒）
    timer 1.0 repeat True action Function(_hanzi_overtime_tick)

    # 采样鼠标位置（只在按下时记录）
    timer 0.05 repeat True action Function(_hanzi_sample_mouse)

    # 背景（拉伸到 1920x1080，保证坐标一致）
    add Transform("images/trace_hun_guide.jpg", xysize=(1920, 1080))

    # 测试用：半透明标出计分区域（show_hit_debug 为 True 时显示，可关闭）
    if show_hit_debug:
        for b in HANZI_BOXES:
            add Solid("#e8c85866", xpos=b[0], ypos=b[1], xsize=b[2]-b[0], ysize=b[3]-b[1])

    # 笔迹点轨迹
    for px, py in points:
        add Solid("#c9a227", xpos=px-4, ypos=py-4, xsize=8, ysize=8)

    # 顶部文字与进度 + 鼠标坐标（用于调框）
    vbox:
        xalign 0.02
        yalign 0.5
        spacing 8
        text "描红：写出【婚书】" size 32 color "#ffffff"
        $ total = len(HANZI_BOXES)
        $ score = int((len(hit) * 100) / total) if total else 0
        text "贴合度：%d%%  (目标 ≥ 80%%)" % score size 26 color "#ffffff"
        text "用时：%ds (>60s 开始超时惩罚)" % int(elapsed) size 22 color "#ffffff"
        $ mx, my = renpy.get_mouse_pos()
        text "mouse: (%d, %d)" % (mx, my) size 20 color "#dddddd"

    # 一键开挂（仅写字区内按下才描红，点此处不会写字）
    textbutton "一键开挂 (Auto-Write)":
        xalign 0.98
        yalign 0.06
        action [Function(_hanzi_cheat_do), Return("cheat")]

    # 底部按钮
    hbox:
        xalign 0.88
        yalign 0.95
        spacing 20
        textbutton "重写(清空)" action Function(_hanzi_reset)
        textbutton "提交" action Function(_hanzi_submit)

    # 不再用 key 拦截点击，改由 timer 轮询鼠标状态，按钮可正常响应