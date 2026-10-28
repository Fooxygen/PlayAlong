# 案卷结构文本转换提示词

## 用途

把一份**案卷原始文本**（Markdown）转换为等价的**案卷结构文本**（JSON），供 `scripts/seed_cases.py` 校验并写入 PowerContext。

本文既是提示词，也是格式说明。人可以直接阅读，Agent 可以把“角色”到“错误输出”整段作为指令。

## 术语

| 术语 | 位置 | 含义 |
| - | - | - |
| 案卷原始文本 | `cases/md/<pack_id>.md` | 人工编写的 Markdown 案卷 |
| 案卷结构文本 | `cases/json/<pack_id>.json` | 运行时读取的 JSON 案卷 |
| 记忆片段 | `fragments[]` | 玩家可以翻阅的记忆卡 |

## 角色

你是一个数据转换器。

输入：一份案卷原始文本。

输出：严格符合本文 Schema 的案卷结构文本。

约束：

- 只输出 JSON 本身；
- 不加解释、不加注释、不使用代码块围栏；
- 不新增、删除、重命名任何字段；
- 校验不通过时，输出错误 JSON，不输出半成品。

## 输入结构

案卷原始文本的标题层级与 JSON 位置的对应关系：

| Markdown | 含义 | JSON 位置 |
| - | - | - |
| `# 标题` | 案卷名，忽略 | —— |
| `## metadata` | 元信息 | 顶层 |
| `## profile` | 失踪者档案 | `profile` |
| `## npcs` | 关系人集合 | `npcs[]` |
| `### npcN 名字（关系）` | 一位关系人 | `npcs[].id = "npcN"` |
| `#### qN ...` | 该关系人的一个问题 | `npcs[].questions[]` |
| `#### fN ...` | 该关系人的一条事实 | `npcs[].facts[]` |
| `## fragments` | 记忆片段集合 | `fragments[]` |
| `### gN 标题` | 一条记忆片段 | `fragments[].id = "gN"` |

字段一律写成列表项：

```markdown
- 字段名: 值
```

同一行的多个值用逗号分隔，转换成字符串数组。

## 输出 Schema

```json
{
  "pack_id": "string",
  "title": "string",
  "version": 1,
  "description": "string",
  "difficulty": 1,
  "rounds": 1,
  "profile": {
    "name": "string",
    "age": 0,
    "occupation": "string",
    "personality": "string",
    "appearance": "string",
    "disappearance": "string",
    "secret": "string"
  },
  "npcs": [
    {
      "id": "string",
      "name": "string",
      "relation": "string",
      "age": 0,
      "personality": "string",
      "speech_style": "string",
      "opening": "string",
      "greeting_hint": "string",
      "intro": "string",
      "questions": [
        {
          "id": "string",
          "content": "string",
          "topic": "string",
          "targets": ["string"]
        }
      ],
      "facts": [
        {
          "id": "string",
          "topic": "string",
          "text": "string",
          "accepts": ["string"],
          "keywords": ["string"],
          "weight": 1,
          "reaction_if_missed": "string",
          "source_fragment": "string"
        }
      ]
    }
  ],
  "fragments": [
    {
      "id": "string",
      "title": "string",
      "text": "string",
      "certainty": "accurate",
      "keywords": ["string"],
      "requires": {
        "npc": "string",
        "mentions": "string"
      }
    }
  ]
}
```

## 字段含义

### metadata

| 字段 | 含义 |
| - | - |
| `pack_id` | 案卷编号，与文件名一致 |
| `title` | 案卷标题 |
| `version` | 案卷版本 |
| `description` | 案卷列表与详情页的介绍，不能剧透 |
| `difficulty` | 难度，1 到 5 |
| `rounds` | 预估回合数 |

### profile

失踪者档案。玩家顶替的就是这个人。

| 字段 | 含义 |
| - | - |
| `name` | 姓名 |
| `age` | 年龄 |
| `occupation` | 职业 |
| `personality` | 性格 |
| `appearance` | 外貌，需要说明为什么能被顶替 |
| `disappearance` | 失踪经过 |
| `secret` | 主线真相，不在正常对话中直接泄露 |

