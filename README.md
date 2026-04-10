# VIS STUDIO

[English](#english) | [中文](#中文)

## English

VIS STUDIO is an AI-native operating system for brand identity and visual identity system work.

It helps teams move from messy inputs to a reusable brand system that AI can actually follow: strategy, visual direction, identity system, applications, governance, wrappers, adapters, and brand-specific prompts.

This is not just a prompt pack.
This is not just a logo workflow.
This is not just a UI `DESIGN.md`.

VIS STUDIO is built for full VIS work.

### New in 2.2.1: Order-Driven Production + Swarm-Compatible Gateway

VIS STUDIO now includes a post-packaging orchestration layer with two run modes:

- `document` mode: generate plan and payload artifacts and stop.
- `production` mode: continue after docs, auto-discover local design MCP services, execute route pipelines, and package outputs by application family.

It can:

- detect production intent from a concrete request
- select a route and primary tool
- assemble source-of-truth documents per route
- generate `EXECUTION_PLAN.md`
- generate `TOOL_EXECUTION_PAYLOAD.json`
- prepare tool-specific prompts for handoff or direct execution
- generate `MCP_DISCOVERY_REPORT.json` in production runs
- generate `RUN_MANIFEST.json`, `RUN_LOG.md`, and `ARTIFACT_REGISTRY.json` for end-to-end production tracking
- route through hybrid gateway (`direct -> swarm-managed -> app-cli`) with `mcp-swarm` compatibility
- detect CLI executors (including Open Pencil for `pencil` route candidates) and record gateway trace details

### What VIS STUDIO is

VIS STUDIO turns brand work into a structured production system:

- discovery and strategic diagnosis
- reference distillation instead of reference copying
- concept exploration and territory narrowing
- identity-system production
- application-system planning and routing
- governance handoff and downstream reuse

It packages the result into machine-readable outputs so AI tools can work inside the approved system instead of improvising from vague style language.

### Why it exists

Most AI design workflows break in the same place:

- strategy is missing
- references are copied instead of distilled
- application work is treated as an afterthought
- tools are prompted inconsistently
- every new asset restarts from zero

VIS STUDIO solves that by making the brand system explicit, reusable, and automation-ready.

### What it produces

Core design documents:

- `REFERENCE_STYLE_DISTILLATION.md`
- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `DESIGN_INDEX.md`

Machine-readable packaging:

- `brand_pack.json`
- `EXECUTION_PLAN.md`
- `TOOL_EXECUTION_PAYLOAD.json`

Reusable downstream wrappers:

- `<brand-slug>-brand-applications`
- `<brand-slug>-brand-guidelines`

Tool-enablement layer:

- `TOOL_ADAPTER_INDEX.md`
- `references/tool-adapters/*.md`
- `TOOL_PROMPT_SKELETON_INDEX.md`
- `references/tool-prompt-skeletons/*.md`

### What gets generated automatically

When a project reaches the packaging stage, VIS STUDIO can automatically generate:

- the final `brand_pack.json`
- a brand-specific applications wrapper
- a brand-specific guidelines wrapper
- bundled tool adapters inside the generated wrapper
- brand-specific prompt files inside the generated wrapper

Those brand-specific prompt files currently support:

- Figma MCP
- Stitch
- Pencil
- Adobe Illustrator
- Adobe Photoshop
- Canva
- Inkscape
- image-generation models such as Doubao, Kling, Nano Banana, and similar tools

### Workflow

1. `brand-discovery-strategy`
   Diagnose the route, check input completeness, ask targeted questions when critical information is missing, and build the strategic base.
2. `visual-concept-exploration`
   Distill references, translate strategy into visual territories, and narrow direction.
3. `identity-system-production`
   Build the identity core and first structured brand payload.
4. `brand-application-system`
   Convert the identity into application families, routes, and production logic.
5. `brand-governance-rollout`
   Finalize governance, packaging, and downstream reuse.

### What makes it different

- It treats VIS as a system, not a one-off design exercise.
- It separates identity production from application production.
- It forces reference distillation before visual execution.
- It supports targeted intake questions when inputs are incomplete.
- It creates outputs that downstream AI tools can reliably consume.
- It includes both generic tool skeletons and brand-specific prompt generation.

### Methodology inside the system

VIS STUDIO also incorporates useful methods from the local `visual-identity-direction` skill, including:

- strategy-to-visual translation
- creative-brief discipline
- moodboard rationale
- logo-brief structure
- photography direction
- typography and color reasoning

### Public skills

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

### Support skills

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`
- `brand-production-orchestrator`

### Orchestration routes (2.1)

- `vis_handbook`
- `logo_refinement`
- `visual_asset_system`
- `packaging_mockup`
- `social_template_pack`
- `landing_page_visual_system`
- `ui_screen_system`
- `open_source_vector_refinement`

### Repository structure

- `skills/`
  Public VIS workflow skills
- `support/`
  Internal support skills for routing, packaging, and production logic
- `references/`
  Shared architecture notes, adapters, and prompt system references
- `README.md`
  Product overview
- `CHANGELOG.md`
  Release history

### Important notes

- `brand_pack.json` is the downstream source of truth.
- Illustrator-heavy work is still treated as `manual_vector`.
- Canva-friendly work follows template logic.
- Photoshop-friendly work follows mockup logic.
- The wrapper layer is intentionally thin: it applies the approved system, not redefines it.

## 中文

VIS STUDIO 是一套面向品牌识别与视觉识别系统工作的 AI 原生操作系统。

它的目标，是把零散、模糊、依赖设计师个人脑内判断的品牌项目，转成 AI 也能稳定执行的结构化系统：从策略、方向、识别系统、应用扩展、治理交付，到 wrapper、adapter 和品牌专属 prompt，全部纳入同一条生产链。

它不是普通的 prompt 包。
它不是单独的 logo 工作流。
它也不只是一个面向 UI 的 `DESIGN.md` 套件。

VIS STUDIO 面向的是完整 VIS 工作。

### 2.2.1 新增能力：订单驱动生产编排 + Swarm 兼容网关

VIS STUDIO 在 packaging 之后增加了双模式 orchestration：

- `document` 模式：输出文档与执行 payload 后结束。
- `production` 模式：文档生成后继续自动发现本地设计 MCP、按路由执行流水线、并按应用家族打包交付。

它可以：

- 从具体生产需求自动识别 intent
- 自动选择 route 与 primary tool
- 按 route 装配 source-of-truth 文档
- 生成 `EXECUTION_PLAN.md`
- 生成 `TOOL_EXECUTION_PAYLOAD.json`
- 生成按工具定制的执行 prompt（handoff 或 execute）
- 在 production run 中输出 `MCP_DISCOVERY_REPORT.json`
- 在 production run 中输出 `RUN_MANIFEST.json`、`RUN_LOG.md`、`ARTIFACT_REGISTRY.json`
- 通过混合网关执行（`direct -> swarm-managed -> app-cli`），兼容 `mcp-swarm` 场景
- 支持 CLI 执行器探测（含 `pencil` 的 Open Pencil CLI）并记录完整 gateway trace

### VIS STUDIO 是什么

VIS STUDIO 把品牌工作变成一套可执行系统：

- discovery 与策略诊断
- 参考风格提炼，而不是照抄参考
- 概念探索与方向收敛
- 识别系统生产
- 应用系统规划与路由
- 治理交接与后续复用

它会把结果封装成机器可读输出，让 AI 工具不再依赖模糊的审美描述，而是依据已批准的品牌系统工作。

### 为什么要做它

大多数 AI 设计流程的问题都出在同几个地方：

- 没有策略基础
- 参考没有提炼，只有拼贴模仿
- application 被当成附属工作
- 不同工具的调用方式不统一
- 每做一个新物料都像重新开局

VIS STUDIO 的作用，就是把品牌系统显式化、可复用化、自动化。

### 它会产出什么

核心设计文件：

- `REFERENCE_STYLE_DISTILLATION.md`
- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `DESIGN_INDEX.md`

机器可读打包层：

- `brand_pack.json`
- `EXECUTION_PLAN.md`
- `TOOL_EXECUTION_PAYLOAD.json`

可复用下游 wrapper：

- `<brand-slug>-brand-applications`
- `<brand-slug>-brand-guidelines`

工具协同层：

- `TOOL_ADAPTER_INDEX.md`
- `references/tool-adapters/*.md`
- `TOOL_PROMPT_SKELETON_INDEX.md`
- `references/tool-prompt-skeletons/*.md`

### 哪些内容会自动生成

当项目走到 packaging 阶段，VIS STUDIO 可以自动生成：

- 最终 `brand_pack.json`
- 品牌专属 applications wrapper
- 品牌专属 guidelines wrapper
- 每个 wrapper 内自带的一套 tool adapters
- 每个 wrapper 内自带的一套品牌专属 prompt 文件

这些品牌专属 prompt 目前支持：

- Figma MCP
- Stitch
- Pencil
- Adobe Illustrator
- Adobe Photoshop
- Canva
- Inkscape
- 文生图模型，如豆包、可灵、Nano Banana 及类似工具

### 工作流

1. `brand-discovery-strategy`
   先判断项目路径，检查输入是否完整；如果关键信息缺失，就先追问，再建立策略基础。
2. `visual-concept-exploration`
   提炼参考风格，把策略翻译成视觉方向，并收敛方案。
3. `identity-system-production`
   构建识别系统核心，并产出第一版结构化品牌数据。
4. `brand-application-system`
   把识别系统扩展成应用家族、生产路线和规模化逻辑。
5. `brand-governance-rollout`
   完成治理、打包和后续复用层。

### 它和普通品牌技能的区别

- 它把 VIS 当成系统，而不是一次性设计任务。
- 它明确区分 identity production 和 application production。
- 它要求先做 reference distillation，再做视觉执行。
- 它支持缺信息时的 targeted intake questions。
- 它会产出 AI 工具可以稳定消费的结构化结果。
- 它同时提供通用 skeleton 和品牌专属 prompt 自动生成。

### 系统内部的方法论

VIS STUDIO 同时吸收了本地 `visual-identity-direction` skill 中有价值的方法，包括：

- strategy-to-visual translation
- creative brief discipline
- moodboard rationale
- logo brief structure
- photography direction
- typography and color reasoning

### 公开技能

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

### 支持技能

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`
- `brand-production-orchestrator`

### 2.1 Orchestration 路由

- `vis_handbook`
- `logo_refinement`
- `visual_asset_system`
- `packaging_mockup`
- `social_template_pack`
- `landing_page_visual_system`
- `ui_screen_system`
- `open_source_vector_refinement`

### 仓库结构

- `skills/`
  公开 VIS 工作流技能
- `support/`
  内部 routing、packaging、production support 技能
- `references/`
  共享架构说明、adapter 和 prompt 系统参考
- `README.md`
  产品化总览
- `CHANGELOG.md`
  发布历史

### 重要说明

- `brand_pack.json` 是后续自动化的事实来源。
- Illustrator 重型工作仍然归为 `manual_vector`。
- 适合 Canva 的内容走模板路线。
- 适合 Photoshop 的内容走样机路线。
- wrapper 层刻意保持轻量，它负责应用已批准系统，而不是重新定义系统。
