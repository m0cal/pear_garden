define l = Character('小莲', color="#c8a2c8")
define p = Character('我', color="#a52a2a")

image lotus_handkerchief = "images/lotus_handkerchief.png"
image bg hong_living = "images/bg_hong_livingroom.jpg"
image bg county_night = "images/bg_county_office_night.jpg"
image bg county_study = "images/bg_county_study.jpg"
image h normal = "images/hong_normal.png"
image h angry = "images/hong_angry.png"
image h scared = "images/hong_scared.png"
image h threat = "images/hong_threat.png"
image y suspicious = "images/yayi_suspicious.png"
image y normal = "images/yayi_normal.png"
image lan normal = "images/lan_normal.png"
image magistrate normal = "images/magistrate_normal.png"
image bg county_court = "images/bg_county_study.jpg"
image item_book = "images/item_book.png"
image item_book_blood = "images/item_book_blood.png"
image item_handkerchief_blood = "images/item_handkerchief_blood.png"
image item_bun = "images/item_bun.png"
image item_contract_evidence = "images/item_contract_evidence.png"
image vid_contract_unfold = Movie(play="videos/contract_unfold.webm")
define audio_door_open = "audio/door_open.mp3"
define audio_cough = "audio/cough.mp3"
init:
  transform cam_shake:
      xoffset 0 yoffset 0
      linear 0.15 xoffset -16
      linear 0.15 xoffset 16
      linear 0.15 xoffset -14
      linear 0.15 xoffset 14
      linear 0.15 xoffset 0

label scene_1:
    scene bg lovelyhome
    "我揣着怀里尚带余温的半个窝头，推开那扇吱呀作响的破木门时，天色已近黄昏。"
    play sound audio_door_open
    
    # BGM
    "屋内昏暗，只有一缕残阳从窗纸的破洞漏进来，恰好照在墙角那张铺着干草的“床”上。小莲蜷缩在那里，身上盖着件打满补丁的旧戏服——那是师父看我可怜赏的，如今成了她唯一的御寒之物。"

    l "哥..."

    "她听见动静，挣扎着想坐起来，却引发了一阵撕心裂肺的咳嗽。"
    play sound audio_cough
    show layer master at cam_shake
    pause 1.8
    show layer master at cam_shake
    pause 1.8
    show layer master at cam_shake

    # 震动效果，音效

    l "哥...你回来了？"

    "我心头一紧，几步抢上前去，轻轻拍着她的背。"
    "入手处，隔着薄薄的衣衫，能清晰地摸到她嶙峋的脊骨，像是一把枯柴。"

    p "别动，躺着。"

    "我努力让自己的声音听起来轻松些，从怀里掏出那半个窝头。"

    p "看，今天班主赏的白面窝头，还热乎着呢。"
    show item_bun at center
    with dissolve

    l "哥...你吃...我...我不饿..."

    "傻丫头，连撒谎都不会。"

    p "我早吃过了，后台点心多着呢。快吃，吃了才有力气。等哥成了角儿，天天给你买肉包子。"
    hide item_bun

    show lotus normal at right
    with dissolve
    
    show lotus_handkerchief at center
    with dissolve
    
    l "哥，这是我新绣的手帕，你看这莲花……"
    
    play sound audio_cough
    show layer master at cam_shake
    pause 1.8
    show layer master at cam_shake
    pause 1.8
    show layer master at cam_shake

    l "【剧烈咳嗽】"
    "她急忙用手帕捂住嘴，摊开时，帕角已晕开一抹刺目的红。"
    hide lotus_handkerchief
    show item_handkerchief_blood at center
    with dissolve

    p "小莲！"
    hide item_handkerchief_blood

    # 切换立绘
    l "没事的，哥 …… 我今天好多了。"

    "药罐早就空了。再不断药，她熬不过这个冬天..."

return