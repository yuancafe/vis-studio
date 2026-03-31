# Brand Identity Design Skills

[English](#english) | [中文](#中文)

## English

Brand Identity Design Skills is a reusable bundle for full brand identity engagements. It turns the current VIS workflow into a structured package that covers the full path from discovery to governance, including the application-production phase that studio work usually treats as a separate layer.

### What this package is for

- Diagnose a brand project and choose the right route
- Narrow visual directions with structured playbooks
- Produce the core identity system
- Expand the identity into applications and touchpoints
- Package everything into a reusable `brand-pack` and brand-specific wrapper skill

### What is included

Public skills in this bundle:

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

Supporting internal skills:

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`

Package references:

- `references/V3_ARCHITECTURE.md`
- `references/PROCESS_SYNTHESIS.md`

Support assets and scripts:

- `support/brand-style-playbook-selector/assets/brand_style_playbooks.json`
- `support/brand-style-playbook-selector/assets/sample_brand_brief.json`
- `support/brand-style-playbook-selector/scripts/select_playbooks.py`
- `support/application-scope-planner/assets/sample_application_request.json`
- `support/application-scope-planner/assets/starter_bundles.json`
- `support/application-scope-planner/scripts/build_scope_matrix.py`
- `support/application-route-classifier/scripts/classify_routes.py`
- `support/application-template-factory/references/template-output-contract.md`
- `support/application-mockup-composer/references/mockup-output-contract.md`
- `support/brand-application-factory/assets/sample_brand_foundation.json`
- `support/brand-application-factory/assets/wrapper_skill_template.md`
- `support/brand-application-factory/scripts/build_brand_pack.py`
- `support/brand-application-factory/scripts/generate_wrapper_skill.py`

### How the flow works

1. `brand-discovery-strategy` gathers context, audits existing assets, and frames the scope.
2. `visual-concept-exploration` narrows style territories and selects the strongest directions.
3. `identity-system-production` builds the core identity system and the first machine-readable `brand-pack`.
4. `brand-application-system` turns the identity into scoped application bundles, recipes, and production routes.
5. `brand-governance-rollout` finalizes the pack, governance rules, asset manifest, and handoff.

### Why the application phase is separate

Application work is not just "more design." It is a different production layer with its own scope logic, route logic, and output logic. This package keeps that layer explicit so teams can handle 5 items, 20 items, or 100+ items without flattening everything into one vague deliverable.

### Package notes

- The package is designed to be installable into a local skills directory, but the public repository keeps paths generic.
- The repository includes the reusable skills, the support layer, and the package-level documentation.
- Version history is tracked in `CHANGELOG.md`; this repo release corresponds to the current bundled release line.

### Notes

- Illustrator-heavy work is still treated as `manual_vector`.
- Canva-friendly work can be routed through template workflows.
- Photoshop-friendly work can be routed through mockup workflows.
- The `brand-pack` is the source of truth for downstream automation.

## 中文

Brand Identity Design Skills 是一个可复用的品牌视觉识别技能包。它把当前 VIS 流程整理成一个结构化套件，覆盖从诊断、概念探索、基础系统生产，到应用生产和治理交付的完整链路，并把 studio 里常常单独处理的 application 阶段明确拆出来。

### 这个技能包是做什么的

- 诊断品牌项目并判断正确路径
- 用结构化 playbook 收敛视觉方向
- 产出核心身份系统
- 把身份系统扩展成各类应用物料和触点
- 把所有内容封装成可复用的 `brand-pack` 和品牌专属 wrapper skill

### 包含什么

公开技能：

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

包内参考文档：

- `references/V3_ARCHITECTURE.md`
- `references/PROCESS_SYNTHESIS.md`

支持性资产和脚本：

- `support/brand-style-playbook-selector/assets/brand_style_playbooks.json`
- `support/brand-style-playbook-selector/assets/sample_brand_brief.json`
- `support/brand-style-playbook-selector/scripts/select_playbooks.py`
- `support/application-scope-planner/assets/sample_application_request.json`
- `support/application-scope-planner/assets/starter_bundles.json`
- `support/application-scope-planner/scripts/build_scope_matrix.py`
- `support/application-route-classifier/scripts/classify_routes.py`
- `support/application-template-factory/references/template-output-contract.md`
- `support/application-mockup-composer/references/mockup-output-contract.md`
- `support/brand-application-factory/assets/sample_brand_foundation.json`
- `support/brand-application-factory/assets/wrapper_skill_template.md`
- `support/brand-application-factory/scripts/build_brand_pack.py`
- `support/brand-application-factory/scripts/generate_wrapper_skill.py`

支持性内部技能：

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`

### 工作流怎么走

1. `brand-discovery-strategy` 做背景诊断、资产盘点和范围判断。
2. `visual-concept-exploration` 用 style playbook 收敛方向。
3. `identity-system-production` 生产核心识别系统和第一版机器可读 `brand-pack`。
4. `brand-application-system` 把身份系统转成应用包、应用 recipe 和生产路线。
5. `brand-governance-rollout` 完成 brand-pack、治理规则、资产清单和交付。

### 为什么要单独分出 application 阶段

Application 不是“多做一点设计”，而是另一层生产系统，拥有独立的范围逻辑、路由逻辑和输出逻辑。把这一层单独拆开后，才能稳定处理 5 项、20 项，甚至 100+ 项的应用需求，而不会把所有内容压成一个模糊交付。

### 包说明

- 公开仓库不会写入本地绝对路径。
- 本地安装由技能管理流程完成，仓库只保留可复用的内容和说明。
- 版本历史记录在 `CHANGELOG.md`，当前对应的是 bundle 的最新发布线。

### 说明

- Illustrator 重型工作仍然按 `manual_vector` 处理。
- 适合 Canva 的内容走模板路线。
- 适合 Photoshop 的内容走样机路线。
- `brand-pack` 是后续自动化的唯一事实来源。
