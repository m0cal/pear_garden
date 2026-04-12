define y = Character("衙役")
define p1 = Character("贾斯文", color="#a52a2a")
define z = Character("张清")

label scene_4:
    scene bg county_night
    with fade
    play music audio_wind fadein 1.0 loop
    "我整理了一下斗篷，从阴影中走出。"

    voice "audio/voice/scene3/ya_1.mp3"
    y "站住！什么人？"
    voice "audio/voice/scene3/sh_8.mp3"
    p1 "差爷恕罪！小人是洪彦龙洪国舅府上的师爷贾斯文，有十万火急的密信，必须亲手呈交知县大人"
    voice "audio/voice/scene3/ya_2.mp3"
    y "洪彦龙的师爷？这么晚了，有何要事？"
    show y suspicious at left
    "明显能看出，衙役的态度明显更谨慎了"

    menu:
        "直接掏出银子":
            voice "audio/voice/scene3/sh_9.mp3"
            p1 "请差爷行个方便，此事关乎大人清誉，耽搁不得啊！"
            voice "audio/voice/scene3/n_2.mp3"
            "衙役皱了皱眉毛，虽然看起来还是不太信任贾斯文的样子，但最终还是点了点头"
            show y normal at left
            voice "audio/voice/scene3/ya_3.mp3"
            y "你等着，我去通报。"
        "尝试用洪彦龙的身份压他":
            voice "audio/voice/scene3/sh_10.mp3"
            p1 "此信是国舅亲笔所写要给知县大人，鄙人已经说了十万火急，若是因为你们耽搁了，且看知县大人如何处置你们！"
            "衙役显然是咬紧了后槽牙，憋了半天才吐出两个字："
            voice "audio/voice/scene3/ya_4.mp3"
            y "等着。（远处小声）狗仗人势的东西..."
    
    voice "audio/voice/scene3/n_3.mp3"
    "不知道过了多久，衙役回来了"
    voice "audio/voice/scene3/ya_5.mp3"
    y "进去吧，知县大人在书房等你。"

    scene bg county_study
    with dissolve
    voice "audio/voice/scene3/n_4.mp3"
    "贾斯文走进张清的书房，他正在书案后坐着，手里捧着一卷书。"
    show magistrate stand at left
    with dissolve

    voice "audio/voice/scene3/z_1.mp3" 
    z "你是洪彦龙的师爷？"
    "我扑通一声跪倒在案前。"
    voice "audio/voice/scene3/sh_11.mp3"
    p1 "是，小人贾斯文，参见知县大人！关于洪家和兰家的案子...小人有要事相禀!"
    voice "audio/voice/scene3/z_2.mp3"
    z "讲。"
    voice "audio/voice/scene3/sh_12.mp3"
    p1 "大人明鉴！洪彦龙强抢民女，伪造婚书，意图构陷兰中玉！"
    "张清的脸色变了变，眯起了眼睛。"
    voice "audio/voice/scene3/z_3.mp3" 
    z "洪彦龙？你不是他师爷吗？这是什么意思？"
    voice "audio/voice/scene3/sh_13.mp3"
    p1 "小人……小人虽是寒门，却也读过圣贤书，知道‘忠义’二字！他做的这些事情伤天害理、丧尽天良！明日公堂之上，他就要用一份假婚书来混淆是非！小人……小人不忍见无辜之人蒙冤，更不忍见大人被奸人蒙蔽，特来告发！"
    $ add_ooc(-20)


    voice "audio/voice/scene3/n_5.mp3"
    "张清沉默了片刻，手指轻轻敲击着桌面。"
    "..."
    "..."
    "..."
    "..."
    "...不知道过了多久，张清终于开口了。"

    voice "audio/voice/scene3/z_4.mp3"
    z "给我说说吧，你有何证据？"

    voice "audio/voice/scene3/sh_14.mp3"
    p1 "知县大人...此婚书非兰中玉所写，且看....."

return