### npcs

| 字段 | 含义 |
| - | - |
| `id` | 关系人编号 |
| `name` | 名字 |
| `relation` | 和失踪者的关系 |
| `age` | 年龄 |
| `personality` | 性格 |
| `speech_style` | 说话方式 |
| `opening` | 第一次见面时的第一句话 |
| `greeting_hint` | 给模型的语气提示，不直接展示 |
| `intro` | 登场时的场景叙述，第二人称，说明如何和玩家搭上话 |
| `questions` | 会问玩家的问题 |
| `facts` | 心里的底牌与判定线 |

### questions

| 字段 | 含义 |
| - | - |
| `id` | 问题编号 |
| `content` | 实际问出口的话 |
| `topic` | 话题 |
| `targets` | 试探哪些事实，填写同一 NPC 的 `fact.id` |

如果 `targets` 指向多条事实，工作流需要明确是“答中任意一条”还是“每条都要接住”。

### facts

一条 fact 是一个判定单元。

| 字段 | 含义 |
| - | - |
| `id` | 事实编号 |
| `topic` | 话题 |
| `text` | NPC 知道的真相或认知 |
| `accepts` | 玩家回答的白名单，意思对上即可 |
| `keywords` | 检索锚点 |
| `weight` | 重要程度，1 到 5，越高答错时怀疑加得越多 |
| `reaction_if_missed` | 没答上时的反应 |
| `source_fragment` | 对应哪段记忆；空字符串表示玩家没有这张卡 |

`accepts` 必须覆盖玩家自然会说出的说法，不要求和 `text` 逐字相同。

`source_fragment` 为空是有效值，不表示漏写。

### fragments

玩家可以翻阅的记忆卡。

| 字段 | 含义 |
| - | - |
| `id` | 记忆编号 |
| `title` | 目录中显示的标题，不要剧透关键人物或地点 |
| `text` | 翻开后的内容，通常用第一人称 |
| `certainty` | `accurate` 或 `inaccurate` |
| `keywords` | 检索锚点 |
| `requires` | 可选，出现条件 |
| `requires.npc` | 在哪个关系人面前才会浮现 |
| `requires.mentions` | 对方提到什么词时才会浮现 |

`inaccurate` 是陷阱：玩家照着说，可能反而撞上 NPC 的底牌。判定仍然只看 `accepts`。

## 映射规则

| Markdown | JSON | 类型 |
| - | - | - |
| `- pack_id: pack01` | `pack_id` | string |
| `- version: 1` | `version` | integer |
| `- difficulty: 3` | `difficulty` | integer，1 到 5 |
| `- rounds: 6` | `rounds` | integer，≥1 |
| `- age: 31` | `age` | integer |
| `### npc1 老周（房东）` | `npcs[].id` | string，取 `npc1` |
| `#### q1 ...` | `questions[].id` | string，取 `q1` |
| `#### f11 ...` | `facts[].id` | string，取 `f11` |
| `### g2 鞋底的泥` | `fragments[].id` | string，取 `g2` |
| `- accepts: 凌晨, 两点, 加班` | `accepts` | string[] |
| `- keywords: 凌晨, 两点, 泥` | `keywords` | string[] |
| `- weight: 2` | `weight` | integer，1 到 5 |
| `- source_fragment:` | `source_fragment` | string，空字符串 |
| `- requires: {npc: npc2, mentions: 看海}` | `requires` | object |
| 未出现 `requires` | —— | 整个键省略，不写 null |

## 转换规则

1. 字段名、层级、数量完全照抄，不新增、不删除、不重命名。
2. 数组顺序按小节在文档中出现的顺序。
3. 文本原样搬运，不改写、不总结、不补充、不删标点。
4. 逗号分隔的列表拆成字符串数组，逐项去掉首尾空格，保留顺序。
5. 只有 `version`、`age`、`weight`、`difficulty`、`rounds` 转整数，其余保持字符串。
6. `id` 取小节标题的编号前缀，不取中文名。
7. 缺失的可选键直接省略。

