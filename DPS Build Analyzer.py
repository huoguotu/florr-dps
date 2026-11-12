from math import *
import io
import sys
import json

global petalhealth, reload, summoner, luck, poison, dup, rot, tp, T, ed, ea, dis, udl, dl, qdl, ph_bonus, ugl, gl, qgl, utri, tri
lenti = [0, 0, 0.03, 0.064, 0.084, 0.104]
ph_buff = {"-": 1, "C": 1.15, "Un": 1.15**2, "R": 1.15**3, "E": 1.15**4, "L": 1.15**5, "M": 1.15**6, "U": 1.15**7, "S": 1.15**8, "Et": 1.15**10}
ph_tp = {"-": 0, "C": 2, "Un": 6, "R": 12, "E": 20, "L": 30, "M": 42, "U": 56, "S": 72, "Et": 90}
reload_buff = {"-": 1, "C": 0.9, "Un": 0.9**2, "R": 0.9**3, "E": 0.9**4, "L": 0.9**4*0.8, "M": 0.9**4*0.8**2, "U": 0.9**4*0.8**3, "S": 0.9**4*0.8**4, "Et": 0.9**4*0.8**4*0.7}
reload_tp = {"-": 0, "C": 2, "Un": 8, "R": 18, "E": 30, "L": 46, "M": 66, "U": 90, "S": 118, "Et": 150}
summoner_buff = {"-": 1, "C": 1.15, "Un": 1.15**2, "R": 1.15**3, "E": 1.15**4, "L": 1.15**5, "M": 1.15**6, "U": 1.15**7, "S": 1.15**8, "Et": 1.15**10}
summoner_tp = {"-": 0, "C": 2, "Un": 7, "R": 15, "E": 26, "L": 40, "M": 57, "U": 77, "S": 100, "Et": 126}
luck_buff = {"-": 0, "C": 0.1, "Un": 0.25, "R": 0.45, "E": 0.7, "L": 1, "M": 1.35, "U": 1.75, "S": 2.2, "Et": 2.7}
luck_tp = {"-": 0, "C": 2, "Un": 5, "R": 9, "E": 14, "L": 20, "M": 27, "U": 35, "S": 44, "Et": 54}
poison_buff = {"-": 1, "1": 1.0625, "2": 1.125, "3": 1.1875, "4": 1.25, "5": 1.3125, "6": 1.375, "7": 1.4375, "8": 1.5, "9": 1.5625}
poison_tp = {"-": 0, "1": 1, "2": 3, "3": 6, "4": 9, "5": 12, "6": 15, "7": 18, "8": 21, "9": 24}
cpoison_buff = {"-": 1, "1": 1.2}
cpoison_tp = {"-": 0, "1": 15}
dup_buff = {"-": 0, "L": 1, "U": 2, "S": 3, "Et": 3}
dup_tp = {"-": 0, "L": 10, "U": 30, "S": 60, "Et": 100}
rot_buff = {"-": 0, "C": 0.6, "Un": 1.2, "R": 1.8, "E": 2.4, "L": 3}
rot_tp = {"-": 0, "C": 1, "Un": 3, "R": 6, "E": 10, "L": 15}
reach_tp = {"-": 0, "R": 3, "M": 9, "S": 18}
health_tp = {"-": 0, "C": 2, "Un": 7, "R": 15, "L": 25, "M": 45}


def rnd(x):
    return max(x, 0.05)


def lvl(x):
    for lv in range(1, 999):
        t = lv//10*20
        if lv % 10 <= 4:
            t += lv % 10-1
        else:
            t += lv % 10
        if t >= x:
            return lv


def d(pd, ph=1, typ=""):
    res = 0
    m = ph
    if typ == "ubattery" or typ == "ulightning":
        return pd*8
    if typ == "battery" or typ == "lightning":
        return pd*9
    if typ == "qbattery" or typ == "qlightning":
        return pd*10
    if typ == "ubone":
        pa = 7290
        while m > 0:
            res += max(0, pd*m/ph-ea)
            m -= max(0, ed-pa)
            pa /= 2
        return res
    if typ == "bone":
        pa = 21870
        while m > 0:
            res += max(0, pd*m/ph-ea)
            m -= max(0, ed-pa)
            pa /= 2
        return res
    if typ == "qbone":
        pa = 65610
        while m > 0:
            res += max(0, pd*m/ph-ea)
            m -= max(0, ed-pa)
            pa /= 2
        return res
    if typ == "uclaw":
        while m > 0:
            res += max(0, pd*m/ph-ea+72900)
            m -= ed
        return res
    if typ == "claw":
        while m > 0:
            res += max(0, pd*m/ph-ea+218700)
            m -= ed
        return res
    if typ == "qclaw":
        while m > 0:
            res += max(0, pd*m/ph-ea+656100)
            m -= ed
        return res
    if typ == "ubgg" or typ == "bgg" or typ == "qbgg" or typ == "uagg" or typ == "agg" or typ == "qagg" or typ == "ustick" or typ == "stick" or typ == "qstick":
        return max(0, pd-ea)*ceil(ph/ed)
    if typ == "qmjolnir":
        while m > 0:
            res += max(0, pd*m/ph)
            m -= ed
        return res
    while m > 0:
        res += max(0, pd*m/ph-ea)
        m -= ed
    return res


def h(ph):
    return ph*(petalhealth+0.3*udl+0.45*dl+0.6*qdl)


def mh(ph):
    return ph*summoner


def fx(x):
    if x <= 13:
        return 0
    return 0.0003664*(x-13.06)


def r(rel, ph=1):
    res = rnd(rel*reload*(0.825**ugl)*(0.8**gl)*(0.775**qgl)*(1.05**(udl+dl+qdl)))
    res += ceil(ph/ed)//10*(1/25)
    res += fx(dis)
    return res


def mr(rel, ph=1):
    res = rnd(rel*reload*(0.825**ugl)*(0.8**gl)*(0.775**qgl)*(1.05**(udl+dl+qdl)))
    res += ceil(ph/ed)*(1/25)
    res += fx(dis)
    return res


def hr(rel, ph=1):
    res = rnd(rel*reload*(0.825**ugl)*(0.8**gl)*(0.775**qgl)*(1.05**(udl+dl+qdl)))
    res += ceil(ph/ed)*(1/25)
    res += fx(dis)
    return res


