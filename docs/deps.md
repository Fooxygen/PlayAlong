# 依赖

本页列出运行 PlayAlong 所需的环境、软件与插件版本。

## 运行环境

| 类别 | 技术 | 版本 |
| - | - | - |
| 操作系统 | Linux / WSL2 | Ubuntu 26.04 |
| 容器 | Docker + Docker Compose | 随 Dify 部署 |
| Python | CPython | 3.12+ |
| 浏览器 | Chromium / Firefox | 支持 ES2020 与 Canvas 2D |

## Dify

| 项目 | 说明 |
| - | - |
| 版本 | 1.18.0 |
| 部署方式 | Docker Compose |
| 应用类型 | Chatflow（`advanced-chat`） |
| 依赖插件 | `langgenius/minimax 0.0.29` |
| 外部连接 | HTTP Request 节点访问 PowerContext HTTP API |

## PowerContext

| 项目 | 说明 |
| - | - |
| 版本 | 1.4.0 |
| 部署方式 | 通过 `uv` 安装 |
| 存储 | 嵌入式 SeekDB |
| 使用接口 | `/v1/scopes`、`/v1/memory/remember`、`/v1/memory/entries/list` |

## 模型

| 模型 | 用途 |
| - | - |
| MiniMax-M3.1 | 开场、NPC 回复生成、结局复盘 |
| MiniMax-M3.1-Flash | 矛盾判定 |

模型由 Dify 的 MiniMax 插件提供，具体参数在应用节点内配置。**可根据实际需求切换模型**。

## Python 脚本

| 依赖 | 用途 |
| - | - |
| Python 标准库 | `json`、`urllib`、`argparse`、`pathlib` |
| 第三方包 | 无 |

## 前端

| 项目 | 说明 |
| - | - |
| 页面 | 原生 HTML / CSS / JavaScript |
| 字体 | 开源字体 Maple Mono、Keinann Maru POP |
| 图标 | Font Awesome Free |
| CSS | Tailwind CSS 3.4.17 预编译 |
| 运行时依赖 | 无 |

只有修改样式时才需要 Node.js 重新编译 Tailwind，运行作品不需要。

前端资源已适配离线运行环境。

## 不需要的依赖

- 不需要单独部署 SeekDB：PowerContext 使用嵌入式 SeekDB；
- 不需要 Embedding 或 Rerank 服务；
- 不需要 Node.js 运行前端；
- 不需要额外的数据库或缓存服务。
