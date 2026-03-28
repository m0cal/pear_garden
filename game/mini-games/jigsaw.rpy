default jigsaw_correct_pieces = 0

init python:
    import random

    JIGSAW_BGM_PATH = "audio/pinlianpu.mp3"
    SUCCESS_SFX_PATH = "audio/success.mp3"
    FAILURE_SFX_PATH = "audio/failure.mp3"

    def _jigsaw_play_sfx_if_exists(path):
        if renpy.loadable(path):
            renpy.sound.play(path)

    def _jigsaw_music_enter():
        """进入拼图小游戏时切换 BGM，并记录进入前音乐。"""
        try:
            store._jigsaw_prev_bgm = renpy.music.get_playing(channel="music")
        except Exception:
            store._jigsaw_prev_bgm = None

        if renpy.loadable(JIGSAW_BGM_PATH):
            renpy.music.play(JIGSAW_BGM_PATH, channel="music", loop=True, fadein=0.5)

    def _jigsaw_music_exit():
        """离开拼图小游戏时恢复进入前 BGM（若无则停止 music）。"""
        prev = getattr(store, "_jigsaw_prev_bgm", None)
        if prev:
            renpy.music.play(prev, channel="music", loop=True, fadein=0.5)
        else:
            renpy.music.stop(channel="music", fadeout=0.5)
    
    def generate_jigsaw_data():
        pieces = []
        drop_zones = []
        grid_w = 3
        grid_h = 3
        
        # 分辨率 550x733
        piece_w = 550 // grid_w  # 183
        piece_h = 733 // grid_h  # 244
        
        # 拼图底板左上角起始坐标
        board_x = 100
        board_y = 150
        
        for y in range(grid_h):
            for x in range(grid_w):
                name = "piece_%d_%d" % (x, y)
                px = board_x + x * piece_w
                py = board_y + y * piece_h
                
                drop_zones.append({
                    "name": name,
                    "x": px,
                    "y": py,
                    "w": piece_w,
                    "h": piece_h
                })
                
                pieces.append({
                    "name": name,
                    "crop": (x * piece_w, y * piece_h, piece_w, piece_h),
                    # 在屏幕右侧随机生成初始位置（x坐标限制在 650-1050，y坐标限制在 50-450）
                    "start_x": random.randint(850, 1250), 
                    "start_y": random.randint(50, 450)
                })
        
        random.shuffle(pieces)
        return pieces, drop_zones

    def jigsaw_dragged(drags, drop):
        if not drop:
            return

        drag = drags[0]
        
        # 判断拖拽的对象名字和放置区域的名字是否匹配
        if drag.drag_name == drop.drag_name:
            # 匹配成功，吸附到目标位置
            drag.snap(drop.x, drop.y)
            drag.draggable = False # 放好后不再允许拖动
            
            store.jigsaw_correct_pieces += 1
            if store.jigsaw_correct_pieces == 9: # 3x3 共有 9 块
                _jigsaw_play_sfx_if_exists(SUCCESS_SFX_PATH)
                return True # 拼图完成，返回 True
        return

screen jigsaw():
    zorder 100
    modal True

    on "show" action Function(_jigsaw_music_enter)
    on "hide" action Function(_jigsaw_music_exit)
    
    # 初始化数据
    default setup_data = generate_jigsaw_data()
    default jigsaw_pieces = setup_data[0]
    default jigsaw_drop_zones = setup_data[1]
    
    # 每次打开界面时，重置拼好的碎片数量为0
    on "show" action SetVariable("jigsaw_correct_pieces", 0)
    
    # 深色半透明背景
    add Solid("#000000cc")
    
    # 拼图板的底框
    frame:
        xpos 100 ypos 150
        # 大小是格子的宽度乘以此数，排除除不尽的误差（183*3=549, 244*3=732）
        xsize (550 // 3 * 3) ysize (733 // 3 * 3)
        background Solid("#333333")
    
    draggroup:
        # 1. 放置所有的正确槽位（作为 drop target）
        for dz in jigsaw_drop_zones:
            drag:
                drag_name dz["name"]
                draggable False
                droppable True
                xpos dz["x"] ypos dz["y"]
                child Solid("#ffffff11", xsize=dz["w"], ysize=dz["h"]) # 微弱的高亮格子提示
                
        # 2. 放置打散的、可拖拽的拼图碎片
        for p in jigsaw_pieces:
            drag:
                drag_name p["name"]
                draggable True
                droppable False
                dragged jigsaw_dragged
                xpos p["start_x"] ypos p["start_y"]
                
                # 裁剪得到碎片
                child Transform("jigsaw.jpeg", crop=p["crop"])
                
    # 退出按钮
    textbutton "跳过":
        align (0.95, 0.95)
        action [Function(_jigsaw_play_sfx_if_exists, FAILURE_SFX_PATH), Return(False)]