<a id="readme-top"></a>

[简体中文](./README.md) |
English

<div align="center">

  <h3 align="center">PlayAlong</h3>
  <p align="center">
    The Mini interactive narrative and Role-playing Game, built with Dify ChatFlow and PowerContext
    <br /><br />
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=bug&template=bug-report.md">
      <strong>» Report Bug</strong>
    </a>
    <a href="https://github.com/Fooxygen/PlayAlong/issues/new?labels=enhancement&template=feature-request.md">
      <strong>» Request Feature</strong>
    </a>
  </p>

</div>

## About

PlayAlong is an interactive narrative and role-playing game. You take the place of a missing person and face everyone who knew him, using nothing but his incomplete memories.

A session includes:

- choosing a case from the case library;
- talking to a series of people who know him;
- recalling his memories a limited number of times;
- filling the gaps with invented answers;
- seeing, at the end, which memories were his and which ones you made up.

The flow is orchestrated in Dify. Cases, dialogue records and memories are stored in PowerContext. See the documents linked below for setup and verification.

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
| `cases/` | Case source text and case structure text |
| `docs/` | Dependency, run, verification, case structure prompt and case authoring guides |
| `ifpkg/` | Dify app package |
| `scripts/` | Case validation and seeding |
| `web/` | Frontend, backend and assets |

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

## Quick start

- Read `docs/deps.md` for the runtime dependencies;
- Read `docs/run.md` for configuration and startup;
- Read `docs/verify.md` for the verification steps;
- Use `docs/case_struct.md` when an Agent converts case source text to case structure text;
- Read `docs/case_add.md` to design your own case;

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

## License

Copyright (c) 2026 Fooxygen. With BaseTUT. Licensed under the [MIT License](LICENSE).

<p align="right"><a href="#readme-top">↑ Back to top</a></p>
