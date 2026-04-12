define p1 = Character("贾斯文", color="#a52a2a")
define a = Character("未知", color="#808080")
define h = Character("洪彦龙", color="#0000ff")
define s = Character("兰中玉", color="#ff69b4")
define audio_bgm_study = "audio/bgm_study.mp3"
define audio_cold_laugh = "audio/cold_laugh.mp3"
define audio_drag = "audio/drag.mp3"
define audio_table = "audio/slap_table.mp3"
define audio_jiaobu = "audio/jiaobu.mp3"
define audio_hard_drum = "audio/hard_drum.wav"
define audio_wind = "audio/wind.mp3"
init:
    transform cam_shake:
        xoffset 0 yoffset 0
        linear 0.05 xoffset -12
        linear 0.05 xoffset 12
        linear 0.05 xoffset -10
        linear 0.05 xoffset 10
        linear 0.05 xoffset 0
        
    
label scene_3:
    stop music fadeout 0.1
    scene bg hong_living
    with fade

    # 由暗转明 晕眩
    # 愤怒
    voice "audio/voice/scene1/p_7.mp3"
    "头好晕..."
    "我感觉自己像是被什么东西狠狠地撞了一下，眼前一片模糊。"
    show h normal at left
    with dissolve
    voice "audio/voice/scene2/h_1.mp3"
    a "把那兰中玉给我拉上来"

    voice "audio/voice/scene2/sh_1.mp3"
    "兰中玉...这个名字好熟悉..."
    voice "audio/voice/scene2/h_2.mp3"
    a "兰中玉，你可还记得——前些时日，本国舅在城中见你兄妹二人同行。"
    voice "audio/voice/scene2/sh_2.mp3"
    "等等...「本国舅」?这个装扮是...《逼婚记》里的洪彦龙？那我是？那个狗头军师贾斯文？"

    call character from _call_character
    # 震动特效 出场音乐
    play music audio_bgm_study fadein 1.0 loop
    show layer master at cam_shake
    voice "audio/voice/scene2/h_3.mp3"
    h "你那妹妹兰贵金，容貌清秀，举止娴静，倒是个难得的好模样。本国舅一时欢喜，起了收她入府的念头，也算抬举你兰家门楣。这等好事，你还有什么不愿意的？"

    show lan normal at right
    with dissolve
    voice "audio/voice/scene2/s_1.mp3"
    s "国舅爷抬爱，草民惶恐。只是舍妹出身寒门，不通礼数，亦无福分，实不敢高攀国舅府门。此事，还请国舅爷另择良配。"

    # 冷笑
    play sound audio_cold_laugh
    voice "audio/voice/scene2/h_4.mp3"
    h "另择？你是在教本国舅做事不成？"
    h "【走到兰中玉面前】"
    play sound audio_jiaobu
    voice "audio/voice/scene2/h_5.mp3"
    h "我洪彦龙堂堂当朝国舅，肯开口，已是你兰家祖宗积了八辈子德才换来的天大造化。你兰中玉不过一个穷酸措大，世仆出身的讨饭坯子贱骨头，也敢在本国舅面前拿腔拿调？"

    voice "audio/voice/scene2/s_2.mp3"
    s "国舅爷..."

    voice "audio/voice/scene2/h_6.mp3"
    h "今天我就告诉你——这国舅府的门，你兰家是攀也得攀，不攀也得攀！"

    voice "audio/voice/scene2/s_3.mp3"
    s "强求之事，终非正道..."

    voice "audio/voice/scene2/h_7.mp3"
    h "来人啊！把这不识抬举的狗奴才，给我拖下去！"
    voice "audio/voice/scene2/j_1.mp3"
    "家丁" "是！"
    show h angry at left

    voice "audio/voice/scene2/s_4.mp3"
    s "草民不敢从命！"
    # 震动特效 拖走和拍桌子的声音
    show layer master at cam_shake
    play sound audio_drag
    play sound audio_table
    voice "audio/voice/scene2/h_8.mp3"
    h "呸！什么东西！给他三分颜色，他还真当自己这根穷骨头撑得起门楣了？！贾斯文！你也是个废物东西！连个臭书生都搞不定，老子养你还不如养条狗！"

    menu:
        "国舅爷息怒！小的方才走神了，罪该万死！您有何吩咐，小的赴汤蹈火在所不辞！":
            voice "audio/voice/scene2/sh_3.mp3"
            p1 "国舅爷息怒！小的方才走神了，罪该万死！您有何吩咐，小的赴汤蹈火在所不辞！"
            voice "audio/voice/scene2/h_9.mp3"
            h "老子让你想办法！"
            $ set_ooc(ooc - 10) # [修复] 顺从选项应降低 OOC
        "国舅爷！强抢民女乃是不义之举，您怎能如此蛮不讲理？":
            voice "audio/voice/scene2/sh_4.mp3"
            p1 "国舅爷！强抢民女乃是不义之举，您怎能如此蛮不讲理？"
            if ooc < 50:
                $ set_ooc(ooc + 25) # 增加惩罚值
                jump fail_to_answer
            else:
                $ set_ooc(100) # 强制拉满触发BE
                jump be