def cal(petal):
    def f(name):
        return petal == name

    # basic/clover/salt/soil/talisman/yinyang
    if f("ubasic") or f("uclover") or f("usalt") or f("usoil") or f("utalisman") or f("uyinyang"):
        return d(7290, h(7290))/r(2.5, h(7290))
    if f("basic") or f("clover") or f("salt") or f("soil") or f("talisman") or f("yinyang"):
        return d(21870, h(21870))/r(2.5, h(21870))
    if f("qbasic") or f("qclover") or f("qsalt") or f("qsoil") or f("qtalisman") or f("qyinyang") or f("tbasic"):
        return d(65610, h(65610))/r(2.5, h(65610))
    # battery
    if f("ubattery"):
        return d(26244, h(1), "ubattery")/(r(2.5)+0.1)
    if f("battery"):
        return d(78732, h(1), "battery")/(r(2.5)+0.1)
    if f("qbattery"):
        return d(236196, h(1), "qbattery")/(r(2.5)+0.1)
    # bean
    if f("ubean") or f("ubean_0"):
        return d(14580, h(8748))/r(2, h(8748))
    if f("ubean_1"):
        return d(21870, h(8748))/r(2, h(8748))
    if f("bean") or f("bean_0"):
        return d(43740, h(26244))/r(2, h(26244))
    if f("bean_1"):
        return d(65610, h(26244))/r(2, h(26244))
    if f("qbean") or f("qbean_0"):
        return d(131220, h(78732))/r(2, h(78732))
    if f("qbean_1"):
        return d(196830, h(78732))/r(2, h(78732))
    # blueberries
    # bone
    if f("ubone"):
        return d(10206, h(7290), "ubone")/r(2.5, h(7290)+14580)
    if f("bone"):
        return d(30618, h(21870), "bone")/r(2.5, h(21870)+43740)
    if f("qbone"):
        return d(91854, h(65610), "qbone")/r(2.5, h(65610)+131220)
    # broccoli
    if f("ubroccoli") or f("ubroccoli_0"):
        return d(10935, h(7290))/r(2.8, h(7290))
    if f("ubroccoli_1") or f("ubroccoli_2") or f("ubroccoli_3"):
        return (d(10935, h(7290))+int(petal[10:])*d(3645, h(2430)))/r(2.8, h(7290))
    if f("broccoli") or f("broccoli_0"):
        return d(32805, h(21870))/r(2.8, h(21870))
    if f("broccoli_1") or f("broccoli_2") or f("broccoli_3"):
        return (d(32805, h(21870))+int(petal[9:])*d(10935, h(7290)))/r(2.8, h(21870))
    if f("qbroccoli") or f("qbroccoli_0"):
        return d(98415, h(65610))/r(2.8, h(65610))
    if f("qbroccoli_1") or f("qbroccoli_2") or f("qbroccoli_3"):
        return (d(98415, h(65610))+int(petal[10:])*d(32805, h(21870)))/r(2.8, h(65610))
    # bur
    if f("ubur"):
        return d(3645, h(3645))/r(2, h(3645))
    if f("bur"):
        return d(10935, h(10935))/r(2, h(10935))
    if f("qbur"):
        return d(32805, h(32805))/r(2, h(32805))
    # cactus/cactus(magic)
    if f("ucactus") or f("ucactus_magic"):
        return d(5103, h(10935))/r(1, h(10935))
    if f("cactus") or f("cactus_magic"):
        return d(15309, h(32805))/r(1, h(32805))
    if f("qcactus") or f("qcactus_magic"):
        return d(45927, h(98415))/r(1, h(98415))
    # card
    if f("ucard"):
        return (d(3645, h(21870))/r(2.5, h(21870))+d(7290, h(18225))/r(2.5, h(18225))+d(10935, h(14580))/r(2.5, h(14580))+d(14580, h(10935))/r(2.5, h(10935)))/4
    if f("card"):
        return (d(10935, h(65610))/r(2.5, h(65610))+d(21870, h(54675))/r(2.5, h(54675))+d(32805, h(43740))/r(2.5, h(43740))+d(43740, h(32805))/r(2.5, h(32805)))/4
    if f("qcard"):
        return (d(32805, h(196830))/r(2.5, h(196830))+d(65610, h(164025))/r(2.5, h(164025))+d(98415, h(131220))/r(2.5, h(131220))+d(131220, h(98415))/r(2.5, h(98415)))/4
    # carrot
    if f("ucarrot_0"):
        return d(13122/5, h(13122))/r(1, h(13122))
    if f("carrot_0"):
        return d(39366/5, h(39366))/r(1, h(39366))
    if f("qcarrot_0"):
        return d(118098/5, h(118098))/r(1, h(118098))
    if f("ucarrot") or f("ucarrot_1"):
        return d(13122, h(13122))/(r(1, h(13122))+0.5)
    if f("carrot") or f("carrot_1"):
        return d(39366, h(39366))/(r(1, h(39366))+0.5)
    if f("qcarrot") or f("carrot_1"):
        return d(118098, h(118098))/(r(1, h(118098))+0.5)
    # chip
    if f("uchip"):
        return d(5103, h(2187))*10/(r(2.5, h(729))+0.9**10/(1-0.9**10)*0.04)
    if f("chip"):
        return d(15309, h(2187))*10/(r(2.5, h(2187))+0.9**10/(1-0.9**10)*0.04)
    if f("qchip"):
        return d(45927, h(2187))*10/(r(2.5, h(6561))+0.9**10/(1-0.9**10)*0.04)
    # claw
    if f("uclaw_0"):
        return d(3645, h(7290))/r(3.5, h(7290))
    if f("uclaw") or f("uclaw_1"):
        return d(3645, h(7290), "uclaw")/r(3.5, h(7290))
    if f("claw_0"):
        return d(10935, h(21870))/r(3.5, h(21870))
    if f("claw") or f("claw_1"):
        return d(10935, h(21870), "claw")/r(3.5, h(21870))
    if f("qclaw_0"):
        return d(32805, h(65610))/r(3.5, h(65610))
    if f("qclaw") or f("qclaw_1"):
        return d(32805, h(65610), "qclaw")/r(3.5, h(65610))
    # clay
    if f("uclay") or f("uclay_0"):
        return d(3645, h(7290))/r(2, h(7290))
    if f("uclay_1"):
        return d(72900, h(7290))/r(2, h(7290))
    if f("clay") or f("clay_0"):
        return d(10935, h(21870))/r(2, h(21870))
    if f("clay_1"):
        return d(218700, h(21870))/r(2, h(21870))
    if f("qclay") or f("qclay_0"):
        return d(32805, h(65610))/r(2, h(65610))
    if f("qclay_1"):
        return d(656100, h(65610))/r(2, h(65610))
    # cog
    if f("ucog"):
        return d(13851, h(9477))/r(2.5, h(9477))
    if f("cog"):
        return d(41553, h(28431))/r(2.5, h(28431))
    if f("qcog"):
        return d(124659, h(85293))/r(2.5, h(85293))
    # coin
    if f("ucoin"):
        return d(10935, h(7290))/r(2.5, h(7290))
    if f("coin"):
        return d(32805, h(21870))/r(2.5, h(21870))
    if f("qcoin"):
        return d(98415, h(65610))/r(2.5, h(65610))
    # coral
    if f("ucoral"):
        return d(8019*3/7)/(r(1.5)+0.08)*7
    if f("coral"):
        return d(24057*3/7)/(r(1.5)+0.08)*7
    if f("qcoral"):
        return d(72171*3/7)/(r(1.5)+0.08)*7
    # corn
    if f("ucorn"):
        return d(5832, h(145800))/r(7, h(145800))
    if f("corn"):
        return d(17496, h(437400))/r(7, h(437400))
    if f("qcorn"):
        return d(52488, h(1312200))/r(7, h(1312200))
    # dandelion
    if f("udandelion"):
        return d(1944, h(1944))/r(1, h(1944))*(3+dup)
    if f("dandelion"):
        return d(5832, h(5832))/r(1, h(5832))*(3+dup)
    if f("qdandelion"):
        return d(17496, h(17496))/r(1, h(17496))*(3+dup)
    # dice
    if f("udice"):
        return d(7290*(2.7+1.36*luck), h(7290))/r(2.5, h(7290))
    if f("dice"):
        return d(21870*(2.7+1.36*luck), h(21870))/r(2.5, h(21870))
    if f("qdice"):
        return d(65610*(2.7+1.36*luck), h(65610))/r(2.5, h(65610))
    # domino
    if f("udomino"):
        return (d(0, h(11664))*7+d(729, h(11664))+d(729*2, h(11664))+d(729*3, h(11664))+d(729*4, h(11664))*2+d(729*5, h(11664))+d(729*6, h(11664))*2+d(729*8, h(11664))+d(729*9, h(11664))+d(729*10, h(11664))+d(729*12, h(11664))*2+d(729*15, h(11664))+d(729*16, h(11664))+d(729*18, h(11664))+d(729*20, h(11664))+d(729*24, h(11664))+d(729*25, h(11664))+d(729*30, h(11664))+d(729*36, h(11664)))/28/r(1.0, h(11664))
    if f("domino"):
        return (d(0, h(34992))*7+d(2187, h(34992))+d(2187*2, h(34992))+d(2187*3, h(34992))+d(2187*4, h(34992))*2+d(2187*5, h(34992))+d(2187*6, h(34992))*2+d(2187*8, h(34992))+d(2187*9, h(34992))+d(2187*10, h(34992))+d(2187*12, h(34992))*2+d(2187*15, h(34992))+d(2187*16, h(34992))+d(2187*18, h(34992))+d(2187*20, h(34992))+d(2187*24, h(34992))+d(2187*25, h(34992))+d(2187*30, h(34992))+d(2187*36, h(34992)))/28/r(1.0, h(34992))
    if f("qdomino"):
        return (d(0, h(104976))*7+d(6561, h(104976))+d(6561*2, h(104976))+d(6561*3, h(104976))+d(6561*4, h(104976))*2+d(6561*5, h(104976))+d(6561*6, h(104976))*2+d(6561*8, h(104976))+d(6561*9, h(104976))+d(6561*10, h(104976))+d(6561*12, h(104976))*2+d(6561*15, h(104976))+d(6561*16, h(104976))+d(6561*18, h(104976))+d(6561*20, h(104976))+d(6561*24, h(104976))+d(6561*25, h(104976))+d(6561*30, h(104976))+d(6561*36, h(104976)))/28/r(1.0, h(104976))
    # dust
    if f("udust"):
        return d(3159, h(1215))/r(0.8, h(1215))*(3+dup)
    if f("dust"):
        return d(9477, h(3645))/r(0.8, h(3645))*(3+dup)
    if f("qdust"):
        return d(28431, h(10935))/r(0.8, h(10935))*(3+dup)
    # agg
    if f("uagg"):
        return d(4374, mh(182250), "uagg")/mr(60, mh(182250))*(4+dup)
    if f("agg"):
        return d(13122, mh(546750), "agg")/mr(60, mh(547650))*(4+dup)
    if f("qagg"):
        return d(39366, mh(1640250), "qagg")/mr(60, mh(1640250))*(4+dup)
    # bgg
    if f("ubgg"):
        return d(5103, mh(364500), "ubgg")/mr(30, mh(1093500))
    if f("bgg"):
        return d(15309, mh(1093500), "bgg")/mr(30, mh(1093500))
    if f("qbgg"):
        return d(45927, mh(3280500), "qbgg")/mr(30, mh(3280500))
    # fang
    if f("ufang"):
        return d(10935)/r(3.5)
    if f("fang"):
        return d(32805)/r(3.5)
    if f("qfang"):
        return d(98415)/r(3.5)
    # faster
    if f("ufaster"):
        return d(8748, h(3645))/r(2.5, h(3645))
    if f("faster"):
        return d(26244, h(10935))/r(2.5, h(10935))
    if f("qfaster"):
        return d(78732, h(32805))/r(2.5, h(32805))
    # fragment/mjolnir
    if f("ufragment"):
        return d(364.5, h(364.5))/r(10, h(364.5))*2
    if f("fragment"):
        return d(729, h(729))/r(10, h(729))*3
    if f("qmjolnir") or f("qmjölnir"):
        return d(328050, h(328050), "qmjolnir")/r(8, h(328050))
    # glass
    if f("uglass"):
        return d(16038)
    if f("glass"):
        return d(48114)
    if f("qglass"):
        return d(144342)
    # grapes
    if f("ugrapes") or f("ugrapes_0"):
        return d(2187, h(3645))/r(1.5, h(3645))+(18225/0.7)*poison
    if f("ugrapes_1") or f("ugrapes_2") or f("ugrapes_3") or f("ugrapes_4") or f("ugrapes_5") or f("ugrapes_6"):
        return (d(2187, h(3645))/r(1.5, h(3645)+0.5)+(18225/0.7)*poison)*int(petal[8:])
    if f("grapes") or f("grapes_0"):
        return d(6561, h(10935))/r(1.5, h(10935))+(54675/0.7)*poison
    if f("grapes_1") or f("grapes_2") or f("grapes_3") or f("grapes_4") or f("grapes_5") or f("grapes_6"):
        return (d(6561, h(10935))/r(1.5, h(10935)+0.5)+(54675/0.7)*poison)*int(petal[7:])
    if f("qgrapes") or f("qgrapes_0"):
        return d(19683, h(32805))/r(1.5, h(32805))+(164025/0.7)*poison
    if f("qgrapes_1") or f("qgrapes_2") or f("qgrapes_3") or f("qgrapes_4") or f("qgrapes_5") or f("qgrapes_6"):
        return (d(19683, h(32805))/r(1.5, h(32805)+0.5)+(164025/0.7)*poison)*int(petal[8:])
    # heavy
    if f("uheavy"):
        return d(9477, h(109350))/r(10, h(109350))
    if f("heavy"):
        return d(28431, h(328050))/r(10, h(328050))
    if f("qheavy"):
        return d(85293, h(984150))/r(10, h(984150))
    # iris
    if f("uiris"):
        return d(3645, h(3645))/r(4, h(3645))+17010*poison
    if f("iris"):
        return d(10935, h(10935))/r(4, h(10935))+51030*poison
    if f("qiris"):
        return d(32805, h(32805))/r(4, h(32805))+153090*poison
    # jelly
    if f("ujelly"):
        return d(7290, h(7290))/hr(10, h(7290))
    if f("jelly"):
        return d(21870, h(21870))/hr(10, h(21870))
    if f("qjelly"):
        return d(65610, h(65610))/hr(10, h(65610))
    # laser
    if f("ulaser_0"):
        return d(3645, h(7290))/hr(5, h(7290))
    if f("ulaser") or f("ulaser_1"):
        return 36450
    if f("laser_0"):
        return d(10935, h(21870))/hr(5, h(21870))
    if f("laser") or f("laser_1"):
        return 109350
    if f("qlaser_0"):
        return d(32805, h(65610))/hr(5, h(65610))
    if f("qlaser") or f("laser_1"):
        return 328050
    # leaf/leaf(magic)
    if f("uleaf") or f("uleaf(magic)"):
        return d(11664, h(8748))/r(1.8, h(8748))
    if f("leaf") or f("leaf(magic)"):
        return d(34992, h(26244))/r(1.8, h(26244))
    if f("qleaf") or f("qleaf(magic)"):
        return d(104976, h(78732))/r(1.8, h(78732))
    # leaf(dead)
    if f("udl") or f("uleaf(dead)"):
        return d(11664, h(8748))/r(1.8/1.05, h(8748/petalhealth*(petalhealth-0.3)))
    if f("dl") or f("leaf(dead)"):
        return d(34992, h(26244))/r(1.8/1.05, h(26244/petalhealth*(petalhealth-0.45)))
    if f("qdl") or f("qleaf(dead)"):
        return d(104976, h(78732))/r(1.8/1.05, h(78732/petalhealth*(petalhealth-0.6)))
    # leaf(golden)
    if f("ugl") or f("uleaf(golden)"):
        return d(11664, h(8748))/r(2.5/0.825, h(8748))
    if f("gl") or f("leaf(golden)"):
        return d(34992, h(26244))/r(2.5/0.8, h(26244))
    if f("qgl") or f("qleaf(golden)"):
        return d(104976, h(78732))/r(2.5/0.775, h(78732))
    # lentil
    if f("ulentil"):
        return d(9477, h(8748))/r(2, h(8748))
    if f("lentil"):
        return d(28431, h(26244))/r(2, h(26244))
    if f("qlentil"):
        return d(85293, h(78732))/r(2, h(78732))
    # light
    if f("ulight"):
        return d(1895.4, h(729))/r(0.8, h(729))*(5+dup)
    if f("light"):
        return d(5686.2, h(2187))/r(0.8, h(2187))*(5+dup)
    if f("qlight"):
        return d(17058.6, h(6561))/r(0.8, h(6561))*(5+dup)
    # lightning
    if f("ulightning"):
        return d(8748, h(14580), "ulightning")/r(2.5)
    if f("lightning"):
        return d(26244, h(43740), "lightning")/r(2.5)
    if f("qlightning"):
        return d(78732, h(131220), "qlightning")/r(2.5)
    # missile/missile(mecha)
    if f("umissile_0") or f("umissile(mecha)_0"):
        return d(25515/5, h(1458))/r(1.5, h(1458))
    if f("umissile") or f("umissile_1") or f("umissile(mecha)") or f("umissile(mecha)_1"):
        return d(25515, h(1458))/(r(1.5, h(1458))+0.5)
    if f("missile_0") or f("missile(mecha)_0"):
        return d(76545/5, h(4374))/r(1.5, h(4374))
    if f("missile") or f("missile_1") or f("missile(mecha)") or f("missile(mecha)_1"):
        return d(76545, h(4374))/(r(1.5, h(4374))+0.5)
    if f("qmissile_0") or f("qmissile(mecha)_0"):
        return d(229635/5, h(13122))/r(1.5, h(13122))
    if f("qmissile") or f("qmissile_1") or f("qmissile(mecha)") or f("qmissile(mecha)_1"):
        return d(229635, h(13122))/(r(1.5, h(13122))+0.5)
    # missile(magic)
    # orange
    if f("uorange"):
        return d(5832, h(4860))/r(3.5, h(4860))*(3+dup)
    if f("orange"):
        return d(17496, h(14580))/r(3.5, h(14580))*(3+dup)
    if f("qorange"):
        return d(52488, h(43740))/r(3.5, h(43740))*(3+dup)
    # pearl
    if f("upearl") or f("upearl_0"):
        return d(14580, h(36450))/r(4, h(36450))
    if f("upearl_1"):
        return d(14580, h(36450))/(r(4, h(36450))+0.5)
    if f("pearl") or f("pearl_0"):
        return d(43740, h(109350))/r(4, h(109350))
    if f("pearl_1"):
        return d(43740, h(109350))/(r(4, h(109350))+0.5)
    if f("qpearl") or f("qpearl_0"):
        return d(131220, h(328050))/r(4, h(328050))
    if f("qpearl_1"):
        return d(131220, h(328050))/(r(4, h(328050))+0.5)
    # peas
    if f("upeas") or f("upeas_0"):
        return d(10935, h(3645))/r(1.5, h(3645))
    if f("upeas_1") or f("upeas_2") or f("upeas_3") or f("upeas_4") or f("upeas_5") or f("upeas_6"):
        return d(10935, h(3645))/(r(1.5, h(3645))+0.5)*int(petal[6:])
    if f("peas") or f("peas_0"):
        return d(32805, h(10935))/r(1.5, h(10935))
    if f("peas_1") or f("peas_2") or f("peas_3") or f("peas_4") or f("peas_5") or f("peas_6"):
        return d(32805, h(10935))/(r(1.5, h(10935))+0.5)*int(petal[5:])
    if f("qpeas") or f("qpeas_0"):
        return d(98415, h(32805))/r(1.5, h(32805))
    if f("qpeas_1") or f("qpeas_2") or f("qpeas_3") or f("qpeas_4") or f("qpeas_5") or f("qpeas_6"):
        return d(98415, h(32805))/(r(1.5, h(32805))+0.5)*int(petal[6:])
    # pincer
    if f("upincer"):
        return d(3645, h(3645))/r(2.5, h(3645))+14580*poison
    if f("pincer"):
        return d(10935, h(10935))/r(2.5, h(10935))+43740*poison
    if f("qpincer"):
        return d(32805, h(32805))/r(2.5, h(32805))+131220*poison
    # pollen
    if f("upollen_0"):
        return d(9234, h(1215))/r(2, h(1215))*(3+dup)
    if f("upollen") or f("upollen_1"):
        return d(9234, h(1215))/(r(2, h(1215))+0.5)*(3+dup)
    if f("pollen_0"):
        return d(27702, h(3645))/r(2, h(3645))*(3+dup)
    if f("pollen") or f("pollen_1"):
        return d(27702, h(3645))/(r(2, h(3645))+0.5)*(3+dup)
    if f("qpollen_0"):
        return d(83106, h(10935))/r(2, h(10935))*(3+dup)
    if f("qpollen") or f("qpollen_1"):
        return d(83106, h(10935))/(r(2, h(10935))+0.5)*(3+dup)
    # privet
    if f("uprivet_ug"):
        return (18225/0.7)*poison*0.2/r(4*0.7**6)
    if f("uprivet_ui"):
        return 17010*poison*0.2/r(4*0.7**6)
    if f("uprivet_up"):
        return 14580*poison*0.2/r(4*0.7**6)
    if f("uprivet_uu"):
        return 36450*poison*0.2/r(4*0.7**6)
    if f("privet_ug"):
        return (18225/0.7)*poison*0.2/r(4*0.7**7)
    if f("privet_ui"):
        return 17010*poison*0.2/r(4*0.7**7)
    if f("privet_up"):
        return 14580*poison*0.2/r(4*0.7**7)
    if f("privet_uu"):
        return 36450*poison*0.2/r(4*0.7**7)
    if f("qprivet_ug"):
        return (18225/0.7)*poison*0.2/r(4*0.7**8)
    if f("qprivet_ui"):
        return 17010*poison*0.2/r(4*0.7**8)
    if f("qprivet_up"):
        return 14580*poison*0.2/r(4*0.7**8)
    if f("qprivet_uu"):
        return 36450*poison*0.2/r(4*0.7**8)
    if f("uprivet_g"):
        return (54675/0.7)*poison*0.2/r(4*0.7**6)
    if f("uprivet_i"):
        return 51030*poison*0.2/r(4*0.7**6)
    if f("uprivet_p"):
        return 43740*poison*0.2/r(4*0.7**6)
    if f("uprivet_u"):
        return 109350*poison*0.2/r(4*0.7**6)
    if f("privet_g"):
        return (54675/0.7)*poison*0.2/r(4*0.7**7)
    if f("privet_i"):
        return 51030*poison*0.2/r(4*0.7**7)
    if f("privet_p"):
        return 43740*poison*0.2/r(4*0.7**7)
    if f("privet_u"):
        return 109350*poison*0.2/r(4*0.7**7)
    if f("qprivet_g"):
        return (54675/0.7)*poison*0.2/r(4*0.7**8)
    if f("qprivet_i"):
        return 51030*poison*0.2/r(4*0.7**8)
    if f("qprivet_p"):
        return 43740*poison*0.2/r(4*0.7**8)
    if f("qprivet_u"):
        return 109350*poison*0.2/r(4*0.7**8)
    if f("uprivet_qg"):
        return (164025/0.7)*poison*0.2/r(4*0.7**6)
    if f("uprivet_qi"):
        return 153090*poison*0.2/r(4*0.7**6)
    if f("uprivet_qp"):
        return 131220*poison*0.2/r(4*0.7**6)
    if f("uprivet_qu"):
        return 328050*poison*0.2/r(4*0.7**6)
    if f("privet_qg"):
        return (164025/0.7)*poison*0.2/r(4*0.7**7)
    if f("privet_qi"):
        return 153090*poison*0.2/r(4*0.7**7)
    if f("privet_qp"):
        return 131220*poison*0.2/r(4*0.7**7)
    if f("privet_qu"):
        return 328050*poison*0.2/r(4*0.7**7)
    if f("qprivet_qg"):
        return (164025/0.7)*poison*0.2/r(4*0.7**8)
    if f("qprivet_qi"):
        return 153090*poison*0.2/r(4*0.7**8)
    if f("qprivet_qp"):
        return 131220*poison*0.2/r(4*0.7**8)
    if f("qprivet_qu"):
        return 328050*poison*0.2/r(4*0.7**8)
    # rice
    if f("urice"):
        return d(2916, h(729))/r(0.05, h(729))
    if f("rice"):
        return d(8748, h(2187))/r(0.05, h(2187))
    if f("qrice"):
        return d(26244, h(6561))/r(0.05, h(6561))
    # rock
    if f("urock"):
        return d(16038, h(21870))/r(3, h(21870))
    if f("rock"):
        return d(48114, h(65610))/r(3, h(65610))
    if f("qrock"):
        return d(144342, h(196830))/r(3, h(196830))
    # sand
    if f("usand"):
        return d(3645, h(911.25))/r(1.5, h(911.25))*(4+dup)
    if f("sand"):
        return d(10935, h(2733.75))/r(1.5, h(2733.75))*(4+dup)
    if f("qsand"):
        return d(32805, h(8201.25))/r(1.5, h(8201.25))*(4+dup)
    # sawblade
    if f("usawblade"):
        return d(29160, h(18225))/r(2.5, h(18225))
    if f("sawblade"):
        return d(87480, h(54675))/r(2.5, h(54675))
    if f("qsawblade"):
        return d(262440, h(164025))/r(2.5, h(164025))
    # starfish
    if f("ustarfish"):
        return d(3645, h(5103))/r(1.5, h(5103))
    if f("starfish"):
        return d(10935, h(15309))/r(1.5, h(15309))
    if f("qstarfish"):
        return d(32805, h(45927))/r(1.5, h(45927))
    # stick
    if f("ustick"):
        return d(65610, mh(65610), "ustick")/5*4
    if f("stick"):
        return d(65610, mh(65610), "stick")/5*4
    if f("qstick"):
        return d(65610, mh(65610), "qstick")/5*4
    # stinger
    if f("ustinger"):
        return d(14580)/r(10)*(5+dup)
    if f("stinger"):
        return d(43740)/r(10)*(5+dup)
    if f("qstinger"):
        return d(131220)/r(10)*(5+dup)
    # stinger(blood)
    if f("ustinger(blood)"):
        return d(14580)/r(7.5)*(5+dup)
    if f("stinger(blood)"):
        return d(43740)/r(7.5)*(5+dup)
    if f("qstinger(blood)"):
        return d(131220)/r(7.5)*(5+dup)
    # stinger(magic)
    # tomato
    if f("utomato_0"):
        return d(3645, h(7290))/r(2.5, h(7290))
    if f("utomato") or f("utomato_1"):
        return d(51030, h(7290))/(r(2.5, h(7290))+1)
    if f("tomato_0"):
        return d(10935, h(21870))/r(2.5, h(21870))
    if f("tomato") or f("tomato_1"):
        return d(153090, h(21870))/(r(2.5, h(21870))+1)
    if f("qtomato_0"):
        return d(32805, h(65610))/r(2.5, h(65610))
    if f("qtomato") or f("qtomato_1"):
        return d(459270, h(65610))/(r(2.5, h(65610))+1)
    # triangle
    if f("utriangle"):
        return d(3645+2916*(utri-1), h(7290))/r(2.0, h(7290))
    if f("triangle"):
        return d(10935+8748*(tri-1), h(21870))/r(2.0, h(21870))
    if f("qtriangle"):
        return d(32805+26244*tri, h(65610))/r(2.0, h(65610))
    # uranium
    if f("uuranium"):
        return 36450*poison
    if f("uranium"):
        return 109350*poison
    if f("quranium"):
        return 328050*poison
    # web(electric)
    if f("uweb(electric)"):
        return 3645
    if f("web(electric)"):
        return 10935
    if f("qweb(electric)"):
        return 32805
    # wing
    if f("uwing"):
        return d(14580, h(7290))/r(3, h(7290))
    if f("wing"):
        return d(43740, h(21870))/r(3, h(21870))
    if f("qwing"):
        return d(131220, h(65610))/r(3, h(65610))
    # yucca
    if f("uyucca"):
        return d(3645, h(7290))/r(2.5, h(7290))
    if f("yucca"):
        return d(10935, h(21870))/r(2.5, h(21870))
    if f("qyucca"):
        return d(32805, h(65610))/r(2.5, h(65610))
    return 0


