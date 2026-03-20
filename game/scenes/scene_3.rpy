define p1 = Character("贾斯文", color="#a52a2a")
define a = Character("未知", color="#808080")
define h = Character("洪彦龙", color="#0000ff")
define s = Character("兰中玉", color="#ff69b4")

label scene_3:
    scene bg hong_living
    with fade

    # 由暗转明 晕眩
    # 愤怒

    "头好晕..."
    "我感觉自己像是被什么东西狠狠地撞了一下，眼前一片模糊。"
    show h normal at left
    with dissolve
    a "把那兰中玉给我拉上来"

    "兰中玉...这个名字好熟悉..."
    a "兰中玉，你可还记得——"
    a "前些时日，本国舅在城中见你兄妹二人同行。"
    "等等...「本国舅」?"

    # 猛然抬起头来
    "这个装扮是..."
    "《逼婚记》里的洪彦龙？"
    "那我是？"
    # 看向自己
    "那个狗头军师贾斯文？"
    # 震动特效 出场音乐
    h "你那妹妹兰贵金，容貌清秀，举止娴静，倒是个难得的好模样。"
    h "本国舅一时欢喜，起了收她入府的念头，也算抬举你兰家门楣。"
    h "这等好事，你还有什么不愿意的？"

    show lan normal at right
    with dissolve
    s "国舅爷抬爱，草民惶恐。只是舍妹出身寒门，不通礼数，亦无福分，实不敢高攀国舅府门。此事，还请国舅爷另择良配。"

    # 冷笑

    h "另择？你是在教本国舅做事不成？"
    h "【走到兰中玉面前】"
    h "我洪彦龙堂堂当朝国舅，肯开口，已是你兰家祖宗积了八辈子德才换来的天大造化。"
    h "你兰中玉不过一个穷酸措大，世仆出身的讨饭坯子贱骨头，也敢在本国舅面前拿腔拿调？"

    s "国舅爷..."

    h "今天我就告诉你——"
    h "这国舅府的门，你兰家是攀也得攀，不攀也得攀！"

    s "强求之事，终非正道..."

    h "来人啊！把这不识抬举的狗奴才，给我拖下去！"
    show h angry at left

    s "草民不敢从命！"
    # 震动特效 拖走和拍桌子的声音

    h "呸！什么东西！给他三分颜色，他还真当自己这根穷骨头撑得起门楣了？！"

    h "【转向你】贾斯文！你也是个废物东西！"
    h "连个臭书生都搞不定，老子养你还不如养条狗！"

    menu:
        "国舅爷息怒！小的方才走神了，罪该万死！您有何吩咐，小的赴汤蹈火在所不辞！":
            h "老子让你想办法！"
            $ set_ooc(ooc - 10) # [修复] 顺从选项应降低 OOC
        "国舅爷！强抢民女乃是不义之举，您怎能如此蛮不讲理？":
            if ooc < 50:
                $ set_ooc(ooc + 25) # 增加惩罚值
                jump fail_to_answer
            else:
                $ set_ooc(100) # 强制拉满触发BE
                jump be

label scene_3_after_first_menu:

    "我得想办法保命，还得救兰贵金..."
    "有了！与其阻拦他，不如帮他做个伪证。若把伪证做得 “太完美” ，反而留下破绽！"
    
    p1 "国舅爷，强扭的瓜不甜。咱们得用计，伪造一份婚书，让他哑巴吃黄连！"
    h "哦？怎么个伪造法？"
    show h threat at left

    p1 "这婚书，不仅要写得真，还要有特定的字，方能显得它喜庆又正式！"

    $ _skipping = False
    call screen hanzi_trace
    $ _skipping = True
    if _return == "success":
        $ renpy.movie_cutscene("videos/contract_unfold.webm")
        show item_contract_evidence at center
        with dissolve
        p1 "这婚书……不仅要写得真，更要留下致命的破绽。"
    elif _return == "cheat":
        # 接：同成功反馈（外挂次数与 OOC 已在 hanzi_trace 中处理）
        pass

    p1 "国舅爷，咱们还得加上一句：秀才兰中玉立此为证！"

    h "妙！妙啊！贾师爷果然一肚子坏水！重重有赏！"

    scene cg_lan_mother
    with fade
    "夜色沉沉，兰母披发赤足奔至县衙门前，一声惊堂鼓震得街巷尽醒。"
    "几天后，听说兰中玉被绑架的兰母到县衙击鼓报了案。"
    "明天就是升堂的日子。"
    "在这之前我还有一些事情要做..."
    "去找知县张清。"
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