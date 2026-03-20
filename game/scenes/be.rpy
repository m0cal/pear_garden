label fail_to_answer_legacy:
    # 用于没有正确回答洪彦龙的提问
    h "你说什么？！"
    h "你是想要和我作对吗？"
    h "贾斯文，不要忘了自己是谁...再敢说这样的话...我就让你死得连骨头都不剩！"
    "回到本幕开头。"
    jump scene_3

label be:
    # 戏碎人亡
    "你的行为脱离了角色设定，已经无法继续进行下去。"
    $ renpy.full_restart()
