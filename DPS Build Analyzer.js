// 全局变量
let petalhealth, reload, summoner, luck, poison, dup, rot, tp, T, ed, ea, dis, udl, dl, qdl, ugl, gl, qgl, poisond, utri, tri;

const ph_buff = {"-": 1, "C": 1.15, "Un": 1.15**2, "R": 1.15**3, "E": 1.15**4, "L": 1.15**5, "M": 1.15**6, "U": 1.15**7, "S": 1.15**8, "Et": 1.15**10};
const ph_tp = {"-": 0, "C": 2, "Un": 6, "R": 12, "E": 20, "L": 30, "M": 42, "U": 56, "S": 72, "Et": 90};
const reload_buff = {"-": 1, "C": 0.9, "Un": 0.9**2, "R": 0.9**3, "E": 0.9**4, "L": 0.9**4*0.8, "M": 0.9**4*0.8**2, "U": 0.9**4*0.8**3, "S": 0.9**4*0.8**4, "Et": 0.9**4*0.8**4*0.7};
const reload_tp = {"-": 0, "C": 2, "Un": 8, "R": 18, "E": 30, "L": 46, "M": 66, "U": 90, "S": 118, "Et": 150};
const summoner_buff = {"-": 1, "C": 1.15, "Un": 1.15**2, "R": 1.15**3, "E": 1.15**4, "L": 1.15**5, "M": 1.15**6, "U": 1.15**7, "S": 1.15**8, "Et": 1.15**10};
const summoner_tp = {"-": 0, "C": 2, "Un": 7, "R": 15, "E": 26, "L": 40, "M": 57, "U": 77, "S": 100, "Et": 126};
const luck_buff = {"-": 0, "C": 0.1, "Un": 0.25, "R": 0.45, "E": 0.7, "L": 1, "M": 1.35, "U": 1.75, "S": 2.2, "Et": 2.7};
const luck_tp = {"-": 0, "C": 2, "Un": 5, "R": 9, "E": 14, "L": 20, "M": 27, "U": 35, "S": 44, "Et": 54};
const poison_buff = {"-": 1, "1": 1.0625, "2": 1.125, "3": 1.1875, "4": 1.25, "5": 1.3125, "6": 1.375, "7": 1.4375, "8": 1.5, "9": 1.5625};
const poison_tp = {"-": 0, "1": 1, "2": 3, "3": 6, "4": 9, "5": 12, "6": 15, "7": 18, "8": 21, "9": 24};
const cpoison_buff = {"-": 1, "1": 1.2};
const cpoison_tp = {"-": 0, "1": 15};
const dup_buff = {"-": 0, "L": 1, "U": 2, "S": 3, "Et": 3};
const dup_tp = {"-": 0, "L": 10, "U": 30, "S": 60, "Et": 100};
const rot_buff = {"-": 0, "C": 0.6, "Un": 1.2, "R": 1.8, "E": 2.4, "L": 3};
const rot_tp = {"-": 0, "C": 1, "Un": 3, "R": 6, "E": 10, "L": 15};
const reach_tp = {"-": 0, "R": 3, "M": 9, "S": 18};
const health_tp = {"-": 0, "C": 2, "Un": 7, "R": 15, "L": 25, "M": 45};

function rnd(x) { return Math.max(x, 0.05); }

function lvl(x) {
    for (let lv = 1; lv < 999; lv++) {
        let t = Math.floor(lv / 10) * 20;
        if (lv % 10 <= 4) t += lv % 10 - 1;
        else t += lv % 10;
        if (t >= x) return lv;
    }
    return 999;
}

function d(pd, ph = 1, typ = "") {
    let res = 0;
    let m = ph;
    if (typ === "ubattery" || typ === "ulightning") return pd * 8;
    if (typ === "battery" || typ === "lightning") return pd * 9;
    if (typ === "qbattery" || typ === "qlightning") return pd * 10;
    if (typ === "ubone") {
        let pa = 7290;
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea);
            m -= Math.max(0, ed - pa);
            pa /= 2;
        }
        return res;
    }
    if (typ === "bone") {
        let pa = 21870;
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea);
            m -= Math.max(0, ed - pa);
            pa /= 2;
        }
        return res;
    }
    if (typ === "qbone") {
        let pa = 65610;
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea);
            m -= Math.max(0, ed - pa);
            pa /= 2;
        }
        return res;
    }
    if (typ === "uclaw") {
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea + 72900);
            m -= ed;
        }
        return res;
    }
    if (typ === "claw") {
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea + 218700);
            m -= ed;
        }
        return res;
    }
    if (typ === "qclaw") {
        while (m > 0) {
            res += Math.max(0, pd * m / ph - ea + 656100);
            m -= ed;
        }
        return res;
    }
    if (["ubgg", "bgg", "qbgg", "uagg", "agg", "qagg", "ustick", "stick", "qstick"].includes(typ)) {
        return Math.max(0, pd - ea) * Math.ceil(ph / ed);
    }
    if (typ === "qmjolnir") {
        while (m > 0) {
            res += Math.max(0, pd * m / ph);
            m -= ed;
        }
        return res;
    }
    while (m > 0) {
        res += Math.max(0, pd * m / ph - ea);
        m -= ed;
    }
    return res;
}

function h(ph) { return ph * (petalhealth + 0.3 * udl + 0.45 * dl + 0.6 * qdl); }
function mh(ph) { return ph * summoner; }
function fx(x) { return x <= 13 ? 0 : 0.0003664 * (x - 13.06); }
function r(rel, ph = 1) {
    let res = rnd(rel * reload * (0.825 ** ugl) * (0.8 ** gl) * (0.775 ** qgl) * (1.05 ** (udl + dl + qdl)));
    res += Math.floor(Math.ceil(ph / ed) / 10) * (1 / 25);
    res += fx(dis);
    return res;
}
function mr(rel, ph = 1) {
    let res = rnd(rel * reload * (0.825 ** ugl) * (0.8 ** gl) * (0.775 ** qgl) * (1.05 ** (udl + dl + qdl)));
    res += Math.ceil(ph / ed) * (1 / 25);
    res += fx(dis);
    return res;
}
function hr(rel, ph = 1) {
    let res = rnd(rel * reload * (0.825 ** ugl) * (0.8 ** gl) * (0.775 ** qgl) * (1.05 ** (udl + dl + qdl)));
    res += Math.ceil(ph / ed) * (1 / 25);
    res += fx(dis);
    return res;
}

