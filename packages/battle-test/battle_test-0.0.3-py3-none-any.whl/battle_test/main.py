# -*- encoding=utf8 -*-
__author__ = "Bingo"

from airtest.core.api import *

w,h = device().get_current_resolution() # 获取手机分辨率
ratio = w/1920

position = {
    'skill_1': [100*ratio, 860*ratio], # 一技能坐标
    'skill_2': [245*ratio, 860*ratio], # 二技能坐标
    'skill_3': [385*ratio, 860*ratio], # 三技能坐标
    'skill_4': [575*ratio, 860*ratio], # 四技能坐标
    'skill_5': [720*ratio, 860*ratio], # 五技能坐标
    'skill_6': [860*ratio, 860*ratio], # 六技能坐标
    'skill_7': [1060*ratio, 860*ratio], # 七技能坐标
    'skill_8': [1195*ratio, 860*ratio], # 八技能坐标
    'skill_9': [1335*ratio, 860*ratio], #  九技能坐标
    'cloth_1': [1350*ratio, 460*ratio], #  衣服1技能坐标
    'cloth_2': [1490*ratio, 460*ratio], #  衣服2技能坐标
    'cloth_3': [1620*ratio, 460*ratio], #  衣服3技能坐标
    'servant_1': [480*ratio, 710*ratio], # 从者1坐标
    'servant_2': [1000*ratio, 710*ratio], # 从者2坐标
    'servant_3': [1400*ratio, 710*ratio], # 从者3坐标
    'change_1': [200*ratio, 500*ratio], # 换人前排1号位坐标
    'change_2': [500*ratio, 500*ratio], # 换人前排2号位坐标
    'change_3': [800*ratio, 500*ratio], # 换人前排3号位坐标
    'change_4': [1100*ratio, 500*ratio], # 换人后排4号位坐标
    'change_5': [1400*ratio, 500*ratio], # 换人后排5号位坐标
    'change_6': [1700*ratio, 500*ratio], # 换人后排6号位坐标
}

# skillName
# targetIndex: 0为不选择, 1 2 3分别选择第1 2 3名从者
# changeTarget使用换人衣服的目标,为后排的index(4、5、6),为None或0时不换人
def useSkill(skillType, skillIndex, targetIndex, changeTarget = None):
    # 如果使用的是从者技能
    if (skillType == 'servant'):
        touch(position['skill_'+ str(skillIndex)])
        sleep(3)
    # 如果使用的是衣服技能
    if (skillType == 'cloth'):
        # 点击衣服
        touch([1790*ratio, 470*ratio])
        sleep(2)
        # 点击该衣服技能
        touch(position['cloth_'+ str(skillIndex)])
        sleep(3)
    # 如果换人
    if (changeTarget):
        # 点击前排
        touch(position['change_'+ str(targetIndex)])
        sleep(2)
        # 点击后排
        touch(position['change_'+ str(changeTarget)])
        sleep(2)
        # 换人
        touch([960*ratio, 930*ratio])
        sleep(4.5)
    else:
        # 如果技能需要给某个从者, 之后点击该从者
        if (targetIndex):
            touch(position['servant_' + str(targetIndex)])
            sleep(3)
    return

def judgePosition(x, selected):
    if (x < 380*ratio):
        if(selected[0] == 0):
            selected[0] = 1
        else:
            selected[1] = 1
    elif (x < 780*ratio):
        if(selected[0] == 0):
            selected[0] = 2
        else:
            selected[1] = 2
    elif (x < 1160*ratio):
        if(selected[0] == 0):
            selected[0] = 3
        else:
            selected[1] = 3
    elif (x < 1560*ratio):
        if(selected[0] == 0):
            selected[0] = 4
        else:
            selected[1] = 4
    else:
        if(selected[0] == 0):
            selected[0] = 5
        else:
            selected[1] = 5
    return selected

def useCard(selected):
    cardPositions = {
        1: [200*ratio, 750*ratio],
        2: [580*ratio, 750*ratio],
        3: [970*ratio, 750*ratio],
        4: [1350*ratio, 750*ratio],
        5: [1740*ratio, 750*ratio],
    }
    all = [1, 2, 3, 4, 5]
    if (selected[0] in all):
        all.remove(selected[0])
    if (selected[1] in all):
        all.remove(selected[1])
    # 排除已选的卡后出卡
    if (len(all) == 5):
        touch(cardPositions[all[0]])
        sleep(1)
        touch(cardPositions[all[1]])
        sleep(1)
    if (len(all) == 4):
        touch(cardPositions[all[0]])
        sleep(1)
    return

def touchCard(card, selected, count):
    if(card):
        selected = judgePosition(card[0], selected)
        count = count + 1
        touch(card)
        card = False
        sleep(1.5)
    return card, selected, count

def attack(useMain = False):
    count = 0
    sleep(3)
    # 攻击
    touch([1700*ratio, 900*ratio])
    sleep(2)
    # 长江宝具
    touch([970*ratio, 300*ratio])
    sleep(2)
    selected = [0, 0]
    # useMain为True表示伤害不够需要选择打手的卡
    if (useMain):
        card = False
        if (count < 2):
            card = exists(Template(r"tpl1601885638547.png", threshold=0.9, record_pos=(0.201, 0.133), resolution=(1920, 1080)))
            card, selected, count = touchCard(card, selected, count)
        if (count < 2):
            card = exists(Template(r"tpl1601885735963.png", threshold=0.9, record_pos=(0.405, 0.132), resolution=(1920, 1080)))
            card, selected, count = touchCard(card, selected, count)
        if (count < 2):
            card = exists(Template(r"tpl1601885735963.png", threshold=0.9, record_pos=(0.405, 0.132), resolution=(1920, 1080)))
            card, selected, count = touchCard(card, selected, count)
        if (count < 2):
            card = exists(Template(r"tpl1601885735963.png", threshold=0.9, record_pos=(0.405, 0.132), resolution=(1920, 1080)))
            card, selected, count = touchCard(card, selected, count)
        if (count < 2):
            card = exists(Template(r"tpl1601885797216.png", threshold=0.9, record_pos=(-0.199, 0.139), resolution=(1920, 1080)))
            card, selected, count = touchCard(card, selected, count)
    # 选择并出卡
    useCard(selected)
    return