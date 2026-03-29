default character_correct_pieces = 0
default jing_dropped_count = 0
default chou_dropped_count = 0
default character_pieces = []

init python:
    import random

    CHARACTER_BGM_PATH = "audio/pinlianpu.mp3"
    SUCCESS_SFX_PATH = "audio/success.mp3"
    FAILURE_SFX_PATH = "audio/failure.mp3"

    def _character_play_sfx_if_exists(path):
        if renpy.loadable(path):
            renpy.sound.play(path)

    def _character_music_enter():
        try:
            store._character_prev_bgm = renpy.music.get_playing(channel="music")
        except Exception:
            store._character_prev_bgm = None

        if renpy.loadable(CHARACTER_BGM_PATH):
            renpy.music.play(CHARACTER_BGM_PATH, channel="music", loop=True, fadein=0.5)

    def _character_music_exit():
        prev = getattr(store, "_character_prev_bgm", None)
        if prev:
            renpy.music.play(prev, channel="music", loop=True, fadein=0.5)
        else:
            renpy.music.stop(channel="music", fadeout=0.5)

    def generate_character_data():
        keywords = [
            {"id": "jing_1", "text": "身着黄袍"},
            {"id": "jing_2", "text": "繁复匝巾"},
            {"id": "jing_3", "text": "浓艳脸谱"},
            {"id": "jing_4", "text": "八字眉"},
            {"id": "chou_1", "text": "“豆腐块”脸谱"},
            {"id": "chou_2", "text": "八字胡"},
            {"id": "chou_3", "text": "带补丁的短褂"}
        ]
        
        pieces = []
        for i, kw in enumerate(keywords):
            # 将词条放置在画面中间偏下的位置，垂直排列稍微加入随机偏移
            pieces.append({
                "name": kw["id"],
                "text": kw["text"],
                "start_x": 860 + random.randint(-50, 50),
                "start_y": 400 + i * 80 + random.randint(-15, 15)
            })
            
        random.shuffle(pieces)
        return pieces

    def character_dragged(drags, drop):
        if not drop:
            # 放错区域弹回原位置
            drag = drags[0]
            for p in store.character_pieces:
                if p["name"] == drag.drag_name:
                    drag.snap(p["start_x"], p["start_y"], 0.2)
                    break
            return

        drag = drags[0]
        
        # 判断归属区域是否正确
        is_jing = drag.drag_name.startswith("jing_") and drop.drag_name == "jing_drop"
        is_chou = drag.drag_name.startswith("chou_") and drop.drag_name == "chou_drop"
        
        if is_jing or is_chou:
            # 放对区域，整齐排布
            if is_jing:
                idx = store.jing_dropped_count
                store.jing_dropped_count += 1
                target_x = drop.x + 50
                target_y = drop.y + 40 + idx * 60
            else:
                idx = store.chou_dropped_count
                store.chou_dropped_count += 1
                target_x = drop.x + 50
                target_y = drop.y + 40 + idx * 60
                
            drag.snap(target_x, target_y, 0.2)
            drag.draggable = False 
            
            store.character_correct_pieces += 1
            if store.character_correct_pieces == 7: 
                _character_play_sfx_if_exists(SUCCESS_SFX_PATH)
                return True 
        else:
            # 放错区域，播放失败音效并弹回
            _character_play_sfx_if_exists(FAILURE_SFX_PATH)
            for p in store.character_pieces:
                if p["name"] == drag.drag_name:
                    drag.snap(p["start_x"], p["start_y"], 0.2)
                    break
                    
        return

screen character_identification():
    zorder 100
    modal True

    on "show" action Function(_character_music_enter)
    on "hide" action Function(_character_music_exit)
    
    # 每次打开界面时，重置拼好的碎片数量和各对应区域收集的数量
    on "show" action [
        SetVariable("character_correct_pieces", 0),
        SetVariable("jing_dropped_count", 0),
        SetVariable("chou_dropped_count", 0)
    ]
    
    # 背景图片
    add "bg character.png"
    
    draggroup:
        # 左侧净角的判定区域
        drag:
            drag_name "jing_drop"
            draggable False
            droppable True
            # 根据背景进行调整（基准：1920x1080）
            xpos 280 
            ypos 100
            child Solid("#ffffff00", xsize=500, ysize=350)
            
        # 右侧丑角的判定区域
        drag:
            drag_name "chou_drop"
            draggable False
            droppable True
            xpos 1240 
            ypos 100
            child Solid("#ffffff00", xsize=500, ysize=350)
                
        # 所有打散的文字描述词条
        for p in character_pieces:
            drag:
                drag_name p["name"]
                draggable True
                droppable False
                dragged character_dragged
                xpos p["start_x"] ypos p["start_y"]
                
                # 文字框UI
                frame:
                    background Solid("#f4e8c1e6") 
                    padding (20, 10)
                    text p["text"] color "#442b10" size 30 outlines [(1, "#ffffff", 0, 0)]

    # 退出/跳过按钮
    textbutton "跳过":
        align (0.95, 0.95)
        action [Function(_character_play_sfx_if_exists, FAILURE_SFX_PATH), Return(False)]

label character:
    $ character_pieces = generate_character_data()
    call screen character_identification
    return

