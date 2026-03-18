"""
咨询报告图表生成工具库

提供常用商业图表的快速生成函数，基于 Plotly 实现。
"""

from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd


def create_waterfall_chart(
    categories: List[str],
    values: List[float],
    title: str = "瀑布图",
    output_path: str = "waterfall_chart.html",
    measure: Optional[List[str]] = None
) -> go.Figure:
    """
    创建瀑布图，用于展示累积效应和各因素贡献。

    应用场景：财务分析、成本分解、利润桥接

    参数:
        categories: 类别列表，如 ['初始收入', '成本节约', '新业务', '运营成本', '最终收入']
        values: 数值列表，对应每个类别的值
        title: 图表标题
        output_path: 输出 HTML 文件路径
        measure: 测量类型列表，如 ['absolute', 'relative', 'relative', 'relative', 'total']
                 若为 None，则自动设置首项为 'absolute'，末项为 'total'，其余为 'relative'

    返回:
        Plotly Figure 对象

    示例:
        >>> create_waterfall_chart(
        ...     categories=['初始收入', '成本节约', '新业务', '运营成本', '最终收入'],
        ...     values=[100, 20, 30, -15, 135],
        ...     title='收入变化分析'
        ... )
    """
    if measure is None:
        measure = ['absolute'] + ['relative'] * (len(categories) - 2) + ['total']

    fig = go.Figure(go.Waterfall(
        x=categories,
        y=values,
        measure=measure,
        text=[f'{v}M' for v in values],
        textposition='outside',
        connector={'line': {'color': 'rgb(63, 63, 63)'}},
    ))

    fig.update_layout(title=title, showlegend=False, height=500)
    fig.write_html(output_path)
    return fig


def create_heatmap(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    text_col: str,
    title: str = "热力图",
    output_path: str = "heatmap.html"
) -> go.Figure:
    """
    创建热力图/优先级矩阵，用于展示二维数据的强度分布。

    应用场景：优先级矩阵、风险评估、相关性分析

    参数:
        data: pandas DataFrame，包含 x、y 和文本标签列
        x_col: X 轴列名
        y_col: Y 轴列名
        text_col: 文本标签列名
        title: 图表标题
        output_path: 输出 HTML 文件路径

    返回:
        Plotly Figure 对象

    示例:
        >>> df = pd.DataFrame({
        ...     '影响': ['高', '高', '中', '中', '低'],
        ...     '难度': ['低', '高', '低', '高', '中'],
        ...     '项目': ['项目A', '项目B', '项目C', '项目D', '项目E']
        ... })
        >>> create_heatmap(df, '难度', '影响', '项目', '项目优先级矩阵')
    """
    fig = px.scatter(
        data, x=x_col, y=y_col, text=text_col,
        size=[100] * len(data),
        color=y_col,
        title=title
    )

    fig.update_traces(textposition='top center')
    fig.update_layout(height=500)
    fig.write_html(output_path)
    return fig


def create_funnel_chart(
    stages: List[str],
    values: List[int],
    title: str = "漏斗图",
    output_path: str = "funnel_chart.html"
) -> go.Figure:
    """
    创建漏斗图，用于展示逐步递减的流程。

    应用场景：转化分析、销售漏斗、用户流程

    参数:
        stages: 阶段列表，如 ['访问', '注册', '试用', '付费', '续费']
        values: 数值列表，对应每个阶段的值
        title: 图表标题
        output_path: 输出 HTML 文件路径

    返回:
        Plotly Figure 对象

    示例:
        >>> create_funnel_chart(
        ...     stages=['访问', '注册', '试用', '付费', '续费'],
        ...     values=[10000, 5000, 2000, 800, 600],
        ...     title='用户转化漏斗'
        ... )
    """
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo='value+percent initial',
    ))

    fig.update_layout(title=title, height=500)
    fig.write_html(output_path)
    return fig


def create_gantt_chart(
    tasks: List[Dict[str, str]],
    title: str = "甘特图",
    output_path: str = "gantt_chart.html",
    index_col: str = "Resource"
) -> go.Figure:
    """
    创建甘特图，用于展示任务时间安排和依赖关系。

    应用场景：项目计划、实施路线图、时间线

    参数:
        tasks: 任务列表，每个任务为字典，包含 Task、Start、Finish、Resource 键
        title: 图表标题
        output_path: 输出 HTML 文件路径
        index_col: 分组列名，默认为 'Resource'

    返回:
        Plotly Figure 对象

    示例:
        >>> tasks = [
        ...     dict(Task='需求分析', Start='2026-03-01', Finish='2026-03-15', Resource='团队A'),
        ...     dict(Task='方案设计', Start='2026-03-10', Finish='2026-03-25', Resource='团队B'),
        ... ]
        >>> create_gantt_chart(tasks, '项目实施计划')
    """
    df = pd.DataFrame(tasks)
    fig = ff.create_gantt(
        df, index_col=index_col, show_colorbar=True,
        group_tasks=True, title=title
    )
    fig.write_html(output_path)
    return fig


def create_sankey_diagram(
    flows: Dict[str, Any],
    title: str = "桑基图",
    output_path: str = "sankey_diagram.html"
) -> go.Figure:
    """
    创建桑基图，用于展示流量的分配和转移。

    应用场景：流程分析、资源流动、价值链

    参数:
        flows: 流动数据字典，包含 'source'、'target'、'value' 键
               source: 源节点索引列表
               target: 目标节点索引列表
               value: 流量值列表
               label: 节点标签列表（可选）
        title: 图表标题
        output_path: 输出 HTML 文件路径

    返回:
        Plotly Figure 对象

    示例:
        >>> flows = {
        ...     'source': [0, 0, 1, 1, 2],
        ...     'target': [2, 3, 2, 3, 4],
        ...     'value': [8, 2, 2, 8, 10],
        ...     'label': ['A', 'B', 'C', 'D', 'E']
        ... }
        >>> create_sankey_diagram(flows, '资源流动分析')
    """
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=flows.get('label', []),
        ),
        link=dict(
            source=flows['source'],
            target=flows['target'],
            value=flows['value']
        )
    ))

    fig.update_layout(title=title, height=500)
    fig.write_html(output_path)
    return fig


def create_bubble_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: str,
    text_col: str,
    title: str = "气泡图",
    output_path: str = "bubble_chart.html"
) -> go.Figure:
    """
    创建气泡图，用于展示三维数据关系。

    应用场景：市场定位、竞争分析、投资组合

    参数:
        data: pandas DataFrame
        x_col: X 轴列名
        y_col: Y 轴列名
        size_col: 气泡大小列名
        text_col: 文本标签列名
        title: 图表标题
        output_path: 输出 HTML 文件路径

    返回:
        Plotly Figure 对象

    示例:
        >>> df = pd.DataFrame({
        ...     '市场份额': [20, 15, 10, 8, 5],
        ...     '增长率': [15, 25, 10, 5, 30],
        ...     '收入': [100, 80, 60, 40, 20],
        ...     '公司': ['A', 'B', 'C', 'D', 'E']
        ... })
        >>> create_bubble_chart(df, '市场份额', '增长率', '收入', '公司', '市场竞争格局')
    """
    fig = px.scatter(
        data, x=x_col, y=y_col, size=size_col, text=text_col,
        title=title
    )

    fig.update_traces(textposition='top center')
    fig.update_layout(height=500)
    fig.write_html(output_path)
    return fig