def calw(petal, angle):
    def f(name):
        return petal == name

    def g(rel):
        ang = angle/360
        try:
            lap = floor(rel/T)
            return ceil(T*ang/(rel-lap*T))/(lap*ceil(T*ang/(rel-lap*T))+1)
        except ZeroDivisionError:
            return round(rel/T)
        # if rel == T:
        #     return 1
        # if rel < T*ang:
        #     return ceil(T*ang/rel)
        # elif T*ang <= rel <= T:
        #     return 1
        # elif T < rel < T+T*ang:
        #     return ceil(T*ang/(rel-T))/(ceil(T*ang/(rel-T))+1)
        # elif T+T*ang <= rel <= 2*T:
        #     return 1/2
        # elif 2*T < rel < 2*T+T*ang:
        #     return ceil(T*ang/(rel-2*T))/(2*ceil(T*ang/(rel-2*T))+1)

    # basic/clover/salt/talisman/yinyang
    if f("ubasic") or f("uclover") or f("usalt") or f("utalisman") or f("uyinyang"):
        return d(7290, h(7290))/T*g(r(2.5, h(7290)))
    if f("basic") or f("clover") or f("salt") or f("talisman") or f("yinyang"):
        return d(21870, h(21870))/T*g(r(2.5, h(21870)))
    if f("qbasic") or f("qclover") or f("qsalt") or f("qtalisman") or f("qyinyang") or f("tbasic"):
        return d(65610, h(65610))/T*g(r(2.5, h(65610)))
    # battery
    if f("ubattery"):
        return d(26244, h(1), "ubattery")/(r(2.5)+0.1)
    if f("battery"):
        return d(78732, h(1), "battery")/(r(2.5)+0.1)
    if f("qbattery"):
        return d(236196, h(1), "qbattery")/(r(2.5)+0.1)
    # bean
    if f("ubean") or f("ubean_0"):
        return d(14580, h(8748))/T*g(r(2, h(8748)))
    if f("ubean_1"):
        return d(21870, h(8748))/T*g(r(2, h(8748)))
    if f("bean") or f("bean_0"):
        return d(43740, h(26244))/T*g(r(2, h(26244)))
    if f("bean_1"):
        return d(65610, h(26244))/T*g(r(2, h(26244)))
    if f("qbean") or f("qbean_0"):
        return d(131220, h(78732))/T*g(r(2, h(78732)))
    if f("qbean_1"):
        return d(196830, h(78732))/T*g(r(2, h(78732)))
    # blueberries
    # bone
    if f("ubone"):
        return d(10206, h(7290), "ubone")/T*g(r(2.5, h(7290)+14580))
    if f("bone"):
        return d(30618, h(21870), "bone")/T*g(r(2.5, h(21870)+43740))
    if f("qbone"):
        return d(91854, h(65610), "qbone")/T*g(r(2.5, h(65610)+131220))
    # broccoli
    if f("ubroccoli") or f("ubroccoli_0"):
        return d(10935, h(7290))/T*g(r(2.8, h(7290)))
    if f("ubroccoli_1") or f("ubroccoli_2") or f("ubroccoli_3"):
        return (d(10935, h(7290))+int(petal[10:])*d(3645, h(2430)))/T*g(r(2.8, h(7290)))
    if f("broccoli") or f("broccoli_0"):
        return d(32805, h(21870))/T*g(r(2.8, h(21870)))
    if f("broccoli_1") or f("broccoli_2") or f("broccoli_3"):
        return (d(32805, h(21870))+int(petal[9:])*d(10935, h(7290)))/T*g(r(2.8, h(21870)))
    if f("qbroccoli") or f("qbroccoli_0"):
        return d(98415, h(65610))/T*g(r(2.8, h(65610)))
    if f("qbroccoli_1") or f("qbroccoli_2") or f("qbroccoli_3"):
        return (d(98415, h(65610))+int(petal[10:])*d(32805, h(21870)))/T*g(r(2.8, h(65610)))
    # bur
    if f("ubur"):
        return d(3645, h(3645))/T*g(r(2, h(3645)))
    if f("bur"):
        return d(10935, h(10935))/T*g(r(2, h(10935)))
    if f("qbur"):
        return d(32805, h(32805))/T*g(r(2, h(32805)))
    # cactus/cactus(magic)
    if f("ucactus") or f("ucactus_magic"):
        return d(5103, h(10935))/T*g(r(1, h(10935)))
    if f("cactus") or f("cactus_magic"):
        return d(15309, h(32805))/T*g(r(1, h(32805)))
    if f("qcactus") or f("qcactus_magic"):
        return d(45927, h(98415))/T*g(r(1, h(98415)))
    # card
    if f("ucard"):
        return (d(3645, h(21870))/r(2.5, h(21870))+d(7290, h(18225))/r(2.5, h(18225))+d(10935, h(14580))/r(2.5, h(14580))+d(14580, h(10935))/T*g(r(2.5, h(10935))))/4
    if f("card"):
        return (d(10935, h(65610))/r(2.5, h(65610))+d(21870, h(54675))/r(2.5, h(54675))+d(32805, h(43740))/r(2.5, h(43740))+d(43740, h(32805))/T*g(r(2.5, h(32805))))/4
    if f("qcard"):
        return (d(32805, h(196830))/r(2.5, h(196830))+d(65610, h(164025))/r(2.5, h(164025))+d(98415, h(131220))/r(2.5, h(131220))+d(131220, h(98415))/T*g(r(2.5, h(98415))))/4
    # carrot
    if f("ucarrot_0"):
        return d(13122/5, h(13122))/T*g(r(1, h(13122)))
    if f("carrot_0"):
        return d(39366/5, h(39366))/T*g(r(1, h(39366)))
    if f("qcarrot_0"):
        return d(118098/5, h(118098))/T*g(r(1, h(118098)))
    if f("ucarrot") or f("ucarrot_1"):
        return d(13122, h(13122))/T*g((r(1, h(13122))+0.5))
    if f("carrot") or f("carrot_1"):
        return d(39366, h(39366))/T*g((r(1, h(39366))+0.5))
    if f("qcarrot") or f("carrot_1"):
        return d(118098, h(118098))/T*g((r(1, h(118098))+0.5))
    # chip
    if f("uchip"):
        return d(5103, h(2187))*10/T*g((r(2.5, h(2187))+0.9**10/(1-0.9**10)*0.04))
    if f("chip"):
        return d(15309, h(2187))*10/T*g((r(2.5, h(2187))+0.9**10/(1-0.9**10)*0.04))
    if f("qchip"):
        return d(45927, h(2187))*10/T*g((r(2.5, h(2187))+0.9**10/(1-0.9**10)*0.04))
    # claw
    if f("uclaw_0"):
        return d(3645, h(7290))/T*g(r(3.5, h(7290)))
    if f("uclaw") or f("uclaw_1"):
        return d(3645, h(7290), "uclaw")/T*g(r(3.5, h(7290)))
    if f("claw_0"):
        return d(10935, h(21870))/T*g(r(3.5, h(21870)))
    if f("claw") or f("claw_1"):
        return d(10935, h(21870), "claw")/T*g(r(3.5, h(21870)))
    if f("qclaw_0"):
        return d(32805, h(65610))/T*g(r(3.5, h(65610)))
    if f("qclaw") or f("qclaw_1"):
        return d(32805, h(65610), "qclaw")/T*g(r(3.5, h(65610)))
    # clay
    if f("uclay") or f("uclay_0"):
        return d(3645, h(7290))/T*g(r(2, h(7290)))
    if f("uclay_1"):
        return d(72900, h(7290))/T*g(r(2, h(7290)))
    if f("clay") or f("clay_0"):
        return d(10935, h(21870))/T*g(r(2, h(21870)))
    if f("clay_1"):
        return d(218700, h(21870))/T*g(r(2, h(21870)))
    if f("qclay") or f("qclay_0"):
        return d(32805, h(65610))/T*g(r(2, h(65610)))
    if f("qclay_1"):
        return d(656100, h(65610))/T*g(r(2, h(65610)))
    # cog
    if f("ucog"):
        return d(13851, h(9477))/T*g(r(2.5, h(9477)))
    if f("cog"):
        return d(41553, h(28431))/T*g(r(2.5, h(28431)))
    if f("qcog"):
        return d(124659, h(85293))/T*g(r(2.5, h(85293)))
    # coin
    if f("ucoin"):
        return d(10935, h(7290))/T*g(r(2.5, h(7290)))
    if f("coin"):
        return d(32805, h(21870))/T*g(r(2.5, h(21870)))
    if f("qcoin"):
        return d(98415, h(65610))/T*g(r(2.5, h(65610)))
    # coral
    if f("ucoral"):
        return d(8019*3/7)/T*g((r(1.5)+0.08))*7
    if f("coral"):
        return d(24057*3/7)/T*g((r(1.5)+0.08))*7
    if f("qcoral"):
        return d(72171*3/7)/T*g((r(1.5)+0.08))*7
    # corn
    if f("ucorn"):
        return d(5832, h(145800))/T*g(r(7, h(145800)))
    if f("corn"):
        return d(17496, h(437400))/T*g(r(7, h(437400)))
    if f("qcorn"):
        return d(52488, h(1312200))/T*g(r(7, h(1312200)))
    # dandelion
    if f("udandelion"):
        return d(1944, h(1944))/T*g(r(1, h(1944)))*(3+dup)
    if f("dandelion"):
        return d(5832, h(5832))/T*g(r(1, h(5832)))*(3+dup)
    if f("qdandelion"):
        return d(17496, h(17496))/T*g(r(1, h(17496)))*(3+dup)
    # dice
    if f("udice"):
        return d(7290*(2.7+1.36*luck), h(7290))/T*g(r(2.5, h(7290)))
    if f("dice"):
        return d(21870*(2.7+1.36*luck), h(21870))/T*g(r(2.5, h(21870)))
    if f("qdice"):
        return d(65610*(2.7+1.36*luck), h(65610))/T*g(r(2.5, h(65610)))
    # domino
    if f("udomino"):
        return (d(0, h(11664))*7+d(729, h(11664))+d(729*2, h(11664))+d(729*3, h(11664))+d(729*4, h(11664))*2+d(729*5, h(11664))+d(729*6, h(11664))*2+d(729*8, h(11664))+d(729*9, h(11664))+d(729*10, h(11664))+d(729*12, h(11664))*2+d(729*15, h(11664))+d(729*16, h(11664))+d(729*18, h(11664))+d(729*20, h(11664))+d(729*24, h(11664))+d(729*25, h(11664))+d(729*30, h(11664))+d(729*36, h(11664)))/T*g(r(1.0, h(11664)))/28
    if f("domino"):
        return (d(0, h(34992))*7+d(2187, h(34992))+d(2187*2, h(34992))+d(2187*3, h(34992))+d(2187*4, h(34992))*2+d(2187*5, h(34992))+d(2187*6, h(34992))*2+d(2187*8, h(34992))+d(2187*9, h(34992))+d(2187*10, h(34992))+d(2187*12, h(34992))*2+d(2187*15, h(34992))+d(2187*16, h(34992))+d(2187*18, h(34992))+d(2187*20, h(34992))+d(2187*24, h(34992))+d(2187*25, h(34992))+d(2187*30, h(34992))+d(2187*36, h(34992)))/T*g(r(1.0, h(34992)))/28
    if f("qdomino"):
        return (d(0, h(104976))*7+d(6561, h(104976))+d(6561*2, h(104976))+d(6561*3, h(104976))+d(6561*4, h(104976))*2+d(6561*5, h(104976))+d(6561*6, h(104976))*2+d(6561*8, h(104976))+d(6561*9, h(104976))+d(6561*10, h(104976))+d(6561*12, h(104976))*2+d(6561*15, h(104976))+d(6561*16, h(104976))+d(6561*18, h(104976))+d(6561*20, h(104976))+d(6561*24, h(104976))+d(6561*25, h(104976))+d(6561*30, h(104976))+d(6561*36, h(104976)))/T*g(r(1.0, h(104976)))/28
    # dust
    if f("udust"):
        return d(3159, h(1215))/T*g(r(0.8, h(1215))*(3+dup))
    if f("dust"):
        return d(9477, h(3645))/T*g(r(0.8, h(3645))*(3+dup))
    if f("qdust"):
        return d(28431, h(10935))/T*g(r(0.8, h(10935))*(3+dup))
    # agg
    if f("uagg"):
        return d(4374, mh(182250), "uagg")/T*g(mr(60, mh(182250)))*(4+dup)
    if f("agg"):
        return d(13122, mh(546750), "agg")/T*g(mr(60, mh(547650)))*(4+dup)
    if f("qagg"):
        return d(39366, mh(1640250), "qagg")/T*g(mr(60, mh(1640250)))*(4+dup)
    # bgg
    if f("ubgg"):
        return d(5103, mh(364500), "ubgg")/T*g(mr(30, mh(1093500)))
    if f("bgg"):
        return d(15309, mh(1093500), "bgg")/T*g(mr(30, mh(1093500)))
    if f("qbgg"):
        return d(45927, mh(3280500), "qbgg")/T*g(mr(30, mh(3280500)))
    # fang
    if f("ufang"):
        return d(10935)/T*g(r(3.5))
    if f("fang"):
        return d(32805)/T*g(r(3.5))
    if f("qfang"):
        return d(98415)/T*g(r(3.5))
    # faster
    if f("ufaster"):
        return d(8748, h(3645))/T*g(r(2.5, h(3645)))
    if f("faster"):
        return d(26244, h(10935))/T*g(r(2.5, h(10935)))
    if f("qfaster"):
        return d(78732, h(32805))/T*g(r(2.5, h(32805)))
    # fragment/mjolnir
    if f("ufragment"):
        return d(364.5, h(364.5))/T*g(r(10, h(364.5)))*2
    if f("fragment"):
        return d(729, h(729))/T*g(r(10, h(729)))*3
    if f("qmjolnir") or f("qmjölnir"):
        return d(328050, h(328050), "qmjolnir")/T*g(r(8, h(328050)))
    # glass
    if f("uglass"):
        return d(16038)/T*g(1)
    if f("glass"):
        return d(48114)/T*g(1)
    if f("qglass"):
        return d(144342)/T*g(1)
    # grapes
    if f("ugrapes") or f("ugrapes_0"):
        return d(2187, h(3645))/T*g(r(1.5, h(3645)))+(18225/0.7)*poison
    if f("ugrapes_1") or f("ugrapes_2") or f("ugrapes_3") or f("ugrapes_4") or f("ugrapes_5") or f("ugrapes_6"):
        return (d(2187, h(3645))/T*g(r(1.5, h(3645)+0.5))+(18225/0.7)*poison)*int(petal[8:])
    if f("grapes") or f("grapes_0"):
        return d(6561, h(10935))/T*g(r(1.5, h(10935)))+(54675/0.7)*poison
    if f("grapes_1") or f("grapes_2") or f("grapes_3") or f("grapes_4") or f("grapes_5") or f("grapes_6"):
        return (d(6561, h(10935))/T*g(r(1.5, h(10935)+0.5))+(54675/0.7)*poison)*int(petal[7:])
    if f("qgrapes") or f("qgrapes_0"):
        return d(19683, h(32805))/T*g(r(1.5, h(32805)))+(164025/0.7)*poison
    if f("qgrapes_1") or f("qgrapes_2") or f("qgrapes_3") or f("qgrapes_4") or f("qgrapes_5") or f("qgrapes_6"):
        return (d(19683, h(32805))/T*g(r(1.5, h(32805)+0.5))+(164025/0.7)*poison)*int(petal[8:])
    # heavy
    if f("uheavy"):
        return d(9477, h(109350))/T*g(r(10, h(109350)))
    if f("heavy"):
        return d(28431, h(328050))/T*g(r(10, h(328050)))
    if f("qheavy"):
        return d(85293, h(984150))/T*g(r(10, h(984150)))
    # iris
    if f("uiris"):
        return d(3645, h(3645))/T*g(r(4, h(3645)))+17010*poison
    if f("iris"):
        return d(10935, h(10935))/T*g(r(4, h(10935)))+51030*poison
    if f("qiris"):
        return d(32805, h(32805))/T*g(r(4, h(32805)))+153090*poison
    # jelly
    if f("ujelly"):
        return d(7290, h(7290))/T*g(hr(10, h(7290)))
    if f("jelly"):
        return d(21870, h(21870))/T*g(hr(10, h(21870)))
    if f("qjelly"):
        return d(65610, h(65610))/T*g(hr(10, h(65610)))
    # laser
    if f("ulaser_0"):
        return d(3645, h(7290))/T*g(hr(5, h(7290)))
    if f("ulaser") or f("ulaser_1"):
        return 36450
    if f("laser_0"):
        return d(10935, h(21870))/T*g(hr(5, h(21870)))
    if f("laser") or f("laser_1"):
        return 109350
    if f("qlaser_0"):
        return d(32805, h(65610))/T*g(hr(5, h(65610)))
    if f("qlaser") or f("laser_1"):
        return 328050
    # leaf/leaf(magic)
    if f("uleaf") or f("uleaf(magic)"):
        return d(11664, h(8748))/T*g(r(1.8, h(8748)))
    if f("leaf") or f("leaf(magic)"):
        return d(34992, h(26244))/T*g(r(1.8, h(26244)))
    if f("qleaf") or f("qleaf(magic)"):
        return d(104976, h(78732))/T*g(r(1.8, h(78732)))
    # leaf(dead)
    if f("udl") or f("uleaf(dead)"):
        return d(11664, h(8748))/T*g(r(1.8/1.05, h(8748/petalhealth*(petalhealth-0.3))))
    if f("dl") or f("leaf(dead)"):
        return d(34992, h(26244))/T*g(r(1.8/1.05, h(26244/petalhealth*(petalhealth-0.45))))
    if f("qdl") or f("qleaf(dead)"):
        return d(104976, h(78732))/T*g(r(1.8/1.05, h(78732/petalhealth*(petalhealth-0.6))))
    # leaf(golden)
    if f("ugl") or f("uleaf(golden)"):
        return d(11664, h(8748))/T*g(r(2.5/0.825, h(8748)))
    if f("gl") or f("leaf(golden)"):
        return d(34992, h(26244))/T*g(r(2.5/0.8, h(26244)))
    if f("qgl") or f("qleaf(golden)"):
        return d(104976, h(78732))/T*g(r(2.5/0.775, h(78732)))
    # lentil
    if f("ulentil"):
        return d(9477, h(8748))/T*g(r(2, h(8748)))
    if f("lentil"):
        return d(28431, h(26244))/T*g(r(2, h(26244)))
    if f("qlentil"):
        return d(85293, h(78732))/T*g(r(2, h(78732)))
    # light
    if f("ulight"):
        return d(1895.4, h(729))/T*g(r(0.8, h(729)))*(5+dup)
    if f("light"):
        return d(5686.2, h(2187))/T*g(r(0.8, h(2187)))*(5+dup)
    if f("qlight"):
        return d(17058.6, h(6561))/T*g(r(0.8, h(6561)))*(5+dup)
    # lightning
    if f("ulightning"):
        return d(8748, h(14580), "ulightning")/T*g(r(2.5))
    if f("lightning"):
        return d(26244, h(43740), "lightning")/T*g(r(2.5))
    if f("qlightning"):
        return d(78732, h(131220), "qlightning")/T*g(r(2.5))
    # missile/missile(mecha)
    if f("umissile_0") or f("umissile(mecha)_0"):
        return d(25515/5, h(1458))/T*g(r(1.5, h(1458)))
    if f("umissile") or f("umissile_1") or f("umissile(mecha)") or f("umissile(mecha)_1"):
        return d(25515, h(1458))/T*g((r(1.5, h(1458))+0.5))
    if f("missile_0") or f("missile(mecha)_0"):
        return d(76545/5, h(4374))/T*g(r(1.5, h(4374)))
    if f("missile") or f("missile_1") or f("missile(mecha)") or f("missile(mecha)_1"):
        return d(76545, h(4374))/T*g((r(1.5, h(4374))+0.5))
    if f("qmissile_0") or f("qmissile(mecha)_0"):
        return d(229635/5, h(13122))/T*g(r(1.5, h(13122)))
    if f("qmissile") or f("qmissile_1") or f("qmissile(mecha)") or f("qmissile(mecha)_1"):
        return d(229635, h(13122))/T*g((r(1.5, h(13122))+0.5))
    # missile(magic)
    # orange
    if f("uorange"):
        return d(5832, h(4860))/T*g(r(3.5, h(4860)))*(3+dup)
    if f("orange"):
        return d(17496, h(14580))/T*g(r(3.5, h(14580)))*(3+dup)
    if f("qorange"):
        return d(52488, h(43740))/T*g(r(3.5, h(43740)))*(3+dup)
    # pearl
    if f("upearl") or f("upearl_0"):
        return d(14580, h(36450))/T*g(r(4, h(36450)))
    if f("upearl_1"):
        return d(14580, h(36450))/T*g((r(4, h(36450))+0.5))
    if f("pearl") or f("pearl_0"):
        return d(43740, h(109350))/T*g(r(4, h(109350)))
    if f("pearl_1"):
        return d(43740, h(109350))/T*g((r(4, h(109350))+0.5))
    if f("qpearl") or f("qpearl_0"):
        return d(131220, h(328050))/T*g(r(4, h(328050)))
    if f("qpearl_1"):
        return d(131220, h(328050))/T*g((r(4, h(328050))+0.5))
    # peas
    if f("upeas") or f("upeas_0"):
        return d(10935, h(3645))/T*g(r(1.5, h(3645)))
    if f("upeas_1") or f("upeas_2") or f("upeas_3") or f("upeas_4") or f("upeas_5") or f("upeas_6"):
        return d(10935, h(3645))/T*g((r(1.5, h(3645))+0.5))*int(petal[6:])
    if f("peas") or f("peas_0"):
        return d(32805, h(10935))/T*g(r(1.5, h(10935)))
    if f("peas_1") or f("peas_2") or f("peas_3") or f("peas_4") or f("peas_5") or f("peas_6"):
        return d(32805, h(10935))/T*g((r(1.5, h(10935))+0.5))*int(petal[5:])
    if f("qpeas") or f("qpeas_0"):
        return d(98415, h(32805))/T*g(r(1.5, h(32805)))
    if f("qpeas_1") or f("qpeas_2") or f("qpeas_3") or f("qpeas_4") or f("qpeas_5") or f("qpeas_6"):
        return d(98415, h(32805))/T*g((r(1.5, h(32805))+0.5))*int(petal[6:])
    # pincer
    if f("upincer"):
        return d(3645, h(3645))/T*g(r(2.5, h(3645)))+14580*poison
    if f("pincer"):
        return d(10935, h(10935))/T*g(r(2.5, h(10935)))+43740*poison
    if f("qpincer"):
        return d(32805, h(32805))/T*g(r(2.5, h(32805)))+131220*poison
    # pollen
    if f("upollen_0"):
        return d(9234, h(1215))/T*g(r(2, h(1215)))*(3+dup)
    if f("upollen") or f("upollen_1"):
        return d(9234, h(1215))/T*g((r(2, h(1215))+0.5))*(3+dup)
    if f("pollen_0"):
        return d(27702, h(3645))/T*g(r(2, h(3645)))*(3+dup)
    if f("pollen") or f("pollen_1"):
        return d(27702, h(3645))/T*g((r(2, h(3645))+0.5))*(3+dup)
    if f("qpollen_0"):
        return d(83106, h(10935))/T*g(r(2, h(10935)))*(3+dup)
    if f("qpollen") or f("qpollen_1"):
        return d(83106, h(10935))/T*g((r(2, h(10935))+0.5))*(3+dup)
    # privet
    if f("uprivet_ug"):
        return (18225/0.7)*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_ui"):
        return 17010*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_up"):
        return 14580*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_uu"):
        return 36450*poison*0.2/T*g(r(4*0.7**6))
    if f("privet_ug"):
        return (18225/0.7)*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_ui"):
        return 17010*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_up"):
        return 14580*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_uu"):
        return 36450*poison*0.2/T*g(r(4*0.7**7))
    if f("qprivet_ug"):
        return (18225/0.7)*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_ui"):
        return 17010*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_up"):
        return 14580*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_uu"):
        return 36450*poison*0.2/T*g(r(4*0.7**8))
    if f("uprivet_g"):
        return (54675/0.7)*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_i"):
        return 51030*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_p"):
        return 43740*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_u"):
        return 109350*poison*0.2/T*g(r(4*0.7**6))
    if f("privet_g"):
        return (54675/0.7)*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_i"):
        return 51030*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_p"):
        return 43740*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_u"):
        return 109350*poison*0.2/T*g(r(4*0.7**7))
    if f("qprivet_g"):
        return (54675/0.7)*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_i"):
        return 51030*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_p"):
        return 43740*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_u"):
        return 109350*poison*0.2/T*g(r(4*0.7**8))
    if f("uprivet_qg"):
        return (164025/0.7)*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_qi"):
        return 153090*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_qp"):
        return 131220*poison*0.2/T*g(r(4*0.7**6))
    if f("uprivet_qu"):
        return 328050*poison*0.2/T*g(r(4*0.7**6))
    if f("privet_qg"):
        return (164025/0.7)*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_qi"):
        return 153090*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_qp"):
        return 131220*poison*0.2/T*g(r(4*0.7**7))
    if f("privet_qu"):
        return 328050*poison*0.2/T*g(r(4*0.7**7))
    if f("qprivet_qg"):
        return (164025/0.7)*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_qi"):
        return 153090*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_qp"):
        return 131220*poison*0.2/T*g(r(4*0.7**8))
    if f("qprivet_qu"):
        return 328050*poison*0.2/T*g(r(4*0.7**8))
    # rice
    if f("urice"):
        return d(2916, h(729))/T*g(r(0.05, h(729)))
    if f("rice"):
        return d(8748, h(2187))/T*g(r(0.05, h(2187)))
    if f("qrice"):
        return d(26244, h(6561))/T*g(r(0.05, h(6561)))
    # rock
    if f("urock"):
        return d(16038, h(21870))/T*g(r(3, h(21870)))
    if f("rock"):
        return d(48114, h(65610))/T*g(r(3, h(65610)))
    if f("qrock"):
        return d(144342, h(196830))/T*g(r(3, h(196830)))
    # sand
    if f("usand"):
        return d(3645, h(911.25))/T*g(r(1.5, h(911.25)))*(4+dup)
    if f("sand"):
        return d(10935, h(2733.75))/T*g(r(1.5, h(2733.75)))*(4+dup)
    if f("qsand"):
        return d(32805, h(8201.25))/T*g(r(1.5, h(8201.25)))*(4+dup)
    # sawblade
    if f("usawblade"):
        return d(29160, h(18225))/T*g(r(2.5, h(18225)))
    if f("sawblade"):
        return d(87480, h(54675))/T*g(r(2.5, h(54675)))
    if f("qsawblade"):
        return d(262440, h(164025))/T*g(r(2.5, h(164025)))
    # starfish
    if f("ustarfish"):
        return d(3645, h(5103))/T*g(r(1.5, h(5103)))
    if f("starfish"):
        return d(10935, h(15309))/T*g(r(1.5, h(15309)))
    if f("qstarfish"):
        return d(32805, h(45927))/T*g(r(1.5, h(45927)))
    # stick
    if f("ustick"):
        return d(65610, mh(65610), "ustick")/5*4
    if f("stick"):
        return d(65610, mh(65610), "stick")/5*4
    if f("qstick"):
        return d(65610, mh(65610), "qstick")/5*4
    # stinger
    if f("ustinger"):
        return d(14580)/T*g(r(10))*(5+dup)
    if f("stinger"):
        return d(43740)/T*g(r(10))*(5+dup)
    if f("qstinger"):
        return d(131220)/T*g(r(10))*(5+dup)
    # stinger(blood)
    if f("ustinger(blood)"):
        return d(14580)/T*g(r(7.5))*(5+dup)
    if f("stinger(blood)"):
        return d(43740)/T*g(r(7.5))*(5+dup)
    if f("qstinger(blood)"):
        return d(131220)/T*g(r(7.5))*(5+dup)
    # stinger(magic)
    # tomato
    if f("utomato_0"):
        return d(3645, h(7290))/T*g(r(2.5, h(7290)))
    if f("utomato") or f("utomato_1"):
        return d(51030, h(7290))/T*g((r(2.5, h(7290))+1))
    if f("tomato_0"):
        return d(10935, h(21870))/T*g(r(2.5, h(21870)))
    if f("tomato") or f("tomato_1"):
        return d(153090, h(21870))/T*g((r(2.5, h(21870))+1))
    if f("qtomato_0"):
        return d(32805, h(65610))/T*g(r(2.5, h(65610)))
    if f("qtomato") or f("qtomato_1"):
        return d(459270, h(65610))/T*g((r(2.5, h(65610))+1))
    # triangle
    if f("utriangle"):
        return d(3645+2916*(utri-1), h(7290))/T*g(r(2.0, h(7290)))
    if f("triangle"):
        return d(10935+8748*(tri-1), h(21870))/T*g(r(2.0, h(21870)))
    if f("qtriangle"):
        return d(32805+26244*tri, h(65610))/T*g(r(2.0, h(65610)))
    # uranium
    if f("uuranium"):
        return 36450*poison
    if f("uranium"):
        return 109350*poison
    if f("quranium"):
        return 328050*poison
    # web(electric)
    if f("uweb(electric)"):
        return 3645
    if f("web(electric)"):
        return 10935
    if f("qweb(electric)"):
        return 32805
    # wing
    if f("uwing"):
        return d(14580, h(7290))/T*g(r(3, h(7290)))
    if f("wing"):
        return d(43740, h(21870))/T*g(r(3, h(21870)))
    if f("qwing"):
        return d(131220, h(65610))/T*g(r(3, h(65610)))
    # yucca
    if f("uyucca"):
        return d(3645, h(7290))/T*g(r(2.5, h(7290)))
    if f("yucca"):
        return d(10935, h(21870))/T*g(r(2.5, h(21870)))
    if f("qyucca"):
        return d(32805, h(65610))/T*g(r(2.5, h(65610)))
    return 0