label scene_3_after_first_menu:

    voice "audio/voice/scene2/sh_4.mp3"
    "我得想办法保命，还得救兰贵金..."
    voice "audio/voice/scene2/sh_4.mp3"
    "有了！与其阻拦他，不如帮他做个伪证。若把伪证做得 “太完美” ，反而留下破绽！"
    
    voice "audio/voice/scene2/sh_5.mp3"
    p1 "国舅爷，强扭的瓜不甜。咱们得用计，伪造一份婚书，让他哑巴吃黄连！"
    voice "audio/voice/scene2/h_10.mp3"
    h "哦？怎么个伪造法？"
    show h threat at left
    
    voice "audio/voice/scene2/sh_6.mp3"
    p1 "这婚书，不仅要写得真，还要有特定的字，方能显得它喜庆又正式！国舅爷，咱们还得加上一句：秀才兰中玉立此为证！"

    call screen hanzi_trace
    if _return == "success":
        $ renpy.movie_cutscene("videos/write_contract.webm") # 替换为新生成的书写视频
        show item_contract_evidence at center
        with dissolve
        $ renpy.notify("OOC 值大幅降低（-20）")
        $ renpy.pause(0.3, hard=True)
    elif _return == "cheat":
        $ renpy.notify("外挂生效：自动完成（OOC -50）")
        $ renpy.pause(0.3, hard=True)
    # if _return == "success":
    #     $ renpy.movie_cutscene("videos/contract_unfold.webm")
    #     show item_contract_evidence at center
    #     with dissolve
    
    if _return == "success" or _return == "cheat":
        p1 "这婚书……不仅要写得真，更要留下致命的破绽。"

    voice "audio/voice/scene2/h_11.mp3"
    h "妙！妙啊！贾师爷果然一肚子坏水！重重有赏！"

    scene bg_lan_mother
    with fade
    play music audio_wind fadein 1.0 loop
    "夜色沉沉，兰母披发赤足奔至县衙门前，一声惊堂鼓震得街巷尽醒。"
    play sound audio_hard_drum
    voice "audio/voice/scene3/n_1.mp3"
    "几天后，听说兰中玉被绑架的兰母到县衙击鼓报了案。"
    voice "audio/voice/scene3/sh_7.mp3"
    "明天就是升堂的日子。在这之前我还有一些事情要做...去找知县张清。知县张清据说为人刚正不阿。如果我能在审判前主动揭发洪彦龙的罪行，或许兰家兄妹就能逃脱这个恶魔的魔爪。"
    
    scene bg_lan_mother
    with fade

    
    scene bg_lan_mother
    with fade
    return

# [修复] 补全缺失的标签和二次选择逻辑（对应策划文档）
label fail_to_answer:
    h "（拔刀相向）你今日鬼话连篇，敢教训本国舅？受死吧！"
    menu:
        "（继续争辩）我所言句句属实，你这样迟早自食恶果！":
            $ set_ooc(100) # OOC拉满，直接死
            jump be
        "（紧急求饶）国舅爷饶命！小的一时糊涂胡言乱语，您大人有大量，饶了小的这一次！":
            $ set_ooc(ooc - 10) # 挽回部分OOC
            h "哼！下次再敢胡言，定不饶你！"
            # 剧情接回正轨
            jump scene_3_after_first_menu