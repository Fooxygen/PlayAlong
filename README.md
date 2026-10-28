<a id="readme-top"></a>

简体中文 |
[English](./README.en.md)

<div align="center">

  <!-- TODO: 替换为正式 LOGO -->
  <img src="brand_playalong.svg" alt="PlayAlong" style="margin=0">
  <h3 align="center">PlayAlong</h3>
  <p align="center">
    你顶替了一个失踪的人，手里只有他不完整的记忆。
    <br /><br />
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=bug">
      <strong>» 报告问题</strong>
    </a>
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=enhancement">
      <strong>» 请求特性</strong>
    </a>
  </p>

</div>

## 关于仓库

PlayAlong 是一个互动剧情与角色扮演小游戏。你顶替了一位已经失踪的人，用他不完整的记忆应付所有认识他的人。

一局游戏包含：

- 从案卷库选择一份案卷；
- 与若干关系人依次对话；
- 在有限的次数内翻阅失踪者的记忆；
- 用编造的回答填补记忆缺口；
- 在结局中看到哪些记忆是他留下的，哪些是你编的。

应用的流程编排在 Dify 中完成，案卷、对话记录和记忆保存在 PowerContext 中。要运行作品，请参阅下文列出的文档链接。

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 玩法流程

| 阶段 | 任务 |
| - | - |
| 选择案卷 | 从案卷库读取案卷摘要 |
| 对话 | 关系人依次登场，玩家回答问题 |
| 翻阅记忆 | 消耗次数，逐条翻开失踪者的记忆 |
| 判定 | 判断回答是否过关，并检查前后矛盾 |
| 结局 | 列出真实记忆、玩家编造的记忆与复盘 |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 工程目录

| 目录 | 内容 |
| - | - |
| `cases/` | `pack01.md` 案卷作者源、`pack01.json` 运行时数据 |
| `docs/` | `deps.md`、`run.md`、`verify.md` |
| `ifpkg/` | `PlayAlong.ifpkg`，Dify 应用包 |
| `scripts/` | `seed_cases.py`，案卷校验与 PowerContext 写入 |
| `web/` | `index.html`、`server.py` 与前端资源 |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 技术栈

| 类别 | 技术 | 版本 |
| - | - | - |
| 流程编排 | Dify | 1.18.0 |
| 记忆与上下文 | PowerContext | 1.4.0 |
| 模型服务 | MiniMax 插件 | 0.0.29 |
| 前端 | 原生 HTML / CSS / JavaScript | - |
| 本地服务 | Python | 3.12+ |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 文档

| 文档 | 内容 |
| - | - |
| [`docs/deps.md`](./docs/deps.md) | 运行环境、软件与插件版本 |
| [`docs/run.md`](./docs/run.md) | PowerContext、Dify 与本地前端的配置、导入 DSL、初始化数据与启动步骤 |
| [`docs/verify.md`](./docs/verify.md) | 验证样例、操作步骤、预期表现与运行证据 |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 许可证

Copyright (c) 2026 Fooxygen. With BaseTUT. Licensed under the [MIT License](LICENSE).

<p align="right"><a href="#readme-top">↑ Back to top</a></p>