def analyze(build, talent, x=21870.0, y=583.2, mode="lentil", lentildis=0.0, rotspeed=1.0, angle=138.0):
    global petalhealth, reload, summoner, luck, poison, dup, rot, tp, T, ed, ea, dis, udl, dl, qdl, ph_bonus, ugl, gl, qgl, utri, tri
    if mode in ["lentil", "yy"]:
        angle = 360
    build = build.split()
    if len(build) > 20:
        build = build[:20]
    while True:
        flag = True
        for i in range(len(build)):
            petal = build[i]
            if not petal:
                continue
            if petal[0] in "0123456789":
                flag = False
                times = ""
                for j in petal:
                    if j in "0123456789":
                        times += j
                    else:
                        break
                build.remove(petal)
                for j in range(min(100, int(times))):
                    build.insert(i, petal[len(times):])
                break
        if flag:
            break
    talent = talent.split()
    tp = 45
    try:
        petalhealth = ph_buff[talent[0]]
        tp += ph_tp[talent[0]]
        reload = reload_buff[talent[1]]
        tp += reload_tp[talent[1]]
        summoner = summoner_buff[talent[2]]
        tp += summoner_tp[talent[2]]
        luck = luck_buff[talent[3]]
        tp += luck_tp[talent[3]]
        poison = poison_buff[talent[4]]*cpoison_buff[talent[5]]
        tp += poison_tp[talent[4]]
        tp += cpoison_tp[talent[5]]
        dup = dup_buff[talent[6]]
        tp += dup_tp[talent[6]]
        rot = 2.5
        if len(talent) >= 8:
            rot += rot_buff[talent[7]]
            tp += rot_tp[talent[7]]
        if len(talent) >= 9:
            tp += reach_tp[talent[8]]
        if len(talent) >= 10:
            tp += health_tp[talent[9]]
    except IndexError:
        print("输入有误（talent长度不够）！")
        return
    except KeyError:
        print("输入有误（talent内容错误）！")
        return
    if dup == 3:
        build.insert(0, build[0])
        dup = 2
    ed = x
    ea = y
    dis = lentildis
    ea -= (build.count("ubur")+build.count("ubur_"))*1093.5
    ea -= (build.count("bur")+build.count("bur_"))*3280.5
    ea -= (build.count("qbur")+build.count("qbur_"))*9841.5
    luck += (build.count("uclover")+build.count("uclover_"))*0.7
    luck += (build.count("clover")+build.count("clover_"))*0.8
    luck += (build.count("qclover")+build.count("qclover_"))*0.9
    rot += (build.count("ufaster")+build.count("ufaster_"))*1.7
    rot += (build.count("faster")+build.count("faster_"))*1.9
    rot += (build.count("qfaster")+build.count("qfaster_"))*2.1
    rot_tmp = rot
    rot *= 0.3+rotspeed*0.7
    T = 2*pi/rot
    udl = build.count("udl")+build.count("udl_")
    dl = build.count("dl")+build.count("dl_")
    qdl = build.count("qdl")+build.count("qdl_")
    ugl = build.count("ugl")+build.count("ugl_")
    gl = build.count("gl")+build.count("gl_")
    qgl = build.count("qgl")+build.count("qgl_")
    ph_bonus = petalhealth+udl*0.3+dl*0.45+qdl*0.6
    utri = build.count("utriangle")+build.count("utriangle_")
    tri = build.count("triangle")+build.count("triangle_")
    dps = []
    if mode in ["lentil", "yy"]:
        for petal in build:
            dps.append(round(cal(petal)))
    elif mode == "wheel":
        for petal in build:
            dps.append(round(calw(petal, angle)))
    maxn = len(str(sum(dps)))
    for petal in build:
        maxn = max(maxn, len(petal))
    print("==============================")
    if mode == "wheel":
        print(f"Rotation Speed: {rot_tmp}*(0.3+0.7*{rotspeed})={rot:.3f}\nPeriod(T): {(2*pi/rot):.3f}s")
    print(f"TP Cost: {tp}TP/lv{lvl(tp)}")
    print(f"Build: ", end="")
    for petal in build:
        print(petal.center(maxn), end="|")
    print("|"+"TOTAL".center(maxn))
    print("  DPS: ", end="")
    for petal_dps in dps:
        print(str(petal_dps).center(maxn), end="|")
    print("|"+str(sum(dps)).center(maxn))


