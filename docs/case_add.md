# 增加案卷

本页说明如何新增一份案卷：编写原始文本、转成结构文本、校验、写入 PowerContext，并让 Dify 读到。

## 文件位置

每份案卷有两个文件，`pack_id` 与文件名一致：

```text
cases/md/<pack_id>.md       案卷原始文本
cases/json/<pack_id>.json   案卷结构文本
```

例如 `pack01`：

```text
cases/md/pack01.md
cases/json/pack01.json
```

## 编写规范

完整字段与格式见 [case_struct.md](./case_struct.md)。

当前工作流按以下结构读取案卷：

- 3 位关系人；
- 每位关系人 2 个问题；
- 每位关系人必须有 `intro`；
- 5 条记忆，其中可以有一条 `inaccurate`。

必须满足：

- `pack_id` 与文件名一致；
- `questions[].targets` 指向同一个 NPC 的 `facts`；
- `facts[].source_fragment` 为空字符串，或指向存在的记忆；
- `fragments[].requires.npc` 指向存在的关系人；
- 所有 `id` 在案卷内唯一。

## 使用提示词

- 打开 [case_struct.md](./case_struct.md)；
- 复制“角色”到“错误输出”之间的内容，作为系统提示词；
- 附上案卷原始文本；
- 要求只输出 JSON，不加解释和代码块围栏；
- 把结果保存为 `cases/json/<pack_id>.json`。

如果转换结果返回了 `error`，按 `reason` 修正原始文本后重新转换。

## 校验

先做一次只校验、不写入的检查：

```powershell
python scripts/seed_cases.py --dry-run
```

输出中应包含新案卷和“通过”：

```text
  pack01  通过
  pack02  通过
  pack03  通过
  pack04  通过
```

常见错误：

| error | 原因 |
| - | - |
| `dangling_reference` | `targets`、`source_fragment` 或 `requires.npc` 指向不存在的 id |
| `missing_field` | 缺少 `intro` 或 `profile` 字段 |
| `duplicate_id` | 同一个 id 出现两次 |

## 写入 PowerContext

校验通过后执行：

```powershell
python scripts/seed_cases.py
```

脚本会：

- 校验 `cases/json/` 下的全部案卷；
- 写入或跳过已有案卷；
- 输出案卷库的 scope；
- 把 scope 写回 `.env` 的 `PC_CASE_SCOPE`。

如果案卷内容发生变化，脚本会要求使用新的 scope-key。修改 `scripts/seed_cases.py` 的 `DEFAULT_SCOPE_KEY`，例如从 `v8` 改为 `v9`，然后重跑。

记录输出中的 scope：

```text
Scope scp_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 让 Dify 读取新案卷

不需要重新导入 DSL。DSL 只包含流程和提示词，案卷内容存放在 PowerContext 中。

- 把 Dify 应用环境变量中的 `PC_SCOPE` 改成新的 `PC_CASE_SCOPE`；
- 保存后新建一次对话；
- 在前端重新选择案卷。

## 常见问题

### 加了案卷，Dify 还是旧内容

`PC_SCOPE` 没有同步到新的 scope。

### 记忆目录为空

案卷里没有 `fragments`，或者前端读取的 `pack_id` 与实际写入的不一致。
