label start:
    stop music

    show screen ooc_overlay
    call intro from _call_intro

    call scene_1 from _call_scene_1

    call scene_2 from _call_scene_2

    # call 脸谱游戏
    call screen jigsaw

    call scene_3 from _call_scene_3

    # 播放夜间潜伏第一人称转场视频
    $ renpy.movie_cutscene("videos/night_stealth.webm")

    # call 躲避家丁游戏
    call screen maze_game
    call scene_4 from _call_scene_4

    call scene_5 from _call_scene_5

    # 正常通关时关闭 OOC 浮层，避免 UI 残留。
    hide screen ooc_overlay
    
    return