def main_interaction():
    analyze("sawblade 6ugl_", "M Et - - - - S - R C", 21870, 583.2, "yy")
    analyze("2chip bur_ 6ugl_", "- Et - - - - S - R M", 21870, 583.2, "yy")
    analyze("2ugl 4dust bur 2ulentil", "- Et - - - - S - R M", 21870, 583.2, "lentil", lentildis=0)
    analyze("2ugl 4dust bur 2ulentil", "- Et - - - - S - R M", 21870, 583.2, "lentil", lentildis=112)
    analyze("faster 9triangle", "Et U - - - - - L S M", 7290, 583.2, "wheel", rotspeed=1, angle=138)
    analyze("faster sawblade sawblade bean_1 bone corn leaf rock", "Et U - - - - - L S M", 7290, 583.2, "wheel", rotspeed=1, angle=138)

    print("\n\n\n请关注原作者：Hu0_gu0_4u31（florr：Huo_guo_tu31）\n\n\n")

    while True:
        try:
            build1 = input("输入构筑（例：2ugl_ 4dust bur 2ulentil）：")
            talent1 = input("输入天赋（例：M Et - - - - S，表示mph treload sdup）：")
            x1 = float(input("输入生物体伤（例：21870）："))
            y1 = float(input("输入生物护甲（例：583.2）："))
            mode1 = input("输入模式（lentil/wheel/yy）：")
            if mode1 in ["lentil", "yy"]:
                lentildis1 = max(0.0, float(input("输入lentil距离（例：112，不计算距离衰减则写0）")))
                print(f"analyze(\"{build1}\", \"{talent1}\", {x1}, {y1}, {mode1}, lentildis={lentildis1})")
                analyze(build1, talent1, x1, y1, mode1, lentildis=lentildis1)
            else:
                mode1 = "wheel"
                rotspeed1 = max(0.0, min(1.0, float(input("输入转速指令值（例：0.95，满转速则写1）"))))
                angle1 = max(0.0, min(360.0, float(input("输入攻击范围角（例：180，推荐138）"))))
                print(f"analyze(\"{build1}\", \"{talent1}\", {x1}, {y1}, {mode1}, rotspeed={rotspeed1}), angle={angle1}")
                analyze(build1, talent1, x1, y1, mode1, rotspeed=rotspeed1, angle=angle1)
        except ValueError:
            print("输入有误（体伤/护甲/距离/指令值不合法）！")
            continue


