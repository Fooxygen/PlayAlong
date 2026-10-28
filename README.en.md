<a id="readme-top"></a>

[简体中文](./README.md) |
English

<div align="center">

  <!-- TODO: replace with the final logo -->
  <img src="docs/images/brand_playalong.svg" alt="PlayAlong" style="margin=0">
  <h3 align="center">PlayAlong</h3>
  <p align="center">
    You take the place of a missing person, with nothing but his incomplete memories.
    <br /><br />
    <a href="https://github.com/Fooxygen/PlayAlong">
      <strong>» Read Wiki</strong>
    </a>
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=bug">
      <strong>» Report an issue</strong>
    </a>
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=enhancement">
      <strong>» Request a feature</strong>
    </a>
  </p>

</div>

## About

PlayAlong is an interactive narrative and role-playing game. You take the place of a missing person and face everyone who knew him, using nothing but his incomplete memories.

One session includes:

- choosing a case from the case library;
- talking to a series of people who know him;
- recalling his memories a limited number of times;
- filling the gaps with invented answers;
- seeing, at the end, which memories were his and which ones you made up.

The flow is orchestrated in Dify. Cases, dialogue records and memories are stored in PowerContext. To run the project, see **Documents** and **Configuration and startup** below.

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## Gameplay

| Stage | Task |
| - | - |
| Choose a case | Read case summaries from the case library |
| Conversation | People appear one by one and question the player |
| Recall | Spend limited attempts to reveal one memory at a time |
| Judgment | Check whether an answer passes and whether it contradicts earlier claims |
| Ending | List the real memories, the invented ones and a review |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## Repository layout

| Directory | Content |
| - | - |
| `cases/` | Case sources (Markdown) and runtime data (JSON) |
| `docs/` | Dependencies, configuration, startup and verification |
| `ifpkg/` | `PlayAlong.ifpkg`, Dify app package |
| `scripts/` | `seed_cases.py`, case validation and PowerContext seeding |
| `web/` | `index.html`, `server.py` and frontend assets |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## Stack

| Category | Technology | Version |
| - | - | - |
| Orchestration | Dify | 1.18.0 |
| Memory and context | PowerContext | 1.4.0 |
| Model service | MiniMax plugin | 0.0.29 |
| Frontend | Plain HTML / CSS / JavaScript | - |
| Local service | Python | 3.12+ |

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## Documents

| Document | Content |
| - | - |
| [`docs/deps.md`](./docs/deps.md) | Runtime environment, software and plugin versions |
| [`docs/configure.md`](./docs/configure.md) | PowerContext, Dify and frontend configuration |
| [`docs/run.md`](./docs/run.md) | DSL import, data initialization and startup |

> The documents are written in Chinese.

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## Configuration and startup

> See [`docs/run.md`](./docs/run.md) for the full setup.

```text
1. Initialize PowerContext and seed the cases
2. Import the Dify app from ifpkg/
3. Configure the Dify environment variables
4. Start the local frontend
```

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## License

Copyright (c) 2026 Fooxygen. Licensed under the [MIT License](LICENSE).

<p align="right"><a href="#readme-top">↑ Back to top</a></p>
