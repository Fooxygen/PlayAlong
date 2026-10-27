# 旧钟楼

## metadata

- pack_id: pack01
- title: 旧钟楼
- version: 1

## profile

- name: 沈砚
- age: 31
- occupation: 钟表修复师，在旧城钟楼街有间自己的铺子
- personality: 寡言，较真，给人修东西的时候话会变多
- appearance: 圆脸，左眉骨一道旧疤，笑起来左边少一颗牙——和你几乎一样
- disappearance: 去年 11 月 3 日夜里没有回家，铺子锁着，公寓里留着一件没穿的外套
- secret: 他没有失踪。是他替别人顶了罪名，人现在在城郊的疗养院里

## npcs

### npc1 老周（房东）

- id: npc1
- name: 老周
- relation: 失踪者的房东
- age: 58
- personality: 爱面子，耳朵背，护短
- speech_style: 说话慢，爱反问，句尾常带"你说是不是"
- opening: 哟，回来啦。外套忘椅背上了。
- greeting_hint: 熟络但不亲

#### q1 前天夜里的行踪

- content: 前天夜里你回来得挺晚，去哪儿了？
- topic: 行踪
- targets: f11

#### q2 铺子的事

- content: 你那铺子三天没开门了，隔壁老陈都在问租金。
- topic: 铺子
- targets: f12

#### f11 前天夜里的泥

- id: f11
- topic: 行踪
- text: 前天夜里他回来是凌晨两点多，鞋底沾着河堤边的泥。
- accepts: 回来得晚, 凌晨, 两点, 出去了, 加班, 城西
- keywords: 凌晨, 两点, 泥, 回来, 前天夜里
- weight: 2
- reaction_if_missed: 「前天夜里你回来得挺晚，去哪儿了？」
- source_fragment: g2

#### f12 三天没开门的铺子

- id: f12
- topic: 铺子
- text: 他那间铺子三天没开门了，隔壁老陈抱怨租金。
- accepts: 歇两天, 出门, 有事, 去外地, 休息
- keywords: 铺子, 开门, 三天, 租金, 隔壁
- weight: 1
- reaction_if_missed: 「铺子三天没开门了，邻居都在问。」
- source_fragment:

#### f13 椅背上的外套

- id: f13
- topic: 外套
- text: 他走的那天把一件灰外套落在了铺子椅背上，尺码偏大。
- accepts: 外套, 忘了, 灰外套, 落在铺子, 尺码
- keywords: 外套, 灰, 椅背, 尺码
- weight: 2
- reaction_if_missed: 「你走那天落下的外套，我给你收着呢。」
- source_fragment: g3

### npc2 林可（恋人）

- id: npc2
- name: 林可
- relation: 失踪者的恋人
- age: 29
- personality: 直接，急性子，聪明
- speech_style: 短句为主，语速快，喜欢反问
- opening: 你今天怎么这个语气？
- greeting_hint: 试探

#### q1 没有兑现的约定

- content: 我们说好那天去看海，你没来，也没接电话。
- topic: 约会
- targets: f21

#### q2 你在躲我

- content: 你最近是不是在躲我？
- topic: 心情
- targets: f22, f23

#### f21 没有兑现的约定

- id: f21
- topic: 约会
- text: 他们约好 11 月 2 日去看海，那天她等到半夜，他一直没有出现。
- accepts: 那天没去成, 加班, 堵车, 生病, 忘了
- keywords: 看海, 约定, 那天, 半夜, 没接电话
- weight: 3
- reaction_if_missed: 「我们说好那天去看海，你没来，也没接电话。」
- source_fragment: g1

#### f22 失踪前的话

- id: f22
- topic: 心情
- text: 他失踪前几天总说"想一个人待几天"，她还以为是工作压力。
- accepts: 压力, 想静一静, 工作, 累
- keywords: 压力, 工作, 待几天, 累
- weight: 2
- reaction_if_missed: 「你失踪前老说想一个人待几天，是不是出什么事了？」
- source_fragment: g4

#### f23 鞋柜里的备用钥匙

- id: f23
- topic: 钥匙
- text: 他家阳台门的备用钥匙一直放在鞋柜抽屉里，谁都能拿到。
- accepts: 钥匙, 抽屉, 备用, 知道, 拿过
- keywords: 钥匙, 备用, 鞋柜, 抽屉
- weight: 3
- reaction_if_missed: 「家里备用钥匙还在鞋柜抽屉里。」
- source_fragment:

### npc3 陈队（片警）

- id: npc3
- name: 陈队
- relation: 负责报案的片警
- age: 41
- personality: 公事公办，但愿意多问一句
- speech_style: 简短，公文化，偶尔缓和
- opening: 坐吧。耽误你十分钟。
- greeting_hint: 公事

#### q1 十一月三号的晚上

- content: 十一月三号晚上十点到十二点，你在哪？
- topic: 时间线
- targets: f31

#### q2 一个陌生的名字

- content: 你认识一个叫姜北的人吗？
- topic: 陌生人
- targets: f32

#### f31 监控里的时间线

- id: f31
- topic: 时间线
- text: 监控显示 11 月 3 日 23:40 他从公寓楼出来，往河堤方向走。
- accepts: 在家, 加班, 不知道, 没印象, 河堤
- keywords: 十一, 三号, 晚上, 十点, 十二点, 监控, 河堤
- weight: 3
- reaction_if_missed: 「监控拍到你十一点四十出的门。」
- source_fragment: g2

#### f32 姜北的表

- id: f32
- topic: 陌生人
- text: 他修过一台姜北的表，收了三成定金，尾款一直没付。
- accepts: 修过, 姜北的表, 收过定金, 尾款
- keywords: 姜北, 表, 定金, 尾款, 修
- weight: 4
- reaction_if_missed: 「你认识一个叫姜北的人吗？」
- source_fragment: g5

#### f33 三天之后才立案

- id: f33
- topic: 报失踪
- text: 是他母亲报的失踪，三天之后才立案，所以前几天邻居都没报警。
- accepts: 不知道, 没注意, 邻居, 没报警
- keywords: 报案, 母亲, 三天, 立案, 邻居
- weight: 1
- reaction_if_missed: 「报失踪的是他母亲。」
- source_fragment:

## fragments

### g1 海边的车票

- id: g1
- title: 海边的车票
- text: 11 月 1 号晚上我买了两张去海边的票，第二天早上退了一张。退票的时候手在抖。
- certainty: accurate
- keywords: 海边, 票, 退票, 11月1, 约会
- requires: {npc: npc2, mentions: 看海}

### g2 鞋底的泥

- id: g2
- title: 鞋底的泥
- text: 前天夜里我去了城西、河堤下面那条旧街。雨把路都泡烂了，走一步陷一下。
- certainty: accurate
- keywords: 城西, 河堤, 泥, 前天夜里, 旧街

### g3 椅背上的外套

- id: g3
- title: 椅背上的外套
- text: 那件灰外套是我故意留下的。里面口袋有东西，不能带在身上。
- certainty: accurate
- keywords: 外套, 灰, 口袋, 留下, 椅背

### g4 想一个人待几天

- id: g4
- title: 想一个人待几天
- text: 最近确实出事了。不是我想躲，是我怕连累人。等事情过去我再回去。
- certainty: accurate
- keywords: 出事, 躲, 连累, 压力, 待几天

### g5 姜北

- id: g5
- title: 姜北
- text: 姜北那台表，我根本没见过。我只是收了他三成的钱，剩下的都在他手里。表根本没修。
- certainty: inaccurate
- keywords: 姜北, 表, 钱, 没修, 三成
- requires: {npc: npc3, mentions: 姜北}