# main_interaction()


def analyze_for_web(build, talent, x, y, mode, lentildis=0.0, rotspeed=1.0, angle=138.0):
    """供网页端调用的函数，拦截 print 输出并解析为 JSON"""
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    try:
        analyze(build, talent, x, y, mode, lentildis=lentildis, rotspeed=rotspeed, angle=angle)
        output = buffer.getvalue()
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        sys.stdout = old_stdout

    lines = output.strip().split('\n')
    build_line = ""
    dps_line = ""
    wheel_info = []
    tp_info = ""  # 用于提取 TP Cost

    for line in lines:
        if "Rotation Speed:" in line or "Period(T):" in line:
            wheel_info.append(line)
        elif line.startswith("Build:"):
            build_line = line
        elif line.startswith("  DPS:"):
            dps_line = line
        elif line.startswith("TP Cost:"):
            tp_info = line  # <--- 提取这一行

    if not build_line or not dps_line:
        return json.dumps({"error": "解析输出失败，未找到 Build 或 DPS 行", "raw": output})

    builds_raw = [s.strip() for s in build_line.split("|")]
    dps_raw = [s.strip() for s in dps_line.split("|")]

    if builds_raw and builds_raw[0].startswith("Build:"):
        builds_raw[0] = builds_raw[0].replace("Build:", "").strip()
    if dps_raw and dps_raw[0].startswith("DPS:"):
        dps_raw[0] = dps_raw[0].replace("DPS:", "").strip()

    builds = [b for b in builds_raw if b]
    dps_vals = [d for d in dps_raw if d]

    total = "0"
    if dps_vals:
        total = dps_vals.pop()
    if builds and builds[-1] == "TOTAL":
        builds.pop()

    return json.dumps({
        "builds": builds,
        "dps": dps_vals,
        "total": total,
        "wheel_info": wheel_info,
        "tp_info": tp_info  # <--- 返回给网页
    })


"""
用法：
1. 在上方输入花瓣构筑、通过下拉框配置天赋、填写生物体伤与生物护甲、选择模式，点击“计算 DPS”即可在下方表格输出各花瓣 DPS 以及总 DPS。
2. 右侧的“TP cost/lvl req”显示框会实时计算并展示当前所选天赋的 TP 消耗及对应等级。
3. 花瓣、天赋、生物体伤、生物护甲为必填项；模式可通过下拉框选择 "lentil"、"yy" 或 "wheel"，默认为 "lentil"。
 - 模式为 "lentil" 或 "yy" 时，需在“lentil 距离”输入框填写数值（比如填 112 表示 2ulentil 距离；若想得到完全紧贴的理论 dps 可填默认值 0）。
 - 模式为 "wheel" 时，需在“转速指令值”输入框填写/rot-speed转速指令（比如 0.95；默认值为 1），以及在“攻击范围角”输入框填写攻击范围角（即花瓣刚好攻击位置与刚好不攻击位置的相位差，默认值为138°）。
花瓣：
1. 各花瓣名用空格隔开，s 不标等级，其它要标等级（例：usawblade、pearl、qcoin）。
2. 花瓣前可加数字表示多个同一花瓣（例：2bone、3claw）。
3. 目前支持的花瓣：所有 u/s/q 等级的一帧十判花瓣（部分魔法花瓣除外）、部分非一帧十判花瓣。
4. 花瓣名的特殊情况：
 (1) 缩写：ant egg -> agg；beetle egg -> bgg；golden leaf -> gl。
 (2) 不含 (1) 的情况中，图标显示花瓣名与真实花瓣名不同时，采用图标显示花瓣名，如 cogwheel 应写为 cog。
 (3) (2) 的情况中，若多个花瓣图标显示花瓣名重复，则将真实花瓣名中的形容词加上 () 括号提到图标花瓣名之后，如 magic leaf 应写为 leaf(magic)。
 (4) 如果同一花瓣不同情况下有不同 dps，则在花瓣名后加上 _+数字 加以区分，不加则为默认，具体如下：
  - bean_0：周围有人；1：周围没人；默认为 0
  - broccoli_0：中0发；1~3：以此类推；默认为 0
  - carrot_0：不发射（伤害-80%）；1：发射（额外时间0.5s）；默认为 1
  - claw_0：无额外伤害；1：有额外伤害；默认为 1
  - clay_0：最低伤害；1：最高伤害（无额外时间）；默认为 1
  - grapes_0：不发射（1发，无额外时间）；1：中1发（额外时间0.5s）；2~6：以此类推；默认为 0
  - laser_0：本体伤害；1：电伤害；默认为 1
  - missile：同 carrot
  - missile(mecha)：同 carrot
  - pearl_0：不发射（无额外时间）；1：发射（额外时间0.5s）；默认为 0
  - peas：同 grapes
  - pollen_0：不发射（无额外时间）；1：发射（额外时间0.5s）；默认为 1
  - privet_xx：xx 表示 privet 对应毒 dps 花瓣缩写，ugrapes 为 ug，siris 为 i，qpincer 为 qp，以此类推
  - tomato_0：最低伤害；1：最高伤害（额外时间1s）
5. 如果花瓣不计入 dps（bur、dl、gl 等）但仍发挥其效果，在后面加上单个下划线 _ （例：ugl_）。            

天赋：
1. 天赋顺序分别为：ph(petal health)、reload、summon、luck、poison、cpoison(concentrated poison)、dup(duplicator)、rot(rotation speed)、reach、health/sc(second chance)。
2. ph 至 luck、dup 至 reach 天赋：用等级表示，不点为 -，Common 为 C，以此类推，其中 Unusual-Un，Ultra-U，Epic-E，Eternal-Et。
3. poison 天赋：用层数表示，不点为 -，点一层为 1，点满为 9。
4. cpoison 天赋：不点为 -，点为 1。
5. health/sc 天赋：用等级表示，Common Health 为 C（Un、R 同理），Rare Health+Legendary Second Chance 为 L（M 同理）。
"""

"""
版本：v2.0.0 | 更新于 2026.11.12
原作者：Hu0_gu0_4u31（florr：Huo_guo_tu31）

更新日志
v2.0.0 (2026.11.12)
- 网页版本发布
- 新增了实时 TP 计算和等级显示
- 新增了攻击范围角（Angle）计算
- 重构了界面，支持响应式布局
- 修复已知问题

v1.0.0 (2026.10.24)
- 初始Python终端版本发布
"""
