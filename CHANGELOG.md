# Changelog

[English](#english) | [中文](#中文)

## English

### 2.2.1 - Current release (Swarm-compatible production hardening)

- Upgraded production gateway routing with explicit CLI discovery support for `pencil` executor:
  - added CLI catalog probing (`open-pencil --help`, `bun open-pencil --help`)
  - added `installed_clis` into MCP discovery report output
  - marked executor app-cli availability from both local app installs and CLI probes
- Added Open Pencil adaptation path in production execution:
  - `app-cli` gateway now prioritizes CLI probe results when available
  - production run records CLI routing metadata (`cli_id`, `cli_command`, probe trace)
  - when `pencil` is selected via `app-cli`, orchestration now attempts direct Open Pencil CLI execution before file packaging
- Improved fallback diagnostics:
  - app-cli probe failures are now classified and written into gateway metadata
  - setup suggestions now include Open Pencil installation guidance for `pencil` critical paths
- Version marker updates:
  - production-generated AI/placeholder assets now mark VIS STUDIO `2.2.1`

### 2.1 - Dual-mode orchestration release

- Added dual run modes for orchestration:
  - `document` mode for plan/payload output only
  - `production` mode for post-document execution orchestration
- Added new orchestration scripts:
  - `scripts/discover_mcp_servers.py`
  - `scripts/build_pipeline.py`
  - `scripts/run_orchestration.py`
- Added MCP auto-discovery from two sources:
  - `~/.codex/config.toml`
  - `~/.config/mcp/config.json`
- Added production run artifacts:
  - `MCP_DISCOVERY_REPORT.json`
  - `RUN_MANIFEST.json`
  - `RUN_LOG.md`
  - `ARTIFACT_REGISTRY.json`
- Added route metadata extensions:
  - `critical`
  - `executor_candidates`
  - `default_family`
  - `input_artifact_types`
  - `output_artifact_types`
- Extended `TOOL_EXECUTION_PAYLOAD.json` with production fields:
  - `run_mode`
  - `production_scope`
  - `fallback_policy.figma_connector`
  - `executor_candidates`
  - `selected_executor`
  - `dependency_inputs`
  - `output_family_dir`
  - `decision_timeout_seconds`
  - `fallback_trace`
- Added production failure policy:
  - non-critical tasks continue on failure
  - critical tasks prompt `retry/skip/stop` with timeout fallback
- Added per-task dependency chaining so downstream task prompts can consume upstream artifact paths automatically.

### 2.0 - Orchestration foundation release

- Added a new post-packaging orchestration support skill: `brand-production-orchestrator`.
- Added route contracts and execution mapping for:
  - `vis_handbook`
  - `logo_refinement`
  - `visual_asset_system`
  - `packaging_mockup`
  - `social_template_pack`
  - `landing_page_visual_system`
  - `ui_screen_system`
  - `open_source_vector_refinement`
- Added orchestration assets:
  - `assets/route-rules.yaml`
  - `assets/route-rules.json`
  - `assets/execution-plan-template.md`
  - `assets/tool-execution-payload.schema.json`
  - `assets/tool-prompt-templates/*`
- Added orchestration scripts:
  - `scripts/select_route.py`
  - `scripts/build_execution_plan.py`
  - `scripts/build_tool_execution_payload.py`
  - `scripts/render_tool_prompt.py`
  - `scripts/_orchestration_utils.py`
- Added two standard orchestration outputs:
  - `EXECUTION_PLAN.md`
  - `TOOL_EXECUTION_PAYLOAD.json`
- Repositioned VIS STUDIO from only a skill suite to a production orchestration layer after packaging.
- Updated root docs (`SKILL.md`, `README.md`) so 2.0 orchestration is reflected in product messaging and capability lists.

### 1.6 - Naming and narrative release

- Renamed the suite identity from `brand-identity-design-skills` to `VIS STUDIO` with `vis-studio` as the technical skill name.
- Reframed the README with a stronger product-facing narrative so the repository is easier to understand, share, and present publicly.

### 1.5 - Methodology and intake release

- Integrated reusable methodology from the local `visual-identity-direction` skill into discovery, concept exploration, and foundation design guidance.
- Added a stricter discovery-intake behavior: the suite should now explicitly check whether business context, audience, competitors, current assets, and intended deliverables are present before moving forward.
- Added clearer guidance that the opening phase should pause and ask 1-3 targeted questions when critical inputs are missing instead of silently assuming them.
- Clarified that rich upfront materials may reduce or eliminate intake questions, which is expected behavior rather than a workflow gap.
- Rewrote the README so the public repository now reflects the actual bundle scope instead of an earlier packaging snapshot.

### 1.4 - Tool prompt system release

- Added tool-adapter contracts for Figma MCP, Stitch, Pencil, Adobe Illustrator, Adobe Photoshop, Canva, Inkscape, and image-generation model workflows.
- Added standard prompt skeletons for each supported tool so teams can invoke design tools and image models with a consistent structure.
- Upgraded wrapper generation so it now auto-builds brand-specific prompt files for each supported tool instead of only pointing to generic skeleton references.

### 1.3 - Wrapper expansion release

- Expanded wrapper generation so the suite can produce both `<brand-slug>-brand-applications` and `<brand-slug>-brand-guidelines`.
- Strengthened the downstream brand-usage layer so future sessions can apply the approved identity system directly through thin wrapper skills.

### 1.2 - VIS system release

- Split application production into a dedicated `brand-application-system`.
- Added the 5 public v3 skills:
  - `brand-discovery-strategy`
  - `visual-concept-exploration`
  - `identity-system-production`
  - `brand-application-system`
  - `brand-governance-rollout`
- Added the support layer:
  - style playbook selector
  - scope planner
  - route classifier
  - template factory
  - mockup composer
  - brand application factory
- Added the machine-readable `brand-pack` as the reusable downstream source of truth.
- Added 30 structured style playbooks to make direction selection and downstream solutioning more consistent.
- Added a VIS-oriented design markdown layer so the suite can produce `REFERENCE_STYLE_DISTILLATION.md`, `BRAND_FOUNDATION_DESIGN.md`, `UI_UX_DESIGN.md`, `APPLICATION_DESIGN.md`, and `DESIGN_INDEX.md` for downstream design tools.
- Added an explicit reference-style distillation workflow so multiple benchmark brands can be synthesized into original identity direction instead of copied literally.

### 1.1 - Intermediate consolidation

- Consolidated the suite into a cleaner 4-skill public flow.
- Kept discovery, concept exploration, identity production, and governance as the main phases.
- Improved the handoff logic between strategy and system design.
- Introduced stronger separation between core identity thinking and later packaging.

### 1.0 - Initial prototype

- Started with the original prototype skill family.
- Focused on brand strategy foundation, asset audit, guideline building, and visual identity system thinking.
- Treated the workflow as a smaller set of standalone skills before the v2 and v3 consolidation work.

## 中文

### 2.2.1 - 当前发布版（Swarm 兼容与 CLI 强化）

- 生产网关新增 `pencil` 执行器的 CLI 探测与路由能力：
  - 增加 CLI 探测目录（`open-pencil --help`、`bun open-pencil --help`）
  - 在 MCP 发现结果中新增 `installed_clis`
  - `app-cli` 可用性由“本地 App 安装”扩展为“App 或 CLI 任一可用”
- 新增 Open Pencil 执行适配：
  - `app-cli` 网关优先使用 CLI 探测命中结果
  - 产线元数据记录 CLI 路由信息（`cli_id`、`cli_command`、probe 轨迹）
  - 当 `pencil` 通过 `app-cli` 选中时，先尝试真实 Open Pencil CLI 执行，再进入文件打包
- 容错与诊断增强：
  - app-cli 探测失败会进行错误分类并写入 gateway 元数据
  - `pencil` 关键链路缺失时，setup 建议中补充 Open Pencil 安装指引
- 版本标记更新：
  - 生成的 AI/占位资产版本标记升级为 VIS STUDIO `2.2.1`

### 2.1 - 双模式 Orchestration 发布版

- 新增双模式编排：
  - `document` 模式只产出 plan/payload
  - `production` 模式在文档之后继续执行自动化编排
- 新增编排脚本：
  - `scripts/discover_mcp_servers.py`
  - `scripts/build_pipeline.py`
  - `scripts/run_orchestration.py`
- 新增双源 MCP 自动发现：
  - `~/.codex/config.toml`
  - `~/.config/mcp/config.json`
- 新增 production run 产物：
  - `MCP_DISCOVERY_REPORT.json`
  - `RUN_MANIFEST.json`
  - `RUN_LOG.md`
  - `ARTIFACT_REGISTRY.json`
- 路由规则新增字段：
  - `critical`
  - `executor_candidates`
  - `default_family`
  - `input_artifact_types`
  - `output_artifact_types`
- `TOOL_EXECUTION_PAYLOAD.json` 扩展字段：
  - `run_mode`
  - `production_scope`
  - `fallback_policy.figma_connector`
  - `executor_candidates`
  - `selected_executor`
  - `dependency_inputs`
  - `output_family_dir`
  - `decision_timeout_seconds`
  - `fallback_trace`
- 新增失败策略：
  - 非关键任务失败继续
  - 关键任务失败触发 `retry/skip/stop`，超时走默认策略
- 新增任务依赖注入机制：后序任务可自动读取前序产物路径并写入执行上下文。

### 2.0 - Orchestration 基础发布版

- 新增 packaging 之后的 orchestration 支撑技能：`brand-production-orchestrator`。
- 新增路由合同与执行映射，覆盖：
  - `vis_handbook`
  - `logo_refinement`
  - `visual_asset_system`
  - `packaging_mockup`
  - `social_template_pack`
  - `landing_page_visual_system`
  - `ui_screen_system`
  - `open_source_vector_refinement`
- 新增 orchestration 资产层：
  - `assets/route-rules.yaml`
  - `assets/route-rules.json`
  - `assets/execution-plan-template.md`
  - `assets/tool-execution-payload.schema.json`
  - `assets/tool-prompt-templates/*`
- 新增 orchestration 脚本层：
  - `scripts/select_route.py`
  - `scripts/build_execution_plan.py`
  - `scripts/build_tool_execution_payload.py`
  - `scripts/render_tool_prompt.py`
  - `scripts/_orchestration_utils.py`
- 新增两类标准编排产物：
  - `EXECUTION_PLAN.md`
  - `TOOL_EXECUTION_PAYLOAD.json`
- 将 VIS STUDIO 从仅 skill suite 的定位升级为 packaging 后可执行的生产编排层。
- 更新根文档（`SKILL.md`、`README.md`），让 2.0 orchestration 能力在对外描述中可见。

### 1.6 - 命名与叙事发布版

- 将套件名称从 `brand-identity-design-skills` 调整为 `VIS STUDIO`，并把技术名统一为 `vis-studio`。
- 重写 README 的对外叙事方式，让仓库首页更像产品主页，更适合公开传播和介绍。

### 1.5 - 方法论与 intake 发布版

- 把本地 `visual-identity-direction` skill 中可复用的方法论并入 discovery、concept 和 foundation 阶段。
- 新增更严格的 discovery intake 机制：在继续推进前，先显式检查 business context、audience、competitors、current assets 和 deliverables 是否齐全。
- 补充更明确的追问规则：当关键信息缺失时，前期阶段应暂停并先追问 1-3 个关键问题，而不是默认直接假设。
- 明确说明：如果用户一开始提供的资料已经足够完整，那么前期问题会减少甚至不再追问，这是预期行为，不是流程缺失。
- 重写了 README，让公开仓库首页真正反映当前 bundle 的能力范围，而不再停留在较早期的打包说明状态。

### 1.4 - 工具 prompt 系统发布版

- 新增工具适配层，覆盖 Figma MCP、Stitch、Pencil、Adobe Illustrator、Adobe Photoshop、Canva、Inkscape 和文生图模型工作流。
- 新增每种工具的标准 prompt skeleton，方便后续稳定调用设计工具和生成模型。
- 升级 wrapper 生成链路，现在会自动产出各工具的品牌专属 prompt 文件，而不只是指向通用 skeleton 参考。

### 1.3 - Wrapper 扩展发布版

- 扩展 wrapper 生成链路，可同时产出 `<brand-slug>-brand-applications` 和 `<brand-slug>-brand-guidelines`。
- 强化下游品牌调用层，让后续会话可以通过轻量 wrapper 直接应用已批准的识别系统。

### 1.2 - VIS 系统发布版

- 把 application production 单独拆成 `brand-application-system`。
- 新增 5 个公开 v3 技能：
  - `brand-discovery-strategy`
  - `visual-concept-exploration`
  - `identity-system-production`
  - `brand-application-system`
  - `brand-governance-rollout`
- 新增支撑层：
  - style playbook selector
  - scope planner
  - route classifier
  - template factory
  - mockup composer
  - brand application factory
- 引入 machine-readable 的 `brand-pack`，作为后续自动化的可复用事实来源。
- 增加 30 套结构化 style playbooks，让方向收敛和后续 solution 更稳定。
- 新增面向 VIS 的 design markdown 输出层，可产出 `REFERENCE_STYLE_DISTILLATION.md`、`BRAND_FOUNDATION_DESIGN.md`、`UI_UX_DESIGN.md`、`APPLICATION_DESIGN.md`、`DESIGN_INDEX.md`，供下游设计工具读取。
- 新增参考风格提炼方法，把多个参考品牌收敛成原创方向，而不是直接拼接模仿。

### 1.1 - 中期收敛版本

- 把技能套件收敛成更清晰的 4 步公开流程。
- 保留 discovery、concept exploration、identity production、governance 作为主阶段。
- 加强 strategy 和 system design 之间的交接逻辑。
- 开始明确核心身份与后续包装之间的边界。

### 1.0 - 初始原型版本

- 从最初的原型技能家族开始。
- 重点是品牌策略基础、资产盘点、规范构建和视觉识别系统思维。
- 当时还是更小的独立技能集合，后来才逐步收敛成 v2 和 v3 的体系。
