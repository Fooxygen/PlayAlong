# 猫的葬礼

## metadata

- pack_id: pack03
- title: 猫的葬礼
- version: 1
- description: 宠物殡葬师失踪了。今天下午有一场猫的葬礼，猫主人、合伙人和物业都在等你。
- difficulty: 2
- rounds: 6

## profile

- name: 阿栗
- age: 31
- occupation: 宠物殡葬师，兼做宠物临终摄影
- personality: 温和，怕冲突，答应别人的事很难拒绝
- appearance: 瘦高，常穿深绿色围裙，右手虎口有一道猫抓的旧疤
- disappearance: 3 月 22 日夜里关店后没有回家，手机落在店里，冷藏柜空着
- secret: 猫没有死。阿栗把它藏了起来，因为周淑芬要用猫的死亡去争一笔遗产。周淑芬发现猫不见后，阿栗躲了起来。

## npcs

### npc1 周淑芬（猫主人）

- id: npc1
- name: 周淑芬
- relation: 猫的主人，葬礼的委托人
- age: 72
- personality: 要强，讲究，嘴上不饶人
- speech_style: 说话慢，喜欢用"我们那时候"开头，句尾常带"你说呢"
- opening: 团团呢？我看看它。
- greeting_hint: 压着情绪
- intro: 周淑芬坐在店门口的小板凳上，腿上放着一个旧猫包。她没有看你，只盯着店里的冷藏柜。

#### q1 猫在哪

- content: 团团呢？葬礼几点开始？
- topic: 猫
- targets: f11

#### q2 昨晚的电话

- content: 阿栗昨晚给我打电话，说今天可能办不了。他跟你说了什么？
- topic: 电话
- targets: f12

#### f11 空着的猫笼

- id: f11
- topic: 猫
- text: 团团昨天还在，今天早上猫笼空了；葬礼订单上写着"不要火化"。
- accepts: 在准备, 马上, 还没, 在里面, 不要火化
- keywords: 团团, 葬礼, 猫笼, 火化
- weight: 2
- reaction_if_missed: 「团团呢？我看看它。」
- source_fragment: g1

#### f12 办不了的那通电话

- id: f12
- topic: 电话
- text: 阿栗昨晚给周淑芬打过电话，说"明天可能办不了"，她没听完就挂了。
- accepts: 打了, 说了, 办不了, 没听完, 不知道
- keywords: 电话, 昨晚, 办不了
- weight: 1
- reaction_if_missed: 「他昨晚给我打电话，说今天可能办不了。」
- source_fragment:

### npc2 许放（合伙人）

- id: npc2
- name: 许放
- relation: 店里的合伙人，负责账目
- age: 35
- personality: 精明，急躁，说话直
- speech_style: 短句，喜欢用数字，常打断别人
- opening: 账上少了两千，阿栗人呢？
- greeting_hint: 不耐烦
- intro: 许放把账本摊在前台，计算器按得啪啪响。他看见你进来，先看了一眼你身后的冷藏柜。

#### q1 账上的两千

- content: 阿栗去哪了？账上那两千是你拿的吗？
- topic: 账目
- targets: f21

#### q2 空着的冷藏柜

- content: 冷藏柜怎么是空的？昨天送来的那只猫呢？
- topic: 冷藏柜
- targets: f22

#### f21 医院的用途

- id: f21
- topic: 账目
- text: 账上少了两千，是阿栗取走的，用途写着"医院"。
- accepts: 医院, 看病, 急用, 我拿的, 会补
- keywords: 两千, 医院, 账
- weight: 2
- reaction_if_missed: 「这两千到底去哪了？」
- source_fragment: g4

#### f22 本该在那里的猫

- id: f22
- topic: 冷藏柜
- text: 冷藏柜里本该有一只待火化的猫，现在空了。
- accepts: 送走了, 火化了, 转移了, 不知道, 在准备
- keywords: 冷藏柜, 猫, 空的
- weight: 3
- reaction_if_missed: 「冷藏柜怎么是空的？」
- source_fragment: g2

### npc3 老魏（物业）

- id: npc3
- name: 老魏
- relation: 物业保安队长
- age: 50
- personality: 爱管闲事，怕担责
- speech_style: 公事公办，喜欢说"按规定"
- opening: 昨晚你们店里猫叫了一宿，投诉电话都打到我这儿了。
- greeting_hint: 例行公事
- intro: 老魏站在店门外的台阶上，手里拿着一本巡逻记录。他先指了指后门的监控，才看向你。

#### q1 夜里的猫叫

- content: 昨晚店里为什么有猫叫？
- topic: 投诉
- targets: f31

#### q2 后门的监控

- content: 监控里阿栗半夜拎着一个箱子出去，去哪了？
- topic: 监控
- targets: f32

#### f31 夜里的投诉

- id: f31
- topic: 投诉
- text: 昨晚十一点店里有猫叫，物业接到投诉。
- accepts: 猫叫, 新来的, 寄养, 不知道, 马上去看
- keywords: 猫叫, 昨晚, 投诉
- weight: 1
- reaction_if_missed: 「昨晚猫叫了一宿，怎么回事？」
- source_fragment:

#### f32 凌晨的箱子

- id: f32
- topic: 监控
- text: 监控拍到阿栗凌晨拎着宠物箱从后门离开。
- accepts: 医院, 送猫, 有事, 不知道, 去看病
- keywords: 监控, 箱子, 后门
- weight: 3
- reaction_if_missed: 「监控里他半夜拎着箱子出去了。」
- source_fragment: g5

## fragments

### g1 一张订单

- id: g1
- title: 一张订单
- text: 3 月 20 号，周淑芬订了一场猫的葬礼。备注栏写着：不要火化。
- certainty: accurate
- keywords: 订单, 3月20, 不要火化, 猫
- requires: {npc: npc1, mentions: 葬礼}

### g2 空着的格子

- id: g2
- title: 空着的格子
- text: 冷藏柜第二层是空的。昨天送来的那只猫本来应该放在那里。
- certainty: accurate
- keywords: 冷藏柜, 空, 第二层
- requires: {npc: npc2, mentions: 冷藏柜}

### g3 没发出去的语音

- id: g3
- title: 没发出去的语音
- text: 手机里有一段没发出去的语音：它还在，别告诉周阿姨。
- certainty: accurate
- keywords: 语音, 还在, 周阿姨

### g4 化验单

- id: g4
- title: 化验单
- text: 宠物医院的化验单，名字被划掉了。只看得清"肾功能"三个字。
- certainty: inaccurate
- keywords: 化验单, 医院, 肾功能
- requires: {npc: npc2, mentions: 医院}

### g5 备用钥匙

- id: g5
- title: 备用钥匙
- text: 周淑芬家的备用钥匙一直放在店里的抽屉里。阿栗用过很多次。
- certainty: accurate
- keywords: 钥匙, 抽屉, 备用
- requires: {npc: npc3, mentions: 钥匙}