## 一致性校验

输出前逐条检查：

- [ ] 每个 `npc`、`question`、`fact`、`fragment` 的 `id` 与小节编号一致；
- [ ] 所有 `id` 全文唯一；
- [ ] `questions[].targets` 中的 id 都存在于同一个 NPC 的 `facts`；
- [ ] `facts[].source_fragment` 非空时，指向存在的 `fragment`；
- [ ] `fragments[].requires.npc` 指向存在的 `npc`；
- [ ] `certainty` 只能是 `accurate` 或 `inaccurate`；
- [ ] `profile` 七个字段齐全；
- [ ] 每个 NPC 都有 `intro`；
- [ ] `description` 非空，且不泄露 `secret`；
- [ ] `difficulty` 是 1 到 5 的整数；
- [ ] `rounds` 是大于等于 1 的整数。

## 错误输出

校验不通过时，只输出：

```json
{
  "error": "错误类型",
  "reason": "具体说明，指出相关 id"
}
```

示例：

```json
{"error": "dangling_reference", "reason": "npc1.q1.targets 引用了 f99，但 npc1.facts 中不存在 f99"}
```

```json
{"error": "missing_field", "reason": "npc2 缺少 intro"}
```

```json
{"error": "duplicate_id", "reason": "fact id f11 出现两次"}
```

## 示例

输入片段：

```markdown
### npc1 阿岚（吉他手）

- id: npc1
- name: 阿岚
- relation: 乐队吉他手，和阿声写了十年歌
- age: 30
- personality: 稳，护短，嘴上不饶人
- speech_style: 短句，习惯先说"行"，再反驳
- opening: 阿声呢？再不开场，票就白卖了。
- greeting_hint: 压着火
- intro: 阿岚蹲在舞台边调弦，脚边放着两瓶没开的啤酒。

#### q1 最后一次见他

- content: 阿声到底去哪了？你最后一次见他是什么时候？
- topic: 行踪
- targets: f11

#### f11 排练室的嗓子

- id: f11
- topic: 行踪
- text: 阿声昨天还在排练室，嗓子哑得说不出话，只用手比划。
- accepts: 排练室, 嗓子, 哑了, 昨天, 不知道
- keywords: 排练室, 嗓子, 昨天
- weight: 2
- reaction_if_missed: 「他昨天还在排练室，嗓子哑得说不出话。」
- source_fragment:
```

对应输出片段：

```json
{
  "id": "npc1",
  "name": "阿岚",
  "relation": "乐队吉他手，和阿声写了十年歌",
  "age": 30,
  "personality": "稳，护短，嘴上不饶人",
  "speech_style": "短句，习惯先说“行”，再反驳",
  "opening": "阿声呢？再不开场，票就白卖了。",
  "greeting_hint": "压着火",
  "intro": "阿岚蹲在舞台边调弦，脚边放着两瓶没开的啤酒。",
  "questions": [
    {
      "id": "q1",
      "content": "阿声到底去哪了？你最后一次见他是什么时候？",
      "topic": "行踪",
      "targets": ["f11"]
    }
  ],
  "facts": [
    {
      "id": "f11",
      "topic": "行踪",
      "text": "阿声昨天还在排练室，嗓子哑得说不出话，只用手比划。",
      "accepts": ["排练室", "嗓子", "哑了", "昨天", "不知道"],
      "keywords": ["排练室", "嗓子", "昨天"],
      "weight": 2,
      "reaction_if_missed": "「他昨天还在排练室，嗓子哑得说不出话。」",
      "source_fragment": ""
    }
  ]
}
```

## 写入工程

转换结果保存为：

```text
cases/json/<pack_id>.json
```

然后执行：

```powershell
python scripts/seed_cases.py
```

脚本会再次校验字段与引用关系，通过后写入 PowerContext。
