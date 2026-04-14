# Pollinations Tier 升级策略

> 更新时间：2026-03-25 01:20

## 一、Tier 级别体系

| Tier | 恢复速率 | 解锁条件 | 日均 Flux 图量 |
|------|---------|---------|-------------|
| 🍄 Spore | 0.01 p/hr | 验证账号 | ~240 张 |
| 🌱 Seed | 0.15 p/hr | 8+ Dev Points（每周自动评估） | ~3,600 张 |
| 🌸 Flower | 10 p/day | 发布 App（需先达到 Seed） | ~10,000 张 |
| 🍯 Nectar | 20 p/day | Coming soon | N/A |

## 二、生图消耗

| 模型 | 消耗/张 | 1 pollen 可生 |
|------|---------|-------------|
| Flux Schnell | 0.001 p | ~1,000 张 |
| Z-Image Turbo | 0.002 p | ~500 张 |

## 三、Dev Points 计算规则（升 Seed 需 ≥ 8pt）

| 指标 | 计分规则 | 上限 |
|------|---------|------|
| 账号年龄 | 0.5pt/月 | max 6pt |
| Public Commits（近90天） | 0.1pt/次 | max 2pt |
| Original Repos（公开非空） | 0.5pt/个 | max 1pt |
| Stars（原创 repo 获星） | 0.1pt/颗 | max 5pt |

## 四、iBubble 账号当前状态

- **GitHub**: https://github.com/iBubble
- **注册日期**: 2011-10-22（14年+）
- **Pollinations Tier**: 🍄 Spore (0.01 p/hr)
- **API Key**: `sk_pmBF6hTFDV0UFDFGHRsTHTlPG4GYP9ej`

### Dev Points 预估（9pt）

| 维度 | 实际 | 得分 |
|------|------|------|
| 账号年龄 14年 | 远超上限 | **6pt** ✅ |
| Public Commits | 20个 | **2pt** ✅ |
| Original Repos | 3个 | **1pt** ✅ |
| Stars | 0颗 | 0pt |
| **总计** | | **9pt ≥ 8pt** |

## 五、已完成操作

- [x] 创建 GitHub 公开 repo: https://github.com/iBubble/ai-image-tools
- [x] 推送 20 个 commits 到 main 分支
- [x] 在 Pollinations 获取新 API Key

## 六、待执行操作

### 短期（等待周评估 → Spore → Seed）
- [ ] 等待 Pollinations 每周 Dev Points 自动评估
- [ ] 确认 Tier 更新为 🌱 Seed (0.15 p/hr)

### 中期（Seed → Flower）
- [ ] 将 Image Studio 部署到公网（Vercel / Railway / 内网穿透）
- [ ] 通过 GitHub Issue 提交 App 发布申请:
      https://github.com/pollinations/pollinations/issues/new?template=tier-app-submission.yml
- [ ] 确认 Tier 更新为 🌸 Flower (10 p/day)

### 可选加分项
- [ ] 用其他 GitHub 账号给 ai-image-tools 点 Star（每颗 +0.1pt）

## 七、额度恢复机制

- 免费额度（Flower）按 **小时** 恢复（3月27日后）
- Flower: 0.4 p/hr, Nectar: 0.8 p/hr
- 额度有上限 cap，消耗后立即开始恢复
- 充值 $5 → 10 pollen（beta翻倍），一次性额度
