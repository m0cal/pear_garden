define p = Character("我", color="#a52a2a")
define audio_background_noise = "audio/background_noise.mp3"
define audio_drum_3 = "audio/drum3.mp3"
define audio_drum_4 = "audio/drum4.mp3"


# 晕头晃脑的特效
init:
  transform dizzy:
      xalign 0.5
      yalign 0.5
      zoom 1.0
      easeout 0.70 zoom 1.30
      easein 0.80 zoom 1.0
      easeout 0.70 zoom 1.30
      easein 0.80 zoom 1.0
      repeat
# 震动特效
init:
    transform cam_shake:
        xoffset 0 yoffset 0
        linear 0.05 xoffset -12
        linear 0.05 xoffset 12
        linear 0.05 xoffset -10
        linear 0.05 xoffset 10
        linear 0.05 xoffset 0

label scene_2:
    scene bg backstage
    play music audio_background_noise loop
    
    # 远处戏台的锣鼓声，后台嘈杂声。
    # 视觉特效 晕头晃脑？
    show layer master at dizzy

    "只要能救小莲，让我做什么都行..."
    play sound audio_drum_4
    "哪怕是把命卖给阎王。"
    show layer master

    # 整理戏箱图片
    show item_book at center
    with dissolve

    p "咝..." # 震动特效
    play sound audio_drum_3
    show layer master at cam_shake

    "【被木头箱子上锋利的木刺划破了手指】"
    hide item_book
    show item_book_blood at center
    with dissolve

    # 书1
    # 书2
    play sound audio_drum_4
    "【戏台上的灯火突然扭曲，化作金色的漩涡。那本无字书仿佛一只眼睛，缓缓睁开...】"
    hide item_book_blood

return