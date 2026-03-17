# 商业图表生成模块

## 一、图表类型与应用场景

### 1.1 瀑布图（Waterfall Chart）
**应用场景**: 财务分析、成本分解、利润桥接
**适用于**: 展示累积效应和各因素贡献

### 1.2 热力图（Heatmap）
**应用场景**: 优先级矩阵、风险评估、相关性分析
**适用于**: 展示二维数据的强度分布

### 1.3 漏斗图（Funnel Chart）
**应用场景**: 转化分析、销售漏斗、用户流程
**适用于**: 展示逐步递减的流程

### 1.4 甘特图（Gantt Chart）
**应用场景**: 项目计划、实施路线图、时间线
**适用于**: 展示任务时间安排和依赖关系

### 1.5 桑基图（Sankey Diagram）
**应用场景**: 流程分析、资源流动、价值链
**适用于**: 展示流量的分配和转移

## 二、技术栈

推荐使用 Python + Plotly 实现交互式图表：

```python
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
```

## 三、代码示例

### 3.1 瀑布图示例

```python
import plotly.graph_objects as go

# 数据
categories = ['初始收入', '成本节约', '新业务', '运营成本', '最终收入']
values = [100, 20, 30, -15, 135]

# 创建瀑布图
fig = go.Figure(go.Waterfall(
    x=categories,
    y=values,
    measure=['absolute', 'relative', 'relative', 'relative', 'total'],
    text=[f'{v}M' for v in values],
    textposition='outside',
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
))

fig.update_layout(
    title='收入变化分析',
    showlegend=False,
    height=500
)

fig.write_html('waterfall_chart.html')
```

### 3.2 热力图示例

```python
import plotly.express as px
import pandas as pd

# 优先级矩阵数据
data = {
    '影响': ['高', '高', '中', '中', '低'],
    '难度': ['低', '高', '低', '高', '中'],
    '项目': ['项目A', '项目B', '项目C', '项目D', '项目E']
}

df = pd.DataFrame(data)

# 创建优先级矩阵
fig = px.scatter(df, x='难度', y='影响', text='项目',
                 size=[100]*len(df),
                 color='影响',
                 title='项目优先级矩阵')

fig.update_traces(textposition='top center')
fig.update_layout(height=500)

fig.write_html('priority_matrix.html')
```

### 3.3 漏斗图示例

```python
import plotly.graph_objects as go

# 转化漏斗数据
stages = ['访问', '注册', '试用', '付费', '续费']
values = [10000, 5000, 2000, 800, 600]

fig = go.Figure(go.Funnel(
    y=stages,
    x=values,
    textinfo='value+percent initial',
))

fig.update_layout(
    title='用户转化漏斗',
    height=500
)

fig.write_html('funnel_chart.html')
```

### 3.4 甘特图示例

```python
import plotly.figure_factory as ff
import pandas as pd

# 项目任务数据
df = pd.DataFrame([
    dict(Task='需求分析', Start='2026-03-01', Finish='2026-03-15', Resource='团队A'),
    dict(Task='方案设计', Start='2026-03-10', Finish='2026-03-25', Resource='团队B'),
    dict(Task='开发实施', Start='2026-03-20', Finish='2026-04-30', Resource='团队A'),
    dict(Task='测试验收', Start='2026-04-25', Finish='2026-05-15', Resource='团队C'),
])

fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True,
                      group_tasks=True, title='项目实施计划')

fig.write_html('gantt_chart.html')
```

## 四、图表设计原则

1. **简洁明了**: 避免过度装饰
2. **数据准确**: 确保数据来源可靠
3. **颜色一致**: 使用统一的配色方案
4. **标注清晰**: 添加必要的标签和说明
5. **交互友好**: 利用 Plotly 的交互特性

## 五、常用配色方案

### 专业配色
- 主色：#1f77b4（蓝色）
- 辅色：#ff7f0e（橙色）
- 强调：#2ca02c（绿色）
- 警告：#d62728（红色）

### McKinsey 风格
- 深蓝：#003f5c
- 中蓝：#58508d
- 紫色：#bc5090
- 粉色：#ff6361
- 橙色：#ffa600
