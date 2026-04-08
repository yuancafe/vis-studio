# Changelog

[English](#english) | [中文](#中文)

## English

### 1.3 - Current release

- Rewrote the README so the public repository now reflects the actual bundle scope instead of an earlier packaging snapshot.
- Added a stricter discovery-intake behavior: the suite should now explicitly check whether business context, audience, competitors, current assets, and intended deliverables are present before moving forward.
- Added clearer guidance that the opening phase should pause and ask 1-3 targeted questions when critical inputs are missing instead of silently assuming them.
- Clarified that rich upfront materials may reduce or eliminate intake questions, which is expected behavior rather than a workflow gap.

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
- Added the machine-readable `brand-pack` and brand-specific wrapper skill model.
- Added 30 structured style playbooks to make direction selection and downstream solutioning more consistent.
- Added a VIS-oriented design markdown layer so the suite can produce `REFERENCE_STYLE_DISTILLATION.md`, `BRAND_FOUNDATION_DESIGN.md`, `UI_UX_DESIGN.md`, `APPLICATION_DESIGN.md`, and `DESIGN_INDEX.md` for downstream design tools.
- Added an explicit reference-style distillation workflow so multiple benchmark brands can be synthesized into original identity direction instead of copied literally.
- Expanded wrapper generation so the suite can produce both `<brand-slug>-brand-applications` and `<brand-slug>-brand-guidelines`.
- Added tool-adapter contracts for Figma MCP, Stitch, Pencil, Adobe Illustrator, Adobe Photoshop, Canva, Inkscape, and image-generation model workflows.
- Added standard prompt skeletons for each supported tool so teams can invoke design tools and image models with a consistent structure.
- Upgraded wrapper generation so it now auto-builds brand-specific prompt files for each supported tool instead of only pointing to generic skeleton references.
- Integrated reusable methodology from the local `visual-identity-direction` skill into discovery, concept exploration, and foundation design guidance.

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

### 1.3 - 当前发布版

- 重写了 README，让公开仓库首页真正反映当前 bundle 的能力范围，而不再停留在较早期的打包说明状态。
- 新增更严格的 discovery intake 机制：在继续推进前，先显式检查 business context、audience、competitors、current assets 和 deliverables 是否齐全。
- 补充更明确的追问规则：当关键信息缺失时，前期阶段应暂停并先追问 1-3 个关键问题，而不是默认直接假设。
- 明确说明：如果用户一开始提供的资料已经足够完整，那么前期问题会减少甚至不再追问，这是预期行为，不是流程缺失。

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
- 引入 machine-readable 的 `brand-pack` 与品牌专属 wrapper skill 模型。
- 增加 30 套结构化 style playbooks，让方向收敛和后续 solution 更稳定。
- 新增面向 VIS 的 design markdown 输出层，可产出 `REFERENCE_STYLE_DISTILLATION.md`、`BRAND_FOUNDATION_DESIGN.md`、`UI_UX_DESIGN.md`、`APPLICATION_DESIGN.md`、`DESIGN_INDEX.md`，供下游设计工具读取。
- 新增参考风格提炼方法，把多个参考品牌收敛成原创方向，而不是直接拼接模仿。
- 扩展 wrapper 生成链路，可同时产出 `<brand-slug>-brand-applications` 和 `<brand-slug>-brand-guidelines`。
- 新增工具适配层，覆盖 Figma MCP、Stitch、Pencil、Adobe Illustrator、Adobe Photoshop、Canva、Inkscape 和文生图模型工作流。
- 新增每种工具的标准 prompt skeleton，方便后续稳定调用设计工具和生成模型。
- 升级 wrapper 生成链路，现在会自动产出各工具的品牌专属 prompt 文件，而不只是指向通用 skeleton 参考。
- 把本地 `visual-identity-direction` skill 中可复用的方法论并入 discovery、concept 和 foundation 阶段。

### 1.1 - 中期收敛版本

- 把技能套件收敛成更清晰的 4 步公开流程。
- 保留 discovery、concept exploration、identity production、governance 作为主阶段。
- 加强 strategy 和 system design 之间的交接逻辑。
- 开始明确核心身份与后续包装之间的边界。

### 1.0 - 初始原型版本

- 从最初的原型技能家族开始。
- 重点是品牌策略基础、资产盘点、规范构建和视觉识别系统思维。
- 当时还是更小的独立技能集合，后来才逐步收敛成 v2 和 v3 的体系。
