screen ooc_overlay():
    # 这个屏幕会一直显示在最上层，显示当前的 OOC
    zorder 100

    frame:
        xalign 0.05
        yalign 0.05
        background "#0008"
        padding (10, 5)
        text "OOC: [ooc]" color "#fff" size 20