function cal(petal) {
    const f = (name) => petal === name || petal === 's' + name;
    const t = () => parseInt(petal.slice(-1));
    if (!petal) return 0;

    if (f("ubasic") || f("uclover") || f("usalt") || f("usoil") || f("utalisman") || f("uyinyang")) return d(7290, h(7290))/r(2.5, h(7290));
    if (f("basic") || f("clover") || f("salt") || f("soil") || f("talisman") || f("yinyang")) return d(21870, h(21870))/r(2.5, h(21870));
    if (f("qbasic") || f("qclover") || f("qsalt") || f("qsoil") || f("qtalisman") || f("qyinyang") || f("tbasic")) return d(65610, h(65610))/r(2.5, h(65610));

    if (f("ubattery")) return d(26244, h(1), "ubattery") / (r(2.5) + 0.1);
    if (f("battery")) return d(78732, h(1), "battery") / (r(2.5) + 0.1);
    if (f("qbattery")) return d(236196, h(1), "qbattery") / (r(2.5) + 0.1);

    if (f("ubean") || f("ubean_0")) return d(14580, h(8748))/r(2, h(8748));
    if (f("ubean_1")) return d(21870, h(8748))/r(2, h(8748));
    if (f("bean") || f("bean_0")) return d(43740, h(26244))/r(2, h(26244));
    if (f("bean_1")) return d(65610, h(26244))/r(2, h(26244));
    if (f("qbean") || f("qbean_0")) return d(131220, h(78732))/r(2, h(78732));
    if (f("qbean_1")) return d(196830, h(78732))/r(2, h(78732));

    if (f("ubone")) return d(10206, h(7290), "ubone")/r(2.5, h(7290)+14580);
    if (f("bone")) return d(30618, h(21870), "bone")/r(2.5, h(21870)+43740);
    if (f("qbone")) return d(91854, h(65610), "qbone")/r(2.5, h(65610)+131220);

    if (f("ubroccoli") || f("ubroccoli_0")) return d(10935, h(7290))/r(2.8, h(7290));
    if (f("ubroccoli_1") || f("ubroccoli_2") || f("ubroccoli_3")) return (d(10935, h(7290))+d(3645, h(2430)))/r(2.8, h(7290))*t();
    if (f("broccoli") || f("broccoli_0")) return d(32805, h(21870))/r(2.8, h(21870));
    if (f("broccoli_1") || f("broccoli_2") || f("broccoli_3")) return (d(32805, h(21870))+d(10935, h(7290)))/r(2.8, h(21870))*t();
    if (f("qbroccoli") || f("qbroccoli_0")) return d(98415, h(65610))/r(2.8, h(65610));
    if (f("qbroccoli_1") || f("qbroccoli_2") || f("qbroccoli_3")) return (d(98415, h(65610))+d(32805, h(21870)))/r(2.8, h(65610))*t();

    if (f("ubur")) return d(3645, h(3645))/r(2, h(3645));
    if (f("bur")) return d(10935, h(10935))/r(2, h(10935));
    if (f("qbur")) return d(32805, h(32805))/r(2, h(32805));

    if (f("ucactus") || f("ucactus_magic")) return d(5103, h(10935))/r(1, h(10935));
    if (f("cactus") || f("cactus_magic")) return d(15309, h(32805))/r(1, h(32805));
    if (f("qcactus") || f("qcactus_magic")) return d(45927, h(98415))/r(1, h(98415));

    if (f("ucard")) return (d(3645, h(21870))/r(2.5, h(21870)) + d(7290, h(18225))/r(2.5, h(18225)) + d(10935, h(14580))/r(2.5, h(14580)) + d(14580, h(10935))/r(2.5, h(10935))) / 4;
    if (f("card")) return (d(10935, h(65610))/r(2.5, h(65610)) + d(21870, h(54675))/r(2.5, h(54675)) + d(32805, h(43740))/r(2.5, h(43740)) + d(43740, h(32805))/r(2.5, h(32805))) / 4;
    if (f("qcard")) return (d(32805, h(196830))/r(2.5, h(196830)) + d(65610, h(164025))/r(2.5, h(164025)) + d(98415, h(131220))/r(2.5, h(131220)) + d(131220, h(98415))/r(2.5, h(98415))) / 4;

    if (f("ucarrot_0")) return d(13122/5, h(13122))/r(1, h(13122));
    if (f("carrot_0")) return d(39366/5, h(39366))/r(1, h(39366));
    if (f("qcarrot_0")) return d(118098/5, h(118098))/r(1, h(118098));
    if (f("ucarrot") || f("ucarrot_1")) return d(13122, h(13122))/(r(1, h(13122))+0.5);
    if (f("carrot") || f("carrot_1")) return d(39366, h(39366))/(r(1, h(39366))+0.5);
    if (f("qcarrot") || f("carrot_1")) return d(118098, h(118098))/(r(1, h(118098))+0.5);

    if (f("uchip")) return d(5103, h(2187))*10/(r(2.5, h(729))+0.9**10/(1-0.9**10)*0.04);
    if (f("chip")) return d(15309, h(2187))*10/(r(2.5, h(2187))+0.9**10/(1-0.9**10)*0.04);
    if (f("qchip")) return d(45927, h(2187))*10/(r(2.5, h(6561))+0.9**10/(1-0.9**10)*0.04);

    if (f("uclaw_0")) return d(3645, h(7290))/r(3.5, h(7290));
    if (f("uclaw") || f("uclaw_1")) return d(3645, h(7290), "uclaw")/r(3.5, h(7290));
    if (f("claw_0")) return d(10935, h(21870))/r(3.5, h(21870));
    if (f("claw") || f("claw_1")) return d(10935, h(21870), "claw")/r(3.5, h(21870));
    if (f("qclaw_0")) return d(32805, h(65610))/r(3.5, h(65610));
    if (f("qclaw") || f("qclaw_1")) return d(32805, h(65610), "qclaw")/r(3.5, h(65610));

    if (f("uclay") || f("uclay_0")) return d(3645, h(7290))/r(2, h(7290));
    if (f("uclay_1")) return d(72900, h(7290))/r(2, h(7290));
    if (f("clay") || f("clay_0")) return d(10935, h(21870))/r(2, h(21870));
    if (f("clay_1")) return d(218700, h(21870))/r(2, h(21870));
    if (f("qclay") || f("qclay_0")) return d(32805, h(65610))/r(2, h(65610));
    if (f("qclay_1")) return d(656100, h(65610))/r(2, h(65610));

    if (f("ucog")) return d(13851, h(9477))/r(2.5, h(9477));
    if (f("cog")) return d(41553, h(28431))/r(2.5, h(28431));
    if (f("qcog")) return d(124659, h(85293))/r(2.5, h(85293));

    if (f("ucoin")) return d(10935, h(7290))/r(2.5, h(7290));
    if (f("coin")) return d(32805, h(21870))/r(2.5, h(21870));
    if (f("qcoin")) return d(98415, h(65610))/r(2.5, h(65610));

    if (f("ucoral")) return d(8019*3/7)/(r(1.5)+0.08)*7;
    if (f("coral")) return d(24057*3/7)/(r(1.5)+0.08)*7;
    if (f("qcoral")) return d(72171*3/7)/(r(1.5)+0.08)*7;

    if (f("ucorn")) return d(5832, h(145800))/r(7, h(145800));
    if (f("corn")) return d(17496, h(437400))/r(7, h(437400));
    if (f("qcorn")) return d(52488, h(1312200))/r(7, h(1312200));

    if (f("udandelion")) return d(1944, h(1944))/r(1, h(1944))*(3+dup);
    if (f("dandelion")) return d(5832, h(5832))/r(1, h(5832))*(3+dup);
    if (f("qdandelion")) return d(17496, h(17496))/r(1, h(17496))*(3+dup);

    if (f("udice")) return d(7290*(2.7+1.36*luck), h(7290))/r(2.5, h(7290));
    if (f("dice")) return d(21870*(2.7+1.36*luck), h(21870))/r(2.5, h(21870));
    if (f("qdice")) return d(65610*(2.7+1.36*luck), h(65610))/r(2.5, h(65610));

    if (f("udomino")) return (d(0, h(11664))*7+d(729, h(11664))+d(729*2, h(11664))+d(729*3, h(11664))+d(729*4, h(11664))*2+d(729*5, h(11664))+d(729*6, h(11664))*2+d(729*8, h(11664))+d(729*9, h(11664))+d(729*10, h(11664))+d(729*12, h(11664))*2+d(729*15, h(11664))+d(729*16, h(11664))+d(729*18, h(11664))+d(729*20, h(11664))+d(729*24, h(11664))+d(729*25, h(11664))+d(729*30, h(11664))+d(729*36, h(11664)))/28/r(1.0, h(11664));
    if (f("domino")) return (d(0, h(34992))*7+d(2187, h(34992))+d(2187*2, h(34992))+d(2187*3, h(34992))+d(2187*4, h(34992))*2+d(2187*5, h(34992))+d(2187*6, h(34992))*2+d(2187*8, h(34992))+d(2187*9, h(34992))+d(2187*10, h(34992))+d(2187*12, h(34992))*2+d(2187*15, h(34992))+d(2187*16, h(34992))+d(2187*18, h(34992))+d(2187*20, h(34992))+d(2187*24, h(34992))+d(2187*25, h(34992))+d(2187*30, h(34992))+d(2187*36, h(34992)))/28/r(1.0, h(34992));
    if (f("qdomino")) return (d(0, h(104976))*7+d(6561, h(104976))+d(6561*2, h(104976))+d(6561*3, h(104976))+d(6561*4, h(104976))*2+d(6561*5, h(104976))+d(6561*6, h(104976))*2+d(6561*8, h(104976))+d(6561*9, h(104976))+d(6561*10, h(104976))+d(6561*12, h(104976))*2+d(6561*15, h(104976))+d(6561*16, h(104976))+d(6561*18, h(104976))+d(6561*20, h(104976))+d(6561*24, h(104976))+d(6561*25, h(104976))+d(6561*30, h(104976))+d(6561*36, h(104976)))/28/r(1.0, h(104976));

    if (f("udust")) return d(3159, h(1215))/r(0.8, h(1215))*(3+dup);
    if (f("dust")) return d(9477, h(3645))/r(0.8, h(3645))*(3+dup);
    if (f("qdust")) return d(28431, h(10935))/r(0.8, h(10935))*(3+dup);

    if (f("uagg")) return d(4374, mh(182250), "uagg")/mr(60, mh(182250))*(4+dup);
    if (f("agg")) return d(13122, mh(546750), "agg")/mr(60, mh(547650))*(4+dup);
    if (f("qagg")) return d(39366, mh(1640250), "qagg")/mr(60, mh(1640250))*(4+dup);

    if (f("ubgg")) return d(5103, mh(364500), "ubgg")/mr(30, mh(1093500));
    if (f("bgg")) return d(15309, mh(1093500), "bgg")/mr(30, mh(1093500));
    if (f("qbgg")) return d(45927, mh(3280500), "qbgg")/mr(30, mh(3280500));

    if (f("ufang")) return d(10935)/r(3.5);
    if (f("fang")) return d(32805)/r(3.5);
    if (f("qfang")) return d(98415)/r(3.5);

    if (f("ufaster")) return d(8748, h(3645))/r(2.5, h(3645));
    if (f("faster")) return d(26244, h(10935))/r(2.5, h(10935));
    if (f("qfaster")) return d(78732, h(32805))/r(2.5, h(32805));

    if (f("ufragment")) return d(364.5, h(364.5))/r(10, h(364.5))*2;
    if (f("fragment")) return d(729, h(729))/r(10, h(729))*3;
    if (f("qmjolnir") || f("qmjölnir")) return d(328050, h(328050), "qmjolnir")/r(8, h(328050));

    if (f("uglass")) return d(16038);
    if (f("glass")) return d(48114);
    if (f("qglass")) return d(144342);

    if (f("ugrapes") || f("ugrapes_0")) return d(2187, h(3645))/r(1.5, h(3645));
    if (f("ugrapes_1") || f("ugrapes_2") || f("ugrapes_3") || f("ugrapes_4") || f("ugrapes_5") || f("ugrapes_6")) return d(2187, h(3645))/r(1.5, h(3645)+0.5)*t();
    if (f("grapes") || f("grapes_0")) return d(6561, h(10935))/r(1.5, h(10935));
    if (f("grapes_1") || f("grapes_2") || f("grapes_3") || f("grapes_4") || f("grapes_5") || f("grapes_6")) return d(6561, h(10935))/r(1.5, h(10935)+0.5)*t();
    if (f("qgrapes") || f("qgrapes_0")) return d(19683, h(32805))/r(1.5, h(32805));
    if (f("qgrapes_1") || f("qgrapes_2") || f("qgrapes_3") || f("qgrapes_4") || f("qgrapes_5") || f("qgrapes_6")) return d(19683, h(32805))/r(1.5, h(32805)+0.5)*t();

    if (f("uheavy")) return d(9477, h(109350))/r(10, h(109350));
    if (f("heavy")) return d(28431, h(328050))/r(10, h(328050));
    if (f("qheavy")) return d(85293, h(984150))/r(10, h(984150));

    if (f("uiris")) return d(3645, h(3645))/r(4, h(3645));
    if (f("iris")) return d(10935, h(10935))/r(4, h(10935));
    if (f("qiris")) return d(32805, h(32805))/r(4, h(32805));

    if (f("ujelly")) return d(7290, h(7290))/hr(10, h(7290));
    if (f("jelly")) return d(21870, h(21870))/hr(10, h(21870));
    if (f("qjelly")) return d(65610, h(65610))/hr(10, h(65610));

    if (f("ulaser_0")) return d(3645, h(7290))/hr(5, h(7290));
    if (f("ulaser") || f("ulaser_1")) return 36450;
    if (f("laser_0")) return d(10935, h(21870))/hr(5, h(21870));
    if (f("laser") || f("laser_1")) return 109350;
    if (f("qlaser_0")) return d(32805, h(65610))/hr(5, h(65610));
    if (f("qlaser") || f("qlaser_1")) return 328050;

    if (f("uleaf") || f("uleaf(magic)")) return d(11664, h(8748))/r(1.8, h(8748));
    if (f("leaf") || f("leaf(magic)")) return d(34992, h(26244))/r(1.8, h(26244));
    if (f("qleaf") || f("qleaf(magic)")) return d(104976, h(78732))/r(1.8, h(78732));

    if (f("udl") || f("uleaf(dead)")) return d(11664, h(8748))/r(1.8/1.05, h(8748/petalhealth*(petalhealth-0.3)));
    if (f("dl") || f("leaf(dead)")) return d(34992, h(26244))/r(1.8/1.05, h(26244/petalhealth*(petalhealth-0.45)));
    if (f("qdl") || f("qleaf(dead)")) return d(104976, h(78732))/r(1.8/1.05, h(78732/petalhealth*(petalhealth-0.6)));

    if (f("ugl") || f("uleaf(golden)")) return d(11664, h(8748))/r(2.5/0.825, h(8748));
    if (f("gl") || f("leaf(golden)")) return d(34992, h(26244))/r(2.5/0.8, h(26244));
    if (f("qgl") || f("qleaf(golden)")) return d(104976, h(78732))/r(2.5/0.775, h(78732));

    if (f("ulentil")) return d(9477, h(8748))/r(2, h(8748));
    if (f("lentil")) return d(28431, h(26244))/r(2, h(26244));
    if (f("qlentil")) return d(85293, h(78732))/r(2, h(78732));

    if (f("ulight")) return d(1895.4, h(729))/r(0.8, h(729))*(5+dup);
    if (f("light")) return d(5686.2, h(2187))/r(0.8, h(2187))*(5+dup);
    if (f("qlight")) return d(17058.6, h(6561))/r(0.8, h(6561))*(5+dup);

    if (f("ulightning")) return d(8748, h(14580), "ulightning")/r(2.5);
    if (f("lightning")) return d(26244, h(43740), "lightning")/r(2.5);
    if (f("qlightning")) return d(78732, h(131220), "qlightning")/r(2.5);

    if (f("umissile_0") || f("umissile(mecha)_0")) return d(25515/5, h(1458))/r(1.5, h(1458));
    if (f("umissile") || f("umissile_1") || f("umissile(mecha)") || f("umissile(mecha)_1")) return d(25515, h(1458))/(r(1.5, h(1458))+0.5);
    if (f("missile_0") || f("missile(mecha)_0")) return d(76545/5, h(4374))/r(1.5, h(4374));
    if (f("missile") || f("missile_1") || f("missile(mecha)") || f("missile(mecha)_1")) return d(76545, h(4374))/(r(1.5, h(4374))+0.5);
    if (f("qmissile_0") || f("qmissile(mecha)_0")) return d(229635/5, h(13122))/r(1.5, h(13122));
    if (f("qmissile") || f("qmissile_1") || f("qmissile(mecha)") || f("qmissile(mecha)_1")) return d(229635, h(13122))/(r(1.5, h(13122))+0.5);

    if (f("uorange")) return d(5832, h(4860))/r(3.5, h(4860))*(3+dup);
    if (f("orange")) return d(17496, h(14580))/r(3.5, h(14580))*(3+dup);
    if (f("qorange")) return d(52488, h(43740))/r(3.5, h(43740))*(3+dup);

    if (f("upearl") || f("upearl_0")) return d(14580, h(36450))/r(4, h(36450));
    if (f("upearl_1")) return d(14580, h(36450))/(r(4, h(36450))+0.5);
    if (f("pearl") || f("pearl_0")) return d(43740, h(109350))/r(4, h(109350));
    if (f("pearl_1")) return d(43740, h(109350))/(r(4, h(109350))+0.5);
    if (f("qpearl") || f("qpearl_0")) return d(131220, h(328050))/r(4, h(328050));
    if (f("qpearl_1")) return d(131220, h(328050))/(r(4, h(328050))+0.5);

    if (f("upeas") || f("upeas_0")) return d(10935, h(3645))/r(1.5, h(3645));
    if (f("upeas_1") || f("upeas_2") || f("upeas_3") || f("upeas_4") || f("upeas_5") || f("upeas_6")) return d(10935, h(3645))/(r(1.5, h(3645))+0.5)*t();
    if (f("peas") || f("peas_0")) return d(32805, h(10935))/r(1.5, h(10935));
    if (f("peas_1") || f("peas_2") || f("peas_3") || f("peas_4") || f("peas_5") || f("peas_6")) return d(32805, h(10935))/(r(1.5, h(10935))+0.5)*t();
    if (f("qpeas") || f("qpeas_0")) return d(98415, h(32805))/r(1.5, h(32805));
    if (f("qpeas_1") || f("qpeas_2") || f("qpeas_3") || f("qpeas_4") || f("qpeas_5") || f("qpeas_6")) return d(98415, h(32805))/(r(1.5, h(32805))+0.5)*t();

    if (f("upincer")) return d(3645, h(3645))/r(2.5, h(3645));
    if (f("pincer")) return d(10935, h(10935))/r(2.5, h(10935));
    if (f("qpincer")) return d(32805, h(32805))/r(2.5, h(32805));

    if (f("upollen_0")) return d(9234, h(1215))/r(2, h(1215))*(3+dup);
    if (f("upollen") || f("upollen_1")) return d(9234, h(1215))/(r(2, h(1215))+0.5)*(3+dup);
    if (f("pollen_0")) return d(27702, h(3645))/r(2, h(3645))*(3+dup);
    if (f("pollen") || f("pollen_1")) return d(27702, h(3645))/(r(2, h(3645))+0.5)*(3+dup);
    if (f("qpollen_0")) return d(83106, h(10935))/r(2, h(10935))*(3+dup);
    if (f("qpollen") || f("qpollen_1")) return d(83106, h(10935))/(r(2, h(10935))+0.5)*(3+dup);

    if (f("uprivet")) return poisond*0.2/r(4*0.7**6);
    if (f("privet")) return poisond*0.2/r(4*0.7**7);
    if (f("qprivet")) return poisond*0.2/r(4*0.7**8);

    if (f("urice")) return d(2916, h(729))/r(0.05, h(729));
    if (f("rice")) return d(8748, h(2187))/r(0.05, h(2187));
    if (f("qrice")) return d(26244, h(6561))/r(0.05, h(6561));

    if (f("urock")) return d(16038, h(21870))/r(3, h(21870));
    if (f("rock")) return d(48114, h(65610))/r(3, h(65610));
    if (f("qrock")) return d(144342, h(196830))/r(3, h(196830));

    if (f("usand")) return d(3645, h(911.25))/r(1.5, h(911.25))*(4+dup);
    if (f("sand")) return d(10935, h(2733.75))/r(1.5, h(2733.75))*(4+dup);
    if (f("qsand")) return d(32805, h(8201.25))/r(1.5, h(8201.25))*(4+dup);

    if (f("usawblade")) return d(29160, h(18225))/r(2.5, h(18225));
    if (f("sawblade")) return d(87480, h(54675))/r(2.5, h(54675));
    if (f("qsawblade")) return d(262440, h(164025))/r(2.5, h(164025));

    if (f("ustarfish")) return d(3645, h(5103))/r(1.5, h(5103));
    if (f("starfish")) return d(10935, h(15309))/r(1.5, h(15309));
    if (f("qstarfish")) return d(32805, h(45927))/r(1.5, h(45927));

    if (f("ustick")) return d(65610, mh(65610), "ustick")/5*4;
    if (f("stick")) return d(65610, mh(65610), "stick")/5*4;
    if (f("qstick")) return d(65610, mh(65610), "qstick")/5*4;

    if (f("ustinger")) return d(14580)/r(10)*(5+dup);
    if (f("stinger")) return d(43740)/r(10)*(5+dup);
    if (f("qstinger")) return d(131220)/r(10)*(5+dup);

    if (f("ustinger(blood)")) return d(14580)/r(7.5)*(5+dup);
    if (f("stinger(blood)")) return d(43740)/r(7.5)*(5+dup);
    if (f("qstinger(blood)")) return d(131220)/r(7.5)*(5+dup);

    if (f("utomato_0")) return d(3645, h(7290))/r(2.5, h(7290));
    if (f("utomato") || f("utomato_1")) return d(51030, h(7290))/(r(2.5, h(7290))+1);
    if (f("tomato_0")) return d(10935, h(21870))/r(2.5, h(21870));
    if (f("tomato") || f("tomato_1")) return d(153090, h(21870))/(r(2.5, h(21870))+1);
    if (f("qtomato_0")) return d(32805, h(65610))/r(2.5, h(65610));
    if (f("qtomato") || f("qtomato_1")) return d(459270, h(65610))/(r(2.5, h(65610))+1);

    if (f("utriangle")) return d(3645+2916*(utri-1), h(7290))/r(2.0, h(7290));
    if (f("triangle")) return d(10935+8748*(tri-1), h(21870))/r(2.0, h(21870));
    if (f("qtriangle")) return d(32805+26244*tri, h(65610))/r(2.0, h(65610));

    if (f("uuranium")) return 0;
    if (f("uranium")) return 0;
    if (f("quranium")) return 0;

    if (f("uweb(electric)")) return 3645;
    if (f("web(electric)")) return 10935;
    if (f("qweb(electric)")) return 32805;

    if (f("uwing")) return d(14580, h(7290))/r(3, h(7290));
    if (f("wing")) return d(43740, h(21870))/r(3, h(21870));
    if (f("qwing")) return d(131220, h(65610))/r(3, h(65610));

    if (f("uyucca")) return d(3645, h(7290))/r(2.5, h(7290));
    if (f("yucca")) return d(10935, h(21870))/r(2.5, h(21870));
    if (f("qyucca")) return d(32805, h(65610))/r(2.5, h(65610));
    return 0;
}

