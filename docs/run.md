# 运行

## 工程目录

| 目录 | 内容 |
| - | - |
| `cases/` | 案卷作者源与运行时数据 |
| `docs/` | 依赖、配置与运行文档 |
| `ifpkg/` | `PlayAlong.ifpkg`，Dify 应用包 |
| `scripts/` | 案卷校验与 PowerContext 写入 |
| `web/` | 页面、本地代理与前端资源 |

本文使用以下占位符：

| 占位符 | 含义 |
| - | - |
| `{REPO}` | PlayAlong 工程根目录 |
| `{DIFY_DIR}` | Dify 仓库目录，其中包含 `docker/` |
| `{PC_DIR}` | PowerContext 配置目录 |

请在使用下方的命令和路径时，把占位符替换成实际路径。

## 部署 Dify

### 获取 Dify 1.18.0

克隆 Dify 仓库，并进入其中的 Docker 部署目录。

```bash
git clone https://github.com/langgenius/dify.git --branch 1.18.0 --depth 1 {DIFY_DIR}
cd {DIFY_DIR}/docker
cp .env.example .env
```

### 配置 Dify 环境

编辑 `{DIFY_DIR}/docker/.env`，补充镜像与内网访问配置（以中科大镜像为例）：

```dotenv
PIP_MIRROR_URL=https://mirrors.ustc.edu.cn/pypi/simple
SSRF_PROXY_ALLOW_PRIVATE_DOMAINS=host.docker.internal
```

编辑 `{DIFY_DIR}/docker/docker-compose.yaml`，在 `api`、`worker`、`ssrf_proxy`、`plugin_daemon` 四个服务下各加入：

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

这一步让 Dify 容器能够访问宿主机上的 PowerContext。

### 启动 Dify

启动全部容器。

```bash
cd {DIFY_DIR}/docker
docker compose up -d
```

首次启动需要拉取镜像并初始化数据库，等待几分钟。

### 4初始化管理员

打开 `localhost`，按页面提示创建管理员账号。

### 安装 MiniMax 插件

> [!TIP]
> MiniMax 只是示例模型。应用里的 LLM 节点可以换成任意已在 Dify 中配置好的对话模型，例如 OpenAI、Anthropic、Qwen、DeepSeek 等。
>
> 更换后需要：
> - 在每个 LLM 节点重新选择模型；
> - 检查**矛盾判定**节点是否仍能稳定输出 JSON；
> - 必要时删除 DSL 中对 MiniMax 插件的依赖；

在 Dify 的插件市场中搜索 `MiniMax`，安装 `langgenius/minimax` 0.0.29。

DSL 中已经声明该插件，导入后如果提示缺少插件，按提示安装同一版本即可。

### 导入应用

在 Dify 中进入**应用**页面，使用工程中的：

```text
{REPO}/ifpkg/PlayAlong.ifpkg
```

### 记录 API Key

进入导入后的应用，打开 **API Access**，创建并复制 API Key。它对应后文的 `DIFY_API_KEY`。

## 部署 PowerContext

### 1安装 uv

安装 Python 包管理工具 uv。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 安装 PowerContext

安装 PowerContext 1.4.0，包含 CLI、服务端和 SeekDB 支持。

```bash
uv tool install "powercontext[cli,server]==1.4.0"
powercontext --version
```

### 初始化配置

创建配置目录并生成 `.env`。

```bash
mkdir -p {PC_DIR}
cd {PC_DIR}
powercontext config init --language zh --output .env
```

初始化时选择：

- 存储：嵌入式 SeekDB；
- 使用范围：仅当前机器；
- 记忆类型：基础记忆；
- Agent 配置：跳过。

### 允许 Dify 容器访问

编辑 `{PC_DIR}/.env`，让服务监听所有网卡：

```dotenv
POWERCONTEXT_SERVER_HTTP_HOST=0.0.0.0
```

同一文件中找到并记录：

```dotenv
POWERCONTEXT_SERVER_AUTH_TOKEN=<token>
```

这个值对应后文的 `PC_TOKEN`。

### 启动服务

启动 PowerContext，保持这个终端运行。

```bash
cd {PC_DIR}
powercontext server run --env-file .env
```

默认监听 `17429` 端口。

## 写入案卷

### 准备前端配置

复制配置模板。

```powershell
cd {REPO}
Copy-Item .env.example .env
```

填写 PowerContext 地址与 Token：

```dotenv
PC_URL=http://127.0.0.1:17429
PC_TOKEN=<与 POWERCONTEXT_SERVER_AUTH_TOKEN 相同>
```

### 执行案卷写入

校验案卷并写入 PowerContext。

```powershell
python {REPO}\scripts\seed_cases.py
```

脚本会：

- 创建或复用一个案卷库 scope；
- 写入 `cases/json/` 下的全部案卷；
- 把生成的 `scope_id` 写回 `.env` 的 `PC_CASE_SCOPE`。

记录输出中的 scope：

```text
PC_CASE_SCOPE=scp_xxxxxxxxxxxxxxxx
```

Dify 中的 `PC_SCOPE` 必须与这个值一致。

## 配置并启动前端

### 1填写前端配置

`.env` 中补齐 Dify 相关配置：

```dotenv
DIFY_API_BASE=http://127.0.0.1/v1
DIFY_API_KEY=app-xxxxxxxx
```

`PC_CASE_SCOPE` 由 seed 自动写入，不需要手动填。

### 启动本地服务

启动前端与代理，保持终端运行。

```powershell
python {REPO}\web\server.py
```

默认监听 `8787`。

### 打开页面

浏览器访问：

```text
http://127.0.0.1:8787
```

## 配置 Dify 应用环境变量

回到 Dify 应用，在**环境变量**中填入：

```text
PC_URL   = http://host.docker.internal:17429
PC_TOKEN = <与 POWERCONTEXT_SERVER_AUTH_TOKEN 相同>
PC_SCOPE = <seed 输出的 scope_id>
```

保存后，在 Dify 中新建对话测试一次，确认能够返回开场白。

## 常见问题

### Dify 无法连接 PowerContext

确认：

- PowerContext 监听 `0.0.0.0`；
- `docker-compose.yaml` 已加 `host.docker.internal:host-gateway`；
- 容器内访问 `http://host.docker.internal:17429` 可达。

### Dify 报 404 或读取不到案卷

`PC_SCOPE` 与 `PC_CASE_SCOPE` 不一致。重新执行 seed，把新的 scope 同步到 Dify。

### 前端返回 401

`DIFY_API_KEY` 不完整或已失效。重新在应用的 API Access 页面生成。

### 页面没有样式

`web/assets/css/app.css` 缺失。该文件已随仓库提供，不需要自行构建。
