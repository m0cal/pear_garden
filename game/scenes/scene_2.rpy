define p = Character("我", color="#a52a2a")

label scene_2:

    scene bg backstage
    # 远处戏台的锣鼓声，后台嘈杂声。
    # 视觉特效 晕头晃脑？

    "只要能救小莲，让我做什么都行..."
    "哪怕是把命卖给阎王。"

    # 整理戏箱图片
    show item_book at center
    with dissolve

    p "咝..." # 震动特效
    "【被木头箱子上锋利的木刺划破了手指】"
    hide item_book
    show item_book_blood at center
    with dissolve

    # 书1
    # 书2

    "【戏台上的灯火突然扭曲，化作金色的漩涡。那本无字书仿佛一只眼睛，缓缓睁开...】"
    hide item_book_blood
    $ renpy.movie_cutscene("videos/time_travel.webm")

return