function calw(petal, angle) {
    const f = (name) => petal === name || petal === 's' + name;
    const t = () => parseInt(petal.slice(-1));
    const g = (rel) => {
        let ang = angle / 360;
        let lap = Math.floor(rel / T);
        let den = rel - lap * T;
        if (den === 0) return Math.round(rel / T);
        return Math.ceil(T * ang / den) / (lap * Math.ceil(T * ang / den) + 1);
    };
    if (!petal) return 0;

    if (f("ubasic") || f("uclover") || f("usalt") || f("usoil") || f("utalisman") || f("uyinyang")) return d(7290, h(7290))/T*g(r(2.5, h(7290)));
    if (f("basic") || f("clover") || f("salt") || f("soil") || f("talisman") || f("yinyang")) return d(21870, h(21870))/T*g(r(2.5, h(21870)));
    if (f("qbasic") || f("qclover") || f("qsalt") || f("qsoil") || f("qtalisman") || f("qyinyang") || f("tbasic")) return d(65610, h(65610))/T*g(r(2.5, h(65610)));
    if (f("ubattery")) return d(26244, h(1), "ubattery") / (r(2.5) + 0.1);
    if (f("battery")) return d(78732, h(1), "battery") / (r(2.5) + 0.1);
    if (f("qbattery")) return d(236196, h(1), "qbattery") / (r(2.5) + 0.1);
    if (f("ubean") || f("ubean_0")) return d(14580, h(8748))/T*g(r(2, h(8748)));
    if (f("ubean_1")) return d(21870, h(8748))/T*g(r(2, h(8748)));
    if (f("bean") || f("bean_0")) return d(43740, h(26244))/T*g(r(2, h(26244)));
    if (f("bean_1")) return d(65610, h(26244))/T*g(r(2, h(26244)));
    if (f("qbean") || f("qbean_0")) return d(131220, h(78732))/T*g(r(2, h(78732)));
    if (f("qbean_1")) return d(196830, h(78732))/T*g(r(2, h(78732)));
    if (f("ubone")) return d(10206, h(7290), "ubone")/T*g(r(2.5, h(7290)+14580));
    if (f("bone")) return d(30618, h(21870), "bone")/T*g(r(2.5, h(21870)+43740));
    if (f("qbone")) return d(91854, h(65610), "qbone")/T*g(r(2.5, h(65610)+131220));
    if (f("ubroccoli") || f("ubroccoli_0")) return d(10935, h(7290))/T*g(r(2.8, h(7290)));
    if (f("ubroccoli_1") || f("ubroccoli_2") || f("ubroccoli_3")) return (d(10935, h(7290))+d(3645, h(2430)))/T*g(r(2.8, h(7290)))*t();
    if (f("broccoli") || f("broccoli_0")) return d(32805, h(21870))/T*g(r(2.8, h(21870)));
    if (f("broccoli_1") || f("broccoli_2") || f("broccoli_3")) return (d(32805, h(21870))+d(10935, h(7290)))/T*g(r(2.8, h(21870)))*t();
    if (f("qbroccoli") || f("qbroccoli_0")) return d(98415, h(65610))/T*g(r(2.8, h(65610)));
    if (f("qbroccoli_1") || f("qbroccoli_2") || f("qbroccoli_3")) return (d(98415, h(65610))+d(32805, h(21870)))/T*g(r(2.8, h(65610)))*t();
    if (f("ubur")) return d(3645, h(3645))/T*g(r(2, h(3645)));
    if (f("bur")) return d(10935, h(10935))/T*g(r(2, h(10935)));
    if (f("qbur")) return d(32805, h(32805))/T*g(r(2, h(32805)));
    if (f("ucactus") || f("ucactus_magic")) return d(5103, h(10935))/T*g(r(1, h(10935)));
    if (f("cactus") || f("cactus_magic")) return d(15309, h(32805))/T*g(r(1, h(32805)));
    if (f("qcactus") || f("qcactus_magic")) return d(45927, h(98415))/T*g(r(1, h(98415)));
    if (f("ucard")) return (d(3645, h(21870))/r(2.5, h(21870)) + d(7290, h(18225))/r(2.5, h(18225)) + d(10935, h(14580))/r(2.5, h(14580)) + d(14580, h(10935))/T*g(r(2.5, h(10935)))) / 4;
    if (f("card")) return (d(10935, h(65610))/r(2.5, h(65610)) + d(21870, h(54675))/r(2.5, h(54675)) + d(32805, h(43740))/r(2.5, h(43740)) + d(43740, h(32805))/T*g(r(2.5, h(32805)))) / 4;
    if (f("qcard")) return (d(32805, h(196830))/r(2.5, h(196830)) + d(65610, h(164025))/r(2.5, h(164025)) + d(98415, h(131220))/r(2.5, h(131220)) + d(131220, h(98415))/T*g(r(2.5, h(98415)))) / 4;
    if (f("ucarrot_0")) return d(13122/5, h(13122))/T*g(r(1, h(13122)));
    if (f("carrot_0")) return d(39366/5, h(39366))/T*g(r(1, h(39366)));
    if (f("qcarrot_0")) return d(118098/5, h(118098))/T*g(r(1, h(118098)));
    if (f("ucarrot") || f("ucarrot_1")) return d(13122, h(13122))/T*g(r(1, h(13122))+0.5);
    if (f("carrot") || f("carrot_1")) return d(39366, h(39366))/T*g(r(1, h(39366))+0.5);
    if (f("qcarrot") || f("carrot_1")) return d(118098, h(118098))/T*g(r(1, h(118098))+0.5);
    if (f("uchip")) return d(5103, h(2187))*10/T*g(r(2.5, h(2187)) + 0.9**10/(1-0.9**10)*0.04);
    if (f("chip")) return d(15309, h(2187))*10/T*g(r(2.5, h(2187)) + 0.9**10/(1-0.9**10)*0.04);
    if (f("qchip")) return d(45927, h(2187))*10/T*g(r(2.5, h(2187)) + 0.9**10/(1-0.9**10)*0.04);
    if (f("uclaw_0")) return d(3645, h(7290))/T*g(r(3.5, h(7290)));
    if (f("uclaw") || f("uclaw_1")) return d(3645, h(7290), "uclaw")/T*g(r(3.5, h(7290)));
    if (f("claw_0")) return d(10935, h(21870))/T*g(r(3.5, h(21870)));
    if (f("claw") || f("claw_1")) return d(10935, h(21870), "claw")/T*g(r(3.5, h(21870)));
    if (f("qclaw_0")) return d(32805, h(65610))/T*g(r(3.5, h(65610)));
    if (f("qclaw") || f("qclaw_1")) return d(32805, h(65610), "qclaw")/T*g(r(3.5, h(65610)));
    if (f("uclay") || f("uclay_0")) return d(3645, h(7290))/T*g(r(2, h(7290)));
    if (f("uclay_1")) return d(72900, h(7290))/T*g(r(2, h(7290)));
    if (f("clay") || f("clay_0")) return d(10935, h(21870))/T*g(r(2, h(21870)));
    if (f("clay_1")) return d(218700, h(21870))/T*g(r(2, h(21870)));
    if (f("qclay") || f("qclay_0")) return d(32805, h(65610))/T*g(r(2, h(65610)));
    if (f("qclay_1")) return d(656100, h(65610))/T*g(r(2, h(65610)));
    if (f("ucog")) return d(13851, h(9477))/T*g(r(2.5, h(9477)));
    if (f("cog")) return d(41553, h(28431))/T*g(r(2.5, h(28431)));
    if (f("qcog")) return d(124659, h(85293))/T*g(r(2.5, h(85293)));
    if (f("ucoin")) return d(10935, h(7290))/T*g(r(2.5, h(7290)));
    if (f("coin")) return d(32805, h(21870))/T*g(r(2.5, h(21870)));
    if (f("qcoin")) return d(98415, h(65610))/T*g(r(2.5, h(65610)));
    if (f("ucoral")) return d(8019*3/7)/T*g(r(1.5)+0.08)*7;
    if (f("coral")) return d(24057*3/7)/T*g(r(1.5)+0.08)*7;
    if (f("qcoral")) return d(72171*3/7)/T*g(r(1.5)+0.08)*7;
    if (f("ucorn")) return d(5832, h(145800))/T*g(r(7, h(145800)));
    if (f("corn")) return d(17496, h(437400))/T*g(r(7, h(437400)));
    if (f("qcorn")) return d(52488, h(1312200))/T*g(r(7, h(1312200)));
    if (f("udandelion")) return d(1944, h(1944))/T*g(r(1, h(1944)))*(3+dup);
    if (f("dandelion")) return d(5832, h(5832))/T*g(r(1, h(5832)))*(3+dup);
    if (f("qdandelion")) return d(17496, h(17496))/T*g(r(1, h(17496)))*(3+dup);
    if (f("udice")) return d(7290*(2.7+1.36*luck), h(7290))/T*g(r(2.5, h(7290)));
    if (f("dice")) return d(21870*(2.7+1.36*luck), h(21870))/T*g(r(2.5, h(21870)));
    if (f("qdice")) return d(65610*(2.7+1.36*luck), h(65610))/T*g(r(2.5, h(65610)));
    if (f("udomino")) return (d(0, h(11664))*7+d(729, h(11664))+d(729*2, h(11664))+d(729*3, h(11664))+d(729*4, h(11664))*2+d(729*5, h(11664))+d(729*6, h(11664))*2+d(729*8, h(11664))+d(729*9, h(11664))+d(729*10, h(11664))+d(729*12, h(11664))*2+d(729*15, h(11664))+d(729*16, h(11664))+d(729*18, h(11664))+d(729*20, h(11664))+d(729*24, h(11664))+d(729*25, h(11664))+d(729*30, h(11664))+d(729*36, h(11664)))/T*g(r(1.0, h(11664)))/28;
    if (f("domino")) return (d(0, h(34992))*7+d(2187, h(34992))+d(2187*2, h(34992))+d(2187*3, h(34992))+d(2187*4, h(34992))*2+d(2187*5, h(34992))+d(2187*6, h(34992))*2+d(2187*8, h(34992))+d(2187*9, h(34992))+d(2187*10, h(34992))+d(2187*12, h(34992))*2+d(2187*15, h(34992))+d(2187*16, h(34992))+d(2187*18, h(34992))+d(2187*20, h(34992))+d(2187*24, h(34992))+d(2187*25, h(34992))+d(2187*30, h(34992))+d(2187*36, h(34992)))/T*g(r(1.0, h(34992)))/28;
    if (f("qdomino")) return (d(0, h(104976))*7+d(6561, h(104976))+d(6561*2, h(104976))+d(6561*3, h(104976))+d(6561*4, h(104976))*2+d(6561*5, h(104976))+d(6561*6, h(104976))*2+d(6561*8, h(104976))+d(6561*9, h(104976))+d(6561*10, h(104976))+d(6561*12, h(104976))*2+d(6561*15, h(104976))+d(6561*16, h(104976))+d(6561*18, h(104976))+d(6561*20, h(104976))+d(6561*24, h(104976))+d(6561*25, h(104976))+d(6561*30, h(104976))+d(6561*36, h(104976)))/T*g(r(1.0, h(104976)))/28;
    if (f("udust")) return d(3159, h(1215))/T*g(r(0.8, h(1215))*(3+dup));
    if (f("dust")) return d(9477, h(3645))/T*g(r(0.8, h(3645))*(3+dup));
    if (f("qdust")) return d(28431, h(10935))/T*g(r(0.8, h(10935))*(3+dup));
    if (f("uagg")) return d(4374, mh(182250), "uagg")/T*g(mr(60, mh(182250)))*(4+dup);
    if (f("agg")) return d(13122, mh(546750), "agg")/T*g(mr(60, mh(547650)))*(4+dup);
    if (f("qagg")) return d(39366, mh(1640250), "qagg")/T*g(mr(60, mh(1640250)))*(4+dup);
    if (f("ubgg")) return d(5103, mh(364500), "ubgg")/T*g(mr(30, mh(1093500)));
    if (f("bgg")) return d(15309, mh(1093500), "bgg")/T*g(mr(30, mh(1093500)));
    if (f("qbgg")) return d(45927, mh(3280500), "qbgg")/T*g(mr(30, mh(3280500)));
    if (f("ufang")) return d(10935)/T*g(r(3.5));
    if (f("fang")) return d(32805)/T*g(r(3.5));
    if (f("qfang")) return d(98415)/T*g(r(3.5));
    if (f("ufaster")) return d(8748, h(3645))/T*g(r(2.5, h(3645)));
    if (f("faster")) return d(26244, h(10935))/T*g(r(2.5, h(10935)));
    if (f("qfaster")) return d(78732, h(32805))/T*g(r(2.5, h(32805)));
    if (f("ufragment")) return d(364.5, h(364.5))/T*g(r(10, h(364.5)))*2;
    if (f("fragment")) return d(729, h(729))/T*g(r(10, h(729)))*3;
    if (f("qmjolnir") || f("qmjölnir")) return d(328050, h(328050), "qmjolnir")/T*g(r(8, h(328050)));
    if (f("uglass")) return d(16038)/T*g(1);
    if (f("glass")) return d(48114)/T*g(1);
    if (f("qglass")) return d(144342)/T*g(1);
    if (f("ugrapes") || f("ugrapes_0")) return d(2187, h(3645))/T*g(r(1.5, h(3645)));
    if (f("ugrapes_1") || f("ugrapes_2") || f("ugrapes_3") || f("ugrapes_4") || f("ugrapes_5") || f("ugrapes_6")) return d(2187, h(3645))/T*g(r(1.5, h(3645)+0.5))*t();
    if (f("grapes") || f("grapes_0")) return d(6561, h(10935))/T*g(r(1.5, h(10935)));
    if (f("grapes_1") || f("grapes_2") || f("grapes_3") || f("grapes_4") || f("grapes_5") || f("grapes_6")) return d(6561, h(10935))/T*g(r(1.5, h(10935)+0.5))*t();
    if (f("qgrapes") || f("qgrapes_0")) return d(19683, h(32805))/T*g(r(1.5, h(32805)));
    if (f("qgrapes_1") || f("qgrapes_2") || f("qgrapes_3") || f("qgrapes_4") || f("qgrapes_5") || f("qgrapes_6")) return d(19683, h(32805))/T*g(r(1.5, h(32805)+0.5))*t();
    if (f("uheavy")) return d(9477, h(109350))/T*g(r(10, h(109350)));
    if (f("heavy")) return d(28431, h(328050))/T*g(r(10, h(328050)));
    if (f("qheavy")) return d(85293, h(984150))/T*g(r(10, h(984150)));
    if (f("uiris")) return d(3645, h(3645))/T*g(r(4, h(3645)));
    if (f("iris")) return d(10935, h(10935))/T*g(r(4, h(10935)));
    if (f("qiris")) return d(32805, h(32805))/T*g(r(4, h(32805)));
    if (f("ujelly")) return d(7290, h(7290))/T*g(hr(10, h(7290)));
    if (f("jelly")) return d(21870, h(21870))/T*g(hr(10, h(21870)));
    if (f("qjelly")) return d(65610, h(65610))/T*g(hr(10, h(65610)));
    if (f("ulaser_0")) return d(3645, h(7290))/T*g(hr(5, h(7290)));
    if (f("ulaser") || f("ulaser_1")) return 36450;
    if (f("laser_0")) return d(10935, h(21870))/T*g(hr(5, h(21870)));
    if (f("laser") || f("laser_1")) return 109350;
    if (f("qlaser_0")) return d(32805, h(65610))/T*g(hr(5, h(65610)));
    if (f("qlaser") || f("qlaser_1")) return 328050;
    if (f("uleaf") || f("uleaf(magic)")) return d(11664, h(8748))/T*g(r(1.8, h(8748)));
    if (f("leaf") || f("leaf(magic)")) return d(34992, h(26244))/T*g(r(1.8, h(26244)));
    if (f("qleaf") || f("qleaf(magic)")) return d(104976, h(78732))/T*g(r(1.8, h(78732)));
    if (f("udl") || f("uleaf(dead)")) return d(11664, h(8748))/T*g(r(1.8/1.05, h(8748/petalhealth*(petalhealth-0.3))));
    if (f("dl") || f("leaf(dead)")) return d(34992, h(26244))/T*g(r(1.8/1.05, h(26244/petalhealth*(petalhealth-0.45))));
    if (f("qdl") || f("qleaf(dead)")) return d(104976, h(78732))/T*g(r(1.8/1.05, h(78732/petalhealth*(petalhealth-0.6))));
    if (f("ugl") || f("uleaf(golden)")) return d(11664, h(8748))/T*g(r(2.5/0.825, h(8748)));
    if (f("gl") || f("leaf(golden)")) return d(34992, h(26244))/T*g(r(2.5/0.8, h(26244)));
    if (f("qgl") || f("qleaf(golden)")) return d(104976, h(78732))/T*g(r(2.5/0.775, h(78732)));
    if (f("ulentil")) return d(9477, h(8748))/T*g(r(2, h(8748)));
    if (f("lentil")) return d(28431, h(26244))/T*g(r(2, h(26244)));
    if (f("qlentil")) return d(85293, h(78732))/T*g(r(2, h(78732)));
    if (f("ulight")) return d(1895.4, h(729))/T*g(r(0.8, h(729)))*(5+dup);
    if (f("light")) return d(5686.2, h(2187))/T*g(r(0.8, h(2187)))*(5+dup);
    if (f("qlight")) return d(17058.6, h(6561))/T*g(r(0.8, h(6561)))*(5+dup);
    if (f("ulightning")) return d(8748, h(14580), "ulightning")/T*g(r(2.5));
    if (f("lightning")) return d(26244, h(43740), "lightning")/T*g(r(2.5));
    if (f("qlightning")) return d(78732, h(131220), "qlightning")/T*g(r(2.5));
    if (f("umissile_0") || f("umissile(mecha)_0")) return d(25515/5, h(1458))/T*g(r(1.5, h(1458)));
    if (f("umissile") || f("umissile_1") || f("umissile(mecha)") || f("umissile(mecha)_1")) return d(25515, h(1458))/T*g(r(1.5, h(1458))+0.5);
    if (f("missile_0") || f("missile(mecha)_0")) return d(76545/5, h(4374))/T*g(r(1.5, h(4374)));
    if (f("missile") || f("missile_1") || f("missile(mecha)") || f("missile(mecha)_1")) return d(76545, h(4374))/T*g(r(1.5, h(4374))+0.5);
    if (f("qmissile_0") || f("qmissile(mecha)_0")) return d(229635/5, h(13122))/T*g(r(1.5, h(13122)));
    if (f("qmissile") || f("qmissile_1") || f("qmissile(mecha)") || f("qmissile(mecha)_1")) return d(229635, h(13122))/T*g(r(1.5, h(13122))+0.5);
    if (f("uorange")) return d(5832, h(4860))/T*g(r(3.5, h(4860)))*(3+dup);
    if (f("orange")) return d(17496, h(14580))/T*g(r(3.5, h(14580)))*(3+dup);
    if (f("qorange")) return d(52488, h(43740))/T*g(r(3.5, h(43740)))*(3+dup);
    if (f("upearl") || f("upearl_0")) return d(14580, h(36450))/T*g(r(4, h(36450)));
    if (f("upearl_1")) return d(14580, h(36450))/T*g(r(4, h(36450))+0.5);
    if (f("pearl") || f("pearl_0")) return d(43740, h(109350))/T*g(r(4, h(109350)));
    if (f("pearl_1")) return d(43740, h(109350))/T*g(r(4, h(109350))+0.5);
    if (f("qpearl") || f("qpearl_0")) return d(131220, h(328050))/T*g(r(4, h(328050)));
    if (f("qpearl_1")) return d(131220, h(328050))/T*g(r(4, h(328050))+0.5);
    if (f("upeas") || f("upeas_0")) return d(10935, h(3645))/T*g(r(1.5, h(3645)));
    if (f("upeas_1") || f("upeas_2") || f("upeas_3") || f("upeas_4") || f("upeas_5") || f("upeas_6")) return d(10935, h(3645))/T*g(r(1.5, h(3645))+0.5)*t();
    if (f("peas") || f("peas_0")) return d(32805, h(10935))/T*g(r(1.5, h(10935)));
    if (f("peas_1") || f("peas_2") || f("peas_3") || f("peas_4") || f("peas_5") || f("peas_6")) return d(32805, h(10935))/T*g(r(1.5, h(10935))+0.5)*t();
    if (f("qpeas") || f("qpeas_0")) return d(98415, h(32805))/T*g(r(1.5, h(32805)));
    if (f("qpeas_1") || f("qpeas_2") || f("qpeas_3") || f("qpeas_4") || f("qpeas_5") || f("qpeas_6")) return d(98415, h(32805))/T*g(r(1.5, h(32805))+0.5)*t();
    if (f("upincer")) return d(3645, h(3645))/T*g(r(2.5, h(3645)));
    if (f("pincer")) return d(10935, h(10935))/T*g(r(2.5, h(10935)));
    if (f("qpincer")) return d(32805, h(32805))/T*g(r(2.5, h(32805)));
    if (f("upollen_0")) return d(9234, h(1215))/T*g(r(2, h(1215)))*(3+dup);
    if (f("upollen") || f("upollen_1")) return d(9234, h(1215))/T*g(r(2, h(1215))+0.5)*(3+dup);
    if (f("pollen_0")) return d(27702, h(3645))/T*g(r(2, h(3645)))*(3+dup);
    if (f("pollen") || f("pollen_1")) return d(27702, h(3645))/T*g(r(2, h(3645))+0.5)*(3+dup);
    if (f("qpollen_0")) return d(83106, h(10935))/T*g(r(2, h(10935)))*(3+dup);
    if (f("qpollen") || f("qpollen_1")) return d(83106, h(10935))/T*g(r(2, h(10935))+0.5)*(3+dup);
    if (f("uprivet")) return poisond*0.2/T*g(r(4*0.7**6));
    if (f("privet")) return poisond*0.2/T*g(r(4*0.7**7));
    if (f("qprivet")) return poisond*0.2/T*g(r(4*0.7**8));
    if (f("urice")) return d(2916, h(729))/T*g(r(0.05, h(729)));
    if (f("rice")) return d(8748, h(2187))/T*g(r(0.05, h(2187)));
    if (f("qrice")) return d(26244, h(6561))/T*g(r(0.05, h(6561)));
    if (f("urock")) return d(16038, h(21870))/T*g(r(3, h(21870)));
    if (f("rock")) return d(48114, h(65610))/T*g(r(3, h(65610)));
    if (f("qrock")) return d(144342, h(196830))/T*g(r(3, h(196830)));
    if (f("usand")) return d(3645, h(911.25))/T*g(r(1.5, h(911.25)))*(4+dup);
    if (f("sand")) return d(10935, h(2733.75))/T*g(r(1.5, h(2733.75)))*(4+dup);
    if (f("qsand")) return d(32805, h(8201.25))/T*g(r(1.5, h(8201.25)))*(4+dup);
    if (f("usawblade")) return d(29160, h(18225))/T*g(r(2.5, h(18225)));
    if (f("sawblade")) return d(87480, h(54675))/T*g(r(2.5, h(54675)));
    if (f("qsawblade")) return d(262440, h(164025))/T*g(r(2.5, h(164025)));
    if (f("ustarfish")) return d(3645, h(5103))/T*g(r(1.5, h(5103)));
    if (f("starfish")) return d(10935, h(15309))/T*g(r(1.5, h(15309)));
    if (f("qstarfish")) return d(32805, h(45927))/T*g(r(1.5, h(45927)));
    if (f("ustick")) return d(65610, mh(65610), "ustick")/5*4;
    if (f("stick")) return d(65610, mh(65610), "stick")/5*4;
    if (f("qstick")) return d(65610, mh(65610), "qstick")/5*4;
    if (f("ustinger")) return d(14580)/T*g(r(10))*(5+dup);
    if (f("stinger")) return d(43740)/T*g(r(10))*(5+dup);
    if (f("qstinger")) return d(131220)/T*g(r(10))*(5+dup);
    if (f("ustinger(blood)")) return d(14580)/T*g(r(7.5))*(5+dup);
    if (f("stinger(blood)")) return d(43740)/T*g(r(7.5))*(5+dup);
    if (f("qstinger(blood)")) return d(131220)/T*g(r(7.5))*(5+dup);
    if (f("utomato_0")) return d(3645, h(7290))/T*g(r(2.5, h(7290)));
    if (f("utomato") || f("utomato_1")) return d(51030, h(7290))/T*g(r(2.5, h(7290))+1);
    if (f("tomato_0")) return d(10935, h(21870))/T*g(r(2.5, h(21870)));
    if (f("tomato") || f("tomato_1")) return d(153090, h(21870))/T*g(r(2.5, h(21870))+1);
    if (f("qtomato_0")) return d(32805, h(65610))/T*g(r(2.5, h(65610)));
    if (f("qtomato") || f("qtomato_1")) return d(459270, h(65610))/T*g(r(2.5, h(65610))+1);
    if (f("utriangle")) return d(3645+2916*(utri-1), h(7290))/T*g(r(2.0, h(7290)));
    if (f("triangle")) return d(10935+8748*(tri-1), h(21870))/T*g(r(2.0, h(21870)));
    if (f("qtriangle")) return d(32805+26244*tri, h(65610))/T*g(r(2.0, h(65610)));
    if (f("uuranium")) return 0;
    if (f("uranium")) return 0;
    if (f("quranium")) return 0;
    if (f("uweb(electric)")) return 3645;
    if (f("web(electric)")) return 10935;
    if (f("qweb(electric)")) return 32805;
    if (f("uwing")) return d(14580, h(7290))/T*g(r(3, h(7290)));
    if (f("wing")) return d(43740, h(21870))/T*g(r(3, h(21870)));
    if (f("qwing")) return d(131220, h(65610))/T*g(r(3, h(65610)));
    if (f("uyucca")) return d(3645, h(7290))/T*g(r(2.5, h(7290)));
    if (f("yucca")) return d(10935, h(21870))/T*g(r(2.5, h(21870)));
    if (f("qyucca")) return d(32805, h(65610))/T*g(r(2.5, h(65610)));
    return 0;
}

function analyze_for_web(build, talent, x, y, mode, lentildis = 0.0, rotspeed = 1.0, angle = 138.0) {
    if (mode === "lentil" || mode === "yy") angle = 360;
    let build_arr = build.trim().split(/\s+/);
    if (build_arr.length > 20) build_arr = build_arr.slice(0, 20);

    while (true) {
        let flag = true;
        for (let i = 0; i < build_arr.length; i++) {
            let petal = build_arr[i];
            if (!petal) continue;
            if ("0123456789".includes(petal[0])) {
                flag = false;
                let times = "";
                for (let j of petal) {
                    if ("0123456789".includes(j)) times += j;
                    else break;
                }
                build_arr.splice(i, 1);
                let rep = Math.min(100, parseInt(times));
                for (let j = 0; j < rep; j++) build_arr.splice(i, 0, petal.slice(times.length));
                break;
            }
        }
        if (flag) break;
    }

    let talent_arr = talent.trim().split(/\s+/);
    tp = 45;
    try {
        petalhealth = ph_buff[talent_arr[0]]; tp += ph_tp[talent_arr[0]];
        reload = reload_buff[talent_arr[1]]; tp += reload_tp[talent_arr[1]];
        summoner = summoner_buff[talent_arr[2]]; tp += summoner_tp[talent_arr[2]];
        luck = luck_buff[talent_arr[3]]; tp += luck_tp[talent_arr[3]];
        poison = poison_buff[talent_arr[4]] * cpoison_buff[talent_arr[5]]; tp += poison_tp[talent_arr[4]]; tp += cpoison_tp[talent_arr[5]];
        dup = dup_buff[talent_arr[6]]; tp += dup_tp[talent_arr[6]];
        rot = 2.5;
        if (talent_arr.length >= 8) { rot += rot_buff[talent_arr[7]]; tp += rot_tp[talent_arr[7]]; }
        if (talent_arr.length >= 9) tp += reach_tp[talent_arr[8]];
        if (talent_arr.length >= 10) tp += health_tp[talent_arr[9]];
    } catch (e) {
        return { error: "输入有误（talent长度或内容错误）！" };
    }

    if (dup === 3) {
        build_arr.unshift(build_arr[0]);
        dup = 2;
    }
    ed = x;
    ea = y;
    dis = lentildis;

    // 增益不可叠加判断
    const hasExact = (arr, base) => arr.some(p => p === base || p === 's' + base || p.startsWith(base + '_') || p.startsWith('s' + base + '_'));

    if (hasExact(build_arr, "qbur")) ea -= 9841.5;
    else if (hasExact(build_arr, "bur")) ea -= 3280.5;
    else if (hasExact(build_arr, "ubur")) ea -= 1093.5;

    if (hasExact(build_arr, "qclover")) luck += 0.9;
    else if (hasExact(build_arr, "clover")) luck += 0.8;
    else if (hasExact(build_arr, "uclover")) luck += 0.7;

    rot += build_arr.filter(p => p === "ufaster" || p === "ufaster_").length * 1.7;
    rot += build_arr.filter(p => p === "faster" || p === "faster_" || p === "sfaster" || p === "sfaster_").length * 1.9;
    rot += build_arr.filter(p => p === "qfaster" || p === "qfaster_").length * 2.1;

    let rot_tmp = rot;
    rot *= 0.3 + rotspeed * 0.7;
    T = 2 * Math.PI / rot;

    udl = build_arr.filter(p => p === "udl" || p === "uleaf(dead)" || p === "udl_" || p === "uleaf(dead)_").length;
    dl = build_arr.filter(p => p === "dl" || p === "sdl" || p === "leaf(dead)" || p === "sleaf(dead)" || p === "dl_" || p === "sdl_" || p === "leaf(dead)_" || p === "sleaf(dead)_").length;
    qdl = build_arr.filter(p => p === "qdl" || p === "qleaf(dead)" || p === "qdl_" || p === "qleaf(dead)_").length;
    ugl = build_arr.filter(p => p === "ugl" || p === "uleaf(golden)" || p === "ugl_" || p === "uleaf(golden)_").length;
    gl = build_arr.filter(p => p === "gl" || p === "sgl" || p === "leaf(golden)" || p === "sleaf(golden)" || p === "gl_" || p === "sgl_" || p === "leaf(golden)_" || p === "sleaf(golden)_").length;
    qgl = build_arr.filter(p => p === "qgl" || p === "qleaf(golden)" || p === "qgl_" || p === "qleaf(golden)_").length;

    let hasPetal = (base) => build_arr.some(p => p === base || p === 's' + base || p.startsWith(base + '_') || p.startsWith('s' + base + '_'));

    poisond = 0;
    if (hasPetal("ugrapes")) poisond = Math.max(poisond, 18225/0.7);
    if (hasPetal("grapes")) poisond = Math.max(poisond, 54675/0.7);
    if (hasPetal("qgrapes")) poisond = Math.max(poisond, 164025/0.7);
    if (hasPetal("uiris")) poisond = Math.max(poisond, 17010);
    if (hasPetal("iris")) poisond = Math.max(poisond, 51030);
    if (hasPetal("qiris")) poisond = Math.max(poisond, 153090);
    if (hasPetal("upincer")) poisond = Math.max(poisond, 14580);
    if (hasPetal("pincer")) poisond = Math.max(poisond, 43740);
    if (hasPetal("qpincer")) poisond = Math.max(poisond, 131220);
    if (hasPetal("uuranium")) poisond = Math.max(poisond, 36450);
    if (hasPetal("uranium")) poisond = Math.max(poisond, 109350);
    if (hasPetal("quranium")) poisond = Math.max(poisond, 328050);
    poisond *= poison;

    utri = build_arr.filter(p => p === "utriangle" || p === "utriangle_").length;
    tri = build_arr.filter(p => p === "triangle" || p === "striangle" || p === "triangle_" || p === "striangle_").length;

    let dps_vals = [];
    let builds = [];
    build_arr = build_arr.filter(p => p);

    for (let petal of build_arr) {
        builds.push(petal);
        if (mode === "lentil" || mode === "yy") {
            dps_vals.push(Math.round(cal(petal)));
        } else if (mode === "wheel") {
            dps_vals.push(Math.round(calw(petal, angle)));
        }
    }

    if (poisond !== 0) {
        builds.push("poison");
        dps_vals.push(Math.round(poisond));
    }

    let total = dps_vals.reduce((a, b) => a + b, 0);
    let wheel_info = [];
    if (mode === "wheel") {
        wheel_info.push(`Rotation Speed: ${rot_tmp}*(0.3+0.7*${rotspeed})=${rot.toFixed(3)}`);
        wheel_info.push(`Period(T): ${(2 * Math.PI / rot).toFixed(3)}s`);
    }

    return {
        builds: builds,
        dps: dps_vals.map(String),
        total: total.toString(),
        wheel_info: wheel_info
    };
}
