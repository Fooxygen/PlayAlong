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
| `cases/` | 案卷原始文本、案卷结构文本 |
| `docs/` | 依赖手册、运行手册、验证手册，案卷原始文本结构化提示词 |
| `ifpkg/` | Dify 应用包 |
| `scripts/` | 案卷校验与写入脚本 |
| `web/` | 前端后端与资源文件 |

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

## 快速开始

- 阅读 `docs/deps.md` 了解 PlayAlong 的依赖环境；
- 阅读 `docs/run.md` 了解 PlayAlong 的配置运行步骤；
- 阅读 `docs/verify.md` 了解 PlayAlong 的验证步骤；
- 使用 `docs/case_struct.md` 便于 Agent 完成案卷原始文本至结构文本的转换；

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## 许可证

Copyright (c) 2026 Fooxygen. With BaseTUT. Licensed under the [MIT License](LICENSE).

<p align="right"><a href="#readme-top">↑ Back to top</a></p>
