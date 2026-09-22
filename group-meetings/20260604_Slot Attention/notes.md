根据会议记录为您生成详细智能总结如下：
录制: 组会
日期: 2026-06-04 18:57:00
录制文件：https://meeting.tencent.com/crm/2pQvVAbZ33
📋 组会智能总结 · 2026-06-04

会议主题： 组会 — NeurIPS 2020《Slot Attention》论文分享与讨论  
主持人/组织者： 方榯楷Shikai Fang  
参会人员： 方榯楷Shikai Fang、超级无敌巨无霸土豆（雨阳/宇航）、陈力豪、张欣宇  
会议时间： 18:57 ~ 20:15（约78分钟）

一、会议安排通知

• 组会计划开到 7月初，暑假暂停，9月新学期恢复。

• 每位成员暑假前再轮流主讲一次论文。

• 下周由 陈力豪 分享 JEPA（Joint Embedding Predictive Architecture） 系列经典论文。

二、论文分享 — "Object-Centric Learning with Slot Attention" (NeurIPS 2020)

1. 核心思想：Object-Centric Representation（以对象为中心的表示）

表示方式 特点

分布式表示（Distributed） Encoder输出高维稠密向量，各维度无明确物理意义，信息纠缠，难以单独提取某物体或属性

Object-Centric / Slot-based 隐空间分解为若干独立Slot（槽），每个Slot候选表示一个物体/组分，可单独编辑，可解释性强

• Slot 随机高斯初始化，不绑定特定类别，顺序可交换（Set 性质）。

• Slot 数量 K ≥ 图中物体数，多余 Slot 学成 ∅(no object)。

2. Slot Attention 模块流程

3. CNN 提取图像特征 → Inputs（作为 K/V）
4. Slots 作为 Query（类似 DETR 的 object queries）
5. 计算 Softmax(slots_dim)(Q·Kᵀ) → 按 Slot 维度归一化（与 DETR 按 Input 维度归一化不同），形成 Slot 间竞争
6. 按注意力权重对 Inputs(V) 加权平均 → Update vector
7. 用 GRU 将旧 Slot 与 Update 融合
8. 上述步骤迭代 T=3 次（训练固定3轮，推理可增加至7轮效果略升）

9. 训练方式

• 无监督： 仅 Image Reconstruction（MSE + Alpha Mask），无需标注，可无监督发现物体结构

• 有监督（目标检测）： Slot → MLP → Box/Class + Bipartite Matching Loss（类 DETR）

4. 实验结论

• 在 CLEVR / Tetrominoes 等合成数据集 ARI（Adjusted Rand Index）显著优于 Baseline（Slot-MLP 去掉 Attention 后效果差→Attention竞争机制是关键）

• 物体数增多时需增大 K；背景无特殊处理是局限性

• 真实复杂自然图像（强纹理/严重遮挡）效果有限

5. 局限性讨论（由分享人+导师补充）

• 不"知道"什么是物体，完全靠数据+Loss诱导

• 无专门背景 Slot，简单背景下 OK

• 复杂自然场景泛化差

• Slot 语义不可直接解释（尤其他领域如物理场），需借助约束/Loss设计引导

三、讨论与延伸——Slot Attention 在 AI for Physics 的启发

方老师引导讨论的核心观点：

1. Slot ≈ 可学习的 K-Means 聚类，在隐空间做解耦表征
2. 无监督即可对齐物体是 CV 中"magic"现象，值得思考能否迁移
3. 物理场应用设想：
   • Slot 可否自动解耦低频/高频成分、不同波源？

   • 可通过 Per-Slot Loss 约束（如低频 Slot 时间连续性高、高频允许跳变）引导 Slot 语义

   • Slot Number K 的选择目前需预设/搜索，是待解决问题

4. 多模态/多源信号（不同物理源、谱分量）也可类比为已知 K 的 Slot 分配问题
5. 后续组会也会涉及 对比学习/自监督/JEPA 等表征学习方法

学员提问亮点：
• 张欣宇：K 与物体数的关系（K≥物体数即可，多余为 ∅）；复杂图像背景问题

• 陈力豪：增大 K 是否改善多物体场景（是，但需重新训练）；联想多模态分离

• 关于 Slot Number 改变是否需要重训→原文固定 K 训练，改变 K 通常需重新训练（虽 Attention 理论可适应不同 token 数，但实践中原实现按固定 K）

四、行动项 & 后续安排

事项 负责人 说明

准备 JEPA 论文分享 陈力豪 下周组会，选经典 Paper 讲思路与表征学习思想

Slot Attention 向物理场表征探索 雨阳（先行），力豪&欣宇后续参与 设计实验验证 Slot 在物理场中的解耦能力

组会继续至7月初 全员 每人再讲一次，暑假停，9月恢复

五、会议评价

• 雨阳首次讲 CV 经典 Paper，对 Object-Centric / Slot Attention / Transformer 前因后果讲解清晰，结合导师追问互动良好 ✅

• 全员参与提问讨论热度较高，导师做了充分的领域迁移引导

• 下次分享希望同样注重核心动机 + 与本项目关联思考

如需导出为 Word/Markdown 文件或只保留某一板块（如仅论文笔记或只行动项），可以告诉我 😊