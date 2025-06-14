import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime


class SalaryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("薪资计算器")
        self.root.geometry("1000x700")

        # 创建变量
        self.create_variables()

        # 创建主框架
        self.create_main_frame()

        # 创建界面
        self.create_interface()

    def create_variables(self):
        """创建所有需要的变量"""
        # 基础参数
        self.delivery_amount = tk.DoubleVar(value=100.0)
        self.purchase_amount = tk.DoubleVar(value=50.0)  # 购买服务包数量（用于所有计算）
        self.service_price = tk.DoubleVar(value=1000.0)
        self.service_cost = tk.DoubleVar(value=300.0)
        self.store_staff_count = tk.IntVar(value=5)
        self.employee_type = tk.StringVar(value="员工")

        # 旧薪资体系参数
        self.old_base_salary = tk.DoubleVar(value=3000.0)
        self.old_basic_bonus = tk.DoubleVar(value=500.0)
        self.old_position_bonus = tk.DoubleVar(value=300.0)
        self.old_extra_bonus = tk.DoubleVar(value=200.0)

        # 新薪资体系参数
        self.new_base_salary_mid = tk.DoubleVar(value=3500.0)
        self.new_base_salary_low = tk.DoubleVar(value=2800.0)
        self.old_purchase_baseline = tk.DoubleVar(value=40.0)
        self.planned_increase = tk.DoubleVar(value=20.0)
        self.new_bonus_coefficient = tk.DoubleVar(value=1.2)
        self.min_conversion_rate = tk.DoubleVar(value=45.0)
        self.penalty_rate = tk.DoubleVar(value=0.8)
        self.salary_mode = tk.StringVar(value="新保底")  # 薪资模式选择
        self.bonus_multiplier = tk.DoubleVar(value=1.5)  # 超额奖金倍数，替代 *1.5
        self.bonus_tier1_threshold = tk.DoubleVar(value=1.0)  # 档1百分比，如 1.0表示100%
        self.bonus_tier2_threshold = tk.DoubleVar(value=1.5)  # 档2百分比，如 1.5表示150%
        self.bonus_extra1 = tk.DoubleVar(value=10.0)  # 档2每包追加金额
        self.bonus_extra2 = tk.DoubleVar(value=20.0)  # 档3每包追加金额
        self.new_purchase_amount = tk.DoubleVar(value=0.0)  # 新服务包购买数，优先替代原 purchase_amount

        # 展示模块参数
        self.current_month = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        self.avg_total_salary = tk.DoubleVar(value=5000.0)
        self.avg_delivery = tk.DoubleVar(value=80.0)
        self.avg_purchase = tk.DoubleVar(value=40.0)
        self.avg_conversion_rate = tk.DoubleVar(value=50.0)
        self.city_cost = tk.DoubleVar(value=10000.0)

    def create_main_frame(self):
        """创建主框架"""
        # 创建笔记本控件（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建各个标签页
        self.create_input_tab()
        self.create_calculation_tab()
        self.create_comparison_tab()
        self.create_store_analysis_tab()
        self.create_visualization_tab()
        self.create_formula_tab()  # 公式说明标签页

    def create_input_tab(self):
        """创建参数输入标签页"""
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="参数设置")

        # 创建滚动框架
        canvas = tk.Canvas(self.input_frame)
        scrollbar = ttk.Scrollbar(self.input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 基础参数组
        basic_group = ttk.LabelFrame(scrollable_frame, text="基础参数", padding=10)
        basic_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(basic_group, text="交付量:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(basic_group, textvariable=self.delivery_amount, width=15).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(basic_group, text="购买服务包数量:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(basic_group, textvariable=self.purchase_amount, width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(basic_group, text="服务包单价:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(basic_group, textvariable=self.service_price, width=15).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(basic_group, text="服务包必要支出:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(basic_group, textvariable=self.service_cost, width=15).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(basic_group, text="门店人数:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(basic_group, textvariable=self.store_staff_count, width=15).grid(row=2, column=1, padx=5, pady=2)

        # 员工类型选择
        ttk.Label(basic_group, text="员工类型:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        employee_combo = ttk.Combobox(basic_group, textvariable=self.employee_type, values=["员工", "主管"], width=12)
        employee_combo.grid(row=2, column=3, padx=5, pady=2)
        employee_combo.state(['readonly'])

        # 旧薪资体系参数组
        old_salary_group = ttk.LabelFrame(scrollable_frame, text="旧薪资体系参数", padding=10)
        old_salary_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(old_salary_group, text="底薪:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(old_salary_group, textvariable=self.old_base_salary, width=15).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(old_salary_group, text="基本绩效:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(old_salary_group, textvariable=self.old_basic_bonus, width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(old_salary_group, text="岗位绩效:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(old_salary_group, textvariable=self.old_position_bonus, width=15).grid(row=1, column=1, padx=5,
                                                                                         pady=2)

        ttk.Label(old_salary_group, text="奖金:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(old_salary_group, textvariable=self.old_extra_bonus, width=15).grid(row=1, column=3, padx=5, pady=2)

        # 新薪资体系参数组
        new_salary_group = ttk.LabelFrame(scrollable_frame, text="新薪资体系参数", padding=10)
        new_salary_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(new_salary_group, text="新底薪（中）:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.new_base_salary_mid, width=15).grid(row=0, column=1, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="新底薪（低）:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.new_base_salary_low, width=15).grid(row=0, column=3, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="旧购买服务包基准:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.old_purchase_baseline, width=15).grid(row=1, column=1, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="计划新增服务包数:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.planned_increase, width=15).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(new_salary_group, text="新奖金系数:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.new_bonus_coefficient, width=15).grid(row=2, column=1, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="下线转化率(%):").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.min_conversion_rate, width=15).grid(row=2, column=3, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="未达标折扣率:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.penalty_rate, width=15).grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(new_salary_group, text="新服务包购买数量:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.new_purchase_amount, width=15).grid(row=4, column=1, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="超额奖金倍数:").grid(row=4, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_multiplier, width=15).grid(row=4, column=3, padx=5, pady=2)

        ttk.Label(new_salary_group, text="档1占比阈值 (%):").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier1_threshold, width=15).grid(row=6, column=1, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="档2占比阈值 (%):").grid(row=6, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier2_threshold, width=15).grid(row=6, column=3, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="档2每包追加金额:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_extra1, width=15).grid(row=7, column=1, padx=5, pady=2)

        ttk.Label(new_salary_group, text="档3每包追加金额:").grid(row=7, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_extra2, width=15).grid(row=7, column=3, padx=5, pady=2)

        # 展示模块参数组
        display_group = ttk.LabelFrame(scrollable_frame, text="展示模块参数", padding=10)
        display_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(display_group, text="当前月份:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.current_month, width=15).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(display_group, text="平均总薪资:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.avg_total_salary, width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(display_group, text="平均交付量:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.avg_delivery, width=15).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(display_group, text="平均购买服务包数:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.avg_purchase, width=15).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(display_group, text="平均转化率(%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.avg_conversion_rate, width=15).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(display_group, text="城市平均成本:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.city_cost, width=15).grid(row=2, column=3, padx=5, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_calculation_tab(self):
        """创建薪资计算标签页"""
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text="薪资计算")

        # 薪资模式选择
        mode_frame = ttk.LabelFrame(self.calc_frame, text="薪资模式选择", padding=10)
        mode_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(mode_frame, text="选择薪资模式:").pack(side=tk.LEFT, padx=5)
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.salary_mode,
                                  values=["新保底", "新底薪（中）", "新底薪（低）"], width=15)
        mode_combo.pack(side=tk.LEFT, padx=5)
        mode_combo.state(['readonly'])

        # 当前底薪值显示
        salary_display_frame = ttk.LabelFrame(self.calc_frame, text="当前底薪值", padding=10)
        salary_display_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(salary_display_frame, text="新保底模式底薪:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.old_base_display = ttk.Label(salary_display_frame, text="")
        self.old_base_display.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(salary_display_frame, text="新底薪（中）:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.mid_base_display = ttk.Label(salary_display_frame, text="")
        self.mid_base_display.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(salary_display_frame, text="新底薪（低）:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.low_base_display = ttk.Label(salary_display_frame, text="")
        self.low_base_display.grid(row=0, column=5, padx=5, pady=2)

        # 绑定变量更新显示
        self.old_base_salary.trace_add("write", self.update_salary_displays)
        self.new_base_salary_mid.trace_add("write", self.update_salary_displays)
        self.new_base_salary_low.trace_add("write", self.update_salary_displays)

        # 计算按钮
        calc_button = ttk.Button(mode_frame, text="计算薪资", command=self.calculate_salary)
        calc_button.pack(side=tk.LEFT, padx=20)

        # 结果显示区域
        result_frame = ttk.LabelFrame(self.calc_frame, text="计算结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建结果显示的文本框
        self.result_text = tk.Text(result_frame, height=20, width=80)
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")

        # 初始化显示
        self.update_salary_displays()

    def create_comparison_tab(self):
        """创建薪资对比标签页"""
        self.comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_frame, text="薪资对比")

        # 对比按钮
        compare_button = ttk.Button(self.comparison_frame, text="生成对比报告", command=self.generate_comparison)
        compare_button.pack(pady=10)

        # 对比结果显示
        self.comparison_text = tk.Text(self.comparison_frame, height=25, width=100)
        comp_scrollbar = ttk.Scrollbar(self.comparison_frame, orient="vertical", command=self.comparison_text.yview)
        self.comparison_text.configure(yscrollcommand=comp_scrollbar.set)

        self.comparison_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        comp_scrollbar.pack(side="right", fill="y")

    def create_store_analysis_tab(self):
        """创建门店分析标签页"""
        self.store_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.store_frame, text="门店分析")

        # 分析按钮
        analyze_button = ttk.Button(self.store_frame, text="门店财务分析", command=self.analyze_store)
        analyze_button.pack(pady=10)

        # 分析结果显示
        self.store_text = tk.Text(self.store_frame, height=25, width=100)
        store_scrollbar = ttk.Scrollbar(self.store_frame, orient="vertical", command=self.store_text.yview)
        self.store_text.configure(yscrollcommand=store_scrollbar.set)

        self.store_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        store_scrollbar.pack(side="right", fill="y")

    def create_visualization_tab(self):
        """创建数据可视化标签页"""
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="数据可视化")

        # 可视化按钮
        viz_button = ttk.Button(self.viz_frame, text="生成图表", command=self.generate_charts)
        viz_button.pack(pady=10)

        # 图表显示区域
        self.viz_text = tk.Text(self.viz_frame, height=25, width=100)
        viz_scrollbar = ttk.Scrollbar(self.viz_frame, orient="vertical", command=self.viz_text.yview)
        self.viz_text.configure(yscrollcommand=viz_scrollbar.set)

        self.viz_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        viz_scrollbar.pack(side="right", fill="y")

    def create_formula_tab(self):
        """创建公式说明标签页"""
        self.formula_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.formula_frame, text="公式说明")

        # 创建文本区域
        formula_text = tk.Text(self.formula_frame, wrap=tk.WORD, height=25, width=100)
        scrollbar = ttk.Scrollbar(self.formula_frame, orient="vertical", command=formula_text.yview)
        formula_text.configure(yscrollcommand=scrollbar.set)

        formula_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # 添加公式说明
        formula_content = """
    === 薪资计算公式说明 ===

    1. 转化率计算:
       转化率 = (购买服务包数量 / 交付量) × 100%

    2. 旧薪资体系计算公式:
       基础计算部分 = (交付量 × 转化率/100 - 交付量/2) × 10 / 门店人数

       如果转化率 ≥ 50%:
           薪资 = 底薪 + 基础计算部分 + 基本绩效 + 岗位绩效 + 奖金
       否则:
           薪资 = 底薪 + 基础计算部分 + (基本绩效 + 岗位绩效)/2 + 奖金

       如果是主管:
           薪资 += 500

    3. 新薪资体系计算公式（模式二/三）:

   A. 新保底模式（模式一）:
      使用旧薪资计算公式。

   B. 新底薪（中）模式（模式二）与 新底薪（低）模式（模式三）:
      新薪资 = 新底薪 + 三档提成总额

      三档提成逻辑如下（以旧底薪为基准）：

      - 差值 = 旧底薪 - 新底薪
      - 单个服务包基础提成 = 差值 / 旧服务包基准数

      根据实际售出服务包数量，分为三档计算：

      ● 档1：实际 ≤ 阈值X%
         提成 = 单包基础提成 × 实际售出服务包数

      ● 档2：阈值X% < 实际 ≤ 阈值Y%
         提成 = 
           单包基础提成 × X%数量
         + (单包提成 + 每包追加金额1) × 超出X%的数量

      ● 档3：实际 > 阈值Y%
         提成 = 
           档1提成
         + 档2追加提成
         + (单包提成 + 每包追加金额2) × 超出Y%的部分数量

      ※ 阈值、追加金额均为可配置参数。

      如果员工类型为主管，额外加 500 元。

      若转化率低于下线值，最终薪资 × 折扣比例（如 0.8）。

    4. 门店财务分析公式:
       门店总流水 = 购买服务包数量 × 服务包单价
       客单利润 = 服务包单价 - 服务包必要支出
       门店总利润 = 购买服务包数量 × 客单利润
       净利润 = 门店总利润 - (员工总薪资成本 + 城市平均成本)
    """
        formula_text.insert(tk.END, formula_content)
        formula_text.config(state=tk.DISABLED)  # 设置为只读

    def create_interface(self):
        """创建完整界面"""
        # 在主窗口底部添加导出按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="导出Excel报告", command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存参数配置", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="加载参数配置", command=self.load_config).pack(side=tk.LEFT, padx=5)

    def update_salary_displays(self, *args):
        """更新底薪显示值，安全处理空值和无效输入"""
        try:
            # 安全获取旧底薪值，处理空值
            old_base = self.old_base_salary.get()
            if old_base == "":
                old_base = 0
            self.old_base_display.config(text=f"{float(old_base):.2f}")
        except Exception:
            self.old_base_display.config(text="0.00")

        try:
            # 安全获取中底薪值，处理空值
            mid_base = self.new_base_salary_mid.get()
            if mid_base == "":
                mid_base = 0
            self.mid_base_display.config(text=f"{float(mid_base):.2f}")
        except Exception:
            self.mid_base_display.config(text="0.00")

        try:
            # 安全获取低底薪值，处理空值
            low_base = self.new_base_salary_low.get()
            if low_base == "":
                low_base = 0
            self.low_base_display.config(text=f"{float(low_base):.2f}")
        except Exception:
            self.low_base_display.config(text="0.00")

    def calculate_conversion_rate(self):
        """计算转化率"""
        delivery = self.delivery_amount.get()
        purchase = self.purchase_amount.get()
        if delivery == 0:
            return 0
        return (purchase / delivery) * 100

    def calculate_old_salary(self):
        """计算旧薪资体系的薪资"""
        delivery = self.delivery_amount.get()
        purchase = self.purchase_amount.get()
        conversion_rate = self.calculate_conversion_rate()
        staff_count = self.store_staff_count.get()

        base_salary = self.old_base_salary.get()
        basic_bonus = self.old_basic_bonus.get()
        position_bonus = self.old_position_bonus.get()
        extra_bonus = self.old_extra_bonus.get()

        # 计算基础薪资部分
        base_calculation = (delivery * conversion_rate / 100 - delivery / 2) * 10 / staff_count

        if conversion_rate >= 50:
            # 转化率高于50%
            salary = base_salary + base_calculation + basic_bonus + position_bonus + extra_bonus
        else:
            # 转化率低于50%
            salary = base_salary + base_calculation + (basic_bonus + position_bonus) / 2 + extra_bonus

        # 如果是主管，加500
        if self.employee_type.get() == "主管":
            salary += 500

        return salary

    def calculate_new_salary_mode1(self):
        """计算新薪资体系模式一：新保底（与旧薪资相同）"""
        return self.calculate_old_salary()

    def calculate_new_salary_mode2(self):
        """计算新薪资体系模式二：新底薪（中） - 三档提成逻辑"""
        purchase_amount = self.new_purchase_amount.get() or self.purchase_amount.get()
        old_purchase_baseline = self.old_purchase_baseline.get()
        new_base = self.new_base_salary_mid.get()
        old_base = self.old_base_salary.get()

        base_diff = old_base - new_base
        per_package_bonus = base_diff / old_purchase_baseline if old_purchase_baseline > 0 else 0

        tier1_ratio = self.bonus_tier1_threshold.get()
        tier2_ratio = self.bonus_tier2_threshold.get()
        extra1 = self.bonus_extra1.get()
        extra2 = self.bonus_extra2.get()

        tier1_limit = old_purchase_baseline * tier1_ratio
        tier2_limit = old_purchase_baseline * tier2_ratio

        if purchase_amount <= tier1_limit:
            bonus = per_package_bonus * purchase_amount
        elif purchase_amount <= tier2_limit:
            bonus = per_package_bonus * tier1_limit + (per_package_bonus + extra1) * (purchase_amount - tier1_limit)
        else:
            bonus = (
                    per_package_bonus * tier1_limit +
                    (per_package_bonus + extra1) * (tier2_limit - tier1_limit) +
                    (per_package_bonus + extra2) * (purchase_amount - tier2_limit)
            )

        salary = new_base + bonus

        if self.employee_type.get() == "主管":
            salary += 500

        return salary

    def calculate_new_salary_mode3(self):
        """计算新薪资体系模式三：新底薪（低） - 三档提成逻辑"""
        purchase_amount = self.new_purchase_amount.get() or self.purchase_amount.get()
        old_purchase_baseline = self.old_purchase_baseline.get()
        new_base = self.new_base_salary_low.get()
        old_base = self.old_base_salary.get()

        base_diff = old_base - new_base
        per_package_bonus = base_diff / old_purchase_baseline if old_purchase_baseline > 0 else 0

        tier1_ratio = self.bonus_tier1_threshold.get()
        tier2_ratio = self.bonus_tier2_threshold.get()
        extra1 = self.bonus_extra1.get()
        extra2 = self.bonus_extra2.get()

        tier1_limit = old_purchase_baseline * tier1_ratio
        tier2_limit = old_purchase_baseline * tier2_ratio

        if purchase_amount <= tier1_limit:
            bonus = per_package_bonus * purchase_amount
        elif purchase_amount <= tier2_limit:
            bonus = per_package_bonus * tier1_limit + (per_package_bonus + extra1) * (purchase_amount - tier1_limit)
        else:
            bonus = (
                    per_package_bonus * tier1_limit +
                    (per_package_bonus + extra1) * (tier2_limit - tier1_limit) +
                    (per_package_bonus + extra2) * (purchase_amount - tier2_limit)
            )

        salary = new_base + bonus

        if self.employee_type.get() == "主管":
            salary += 500

        print(f"[DEBUG] 使用底薪（低）: {new_base}, bonus: {bonus}, total: {salary}")

        return salary

    def apply_conversion_rate_penalty(self, salary):
            """应用转化率未达标的折扣"""
            conversion_rate = self.calculate_conversion_rate()
            min_rate = self.min_conversion_rate.get()
            penalty_rate = self.penalty_rate.get()

            if conversion_rate < min_rate:
                return salary * penalty_rate
            return salary

    def calculate_salary(self):
        """计算并显示薪资结果"""
        try:
            self.result_text.delete(1.0, tk.END)

            # 获取基本参数
            delivery = self.delivery_amount.get()
            purchase = self.purchase_amount.get()
            conversion_rate = self.calculate_conversion_rate()
            employee_type = self.employee_type.get()
            salary_mode = self.salary_mode.get()

            result = f"=== 薪资计算结果 ===\n\n"
            result += f"员工类型: {employee_type}\n"
            result += f"交付量: {delivery}\n"
            result += f"购买服务包数量: {purchase}\n"
            result += f"转化率: {conversion_rate:.2f}%\n"
            result += f"选择模式: {salary_mode}\n\n"

            # 计算旧薪资
            old_salary = self.calculate_old_salary()
            result += f"旧薪资体系计算结果: {old_salary:.2f}元\n\n"

            # 根据选择的模式计算新薪资
            if salary_mode == "新保底":
                new_salary = self.calculate_new_salary_mode1()
            elif salary_mode == "新底薪（中）":
                new_salary = self.calculate_new_salary_mode2()
            else:  # 新底薪（低）
                new_salary = self.calculate_new_salary_mode3()

            # 应用转化率折扣
            new_salary_with_penalty = self.apply_conversion_rate_penalty(new_salary)

            result += f"新薪资体系（{salary_mode}）计算结果: {new_salary:.2f}元\n"

            if new_salary != new_salary_with_penalty:
                result += f"转化率未达标，应用折扣后: {new_salary_with_penalty:.2f}元\n"

            # 薪资差异分析
            difference = new_salary_with_penalty - old_salary
            result += f"\n薪资差异: {difference:.2f}元\n"

            if difference > 0:
                result += f"新模式比旧模式多 {difference:.2f}元 ({(difference / old_salary) * 100:.2f}%)\n"
            elif difference < 0:
                result += f"新模式比旧模式少 {abs(difference):.2f}元 ({(abs(difference) / old_salary) * 100:.2f}%)\n"
            else:
                result += "新旧模式薪资相同\n"

            # 客单利润计算
            service_price = self.service_price.get()
            service_cost = self.service_cost.get()
            unit_profit = service_price - service_cost
            total_profit = purchase * unit_profit

            result += f"\n=== 业务数据 ===\n"
            result += f"服务包单价: {service_price:.2f}元\n"
            result += f"服务包成本: {service_cost:.2f}元\n"
            result += f"客单利润: {unit_profit:.2f}元\n"
            result += f"总利润: {total_profit:.2f}元\n"

            self.result_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误: {str(e)}")

    def generate_comparison(self):
        """生成薪资对比报告"""
        try:
            self.comparison_text.delete(1.0, tk.END)

            # 计算所有模式的薪资
            old_salary = self.calculate_old_salary()
            mode1_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode1())
            mode2_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2())
            mode3_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode3())

            conversion_rate = self.calculate_conversion_rate()
            employee_type = self.employee_type.get()

            result = f"=== 薪资模式对比报告 ===\n\n"
            result += f"员工类型: {employee_type}\n"
            result += f"交付量: {self.delivery_amount.get()}\n"
            result += f"购买服务包数量: {self.purchase_amount.get()}\n"
            result += f"转化率: {conversion_rate:.2f}%\n\n"

            # 各模式薪资对比
            result += f"{'模式':<15} {'薪资(元)':<12} {'与旧模式差异(元)':<15} {'差异百分比':<12}\n"
            result += f"{'-' * 60}\n"

            modes = [
                ("旧薪资体系", old_salary),
                ("新保底", mode1_salary),
                ("新底薪（中）", mode2_salary),
                ("新底薪（低）", mode3_salary)
            ]

            for mode_name, salary in modes:
                if mode_name == "旧薪资体系":
                    diff = 0
                    diff_pct = 0
                else:
                    diff = salary - old_salary
                    diff_pct = (diff / old_salary) * 100 if old_salary != 0 else 0

                result += f"{mode_name:<15} {salary:<12.2f} {diff:<15.2f} {diff_pct:<12.2f}%\n"

            # 推荐最优模式
            best_salary = max(mode1_salary, mode2_salary, mode3_salary)
            best_modes = []
            if mode1_salary == best_salary:
                best_modes.append("新保底")
            if mode2_salary == best_salary:
                best_modes.append("新底薪（中）")
            if mode3_salary == best_salary:
                best_modes.append("新底薪（低）")

            result += f"\n=== 推荐方案 ===\n"
            result += f"推荐选择: {', '.join(best_modes)}\n"
            result += f"最高薪资: {best_salary:.2f}元\n"
            result += f"比旧模式多: {best_salary - old_salary:.2f}元\n"

            # 转化率影响分析
            min_rate = self.min_conversion_rate.get()
            if conversion_rate < min_rate:
                result += f"\n⚠️ 警告: 当前转化率({conversion_rate:.2f}%)低于要求({min_rate}%)，薪资已应用折扣\n"
                result += f"如果转化率达到{min_rate}%，薪资将有所提升\n"

            self.comparison_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("对比错误", f"生成对比报告时出现错误: {str(e)}")

    def analyze_store(self):
        """门店财务分析"""
        try:
            self.store_text.delete(1.0, tk.END)

            # 门店财务数据计算
            purchase = self.purchase_amount.get()
            service_price = self.service_price.get()
            service_cost = self.service_cost.get()
            staff_count = self.store_staff_count.get()
            city_cost = self.city_cost.get()

            # 计算各种薪资
            old_salary = self.calculate_old_salary()
            mode1_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode1())
            mode2_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2())
            mode3_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode3())

            # 门店财务指标
            total_revenue = purchase * service_price
            unit_profit = service_price - service_cost
            total_profit = purchase * unit_profit

            result = f"=== 门店财务分析报告 ===\n\n"
            result += f"=== 基础数据 ===\n"
            result += f"购买服务包数量: {purchase}\n"
            result += f"服务包单价: {service_price:.2f}元\n"
            result += f"服务包成本: {service_cost:.2f}元\n"
            result += f"门店人数: {staff_count}\n"
            result += f"城市平均成本: {city_cost:.2f}元\n\n"

            result += f"=== 门店财务指标 ===\n"
            result += f"门店总流水: {total_revenue:.2f}元\n"
            result += f"客单利润: {unit_profit:.2f}元\n"
            result += f"门店总利润: {total_profit:.2f}元\n\n"

            # 不同薪资模式下的成本分析
            result += f"=== 不同薪资模式下的成本分析 ===\n"

            salary_modes = [
                ("旧薪资体系", old_salary),
                ("新保底", mode1_salary),
                ("新底薪（中）", mode2_salary),
                ("新底薪（低）", mode3_salary)
            ]

            for mode_name, salary in salary_modes:
                total_salary_cost = salary * staff_count
                net_profit = total_profit - total_salary_cost - city_cost

                result += f"\n{mode_name}:\n"
                result += f"  单人薪资: {salary:.2f}元\n"
                result += f"  总薪资成本: {total_salary_cost:.2f}元\n"
                result += f"  净利润: {net_profit:.2f}元\n"

                if net_profit <= 0:
                    result += f"  ⚠️ 警告: 净利润为负，需要改善!\n"

                    # 计算打平成本需要的条件
                    break_even_packages = (total_salary_cost + city_cost) / unit_profit
                    current_conversion = self.calculate_conversion_rate()
                    current_delivery = self.delivery_amount.get()

                    if current_conversion > 0:
                        break_even_delivery = break_even_packages / (current_conversion / 100)
                        break_even_conversion = (break_even_packages / current_delivery) * 100

                        result += f"  需要购买 {break_even_packages:.0f} 个服务包才能打平成本\n"
                        result += f"  当前转化率不变，需要交付量达到 {break_even_delivery:.0f}\n"
                        result += f"  当前交付量不变，需要转化率达到 {break_even_conversion:.2f}%\n"

                        if (break_even_packages > purchase * 2 and
                                break_even_delivery > current_delivery * 2 and
                                break_even_conversion > current_conversion * 2):
                            result += f"  建议: 以上条件都难以达成，建议该员工只能选择新保底模式\n"
                else:
                    result += f"  ✓ 盈利状况良好\n"

            # 展示模块数据
            result += f"\n=== 展示模块数据 ({self.current_month.get()}) ===\n"
            result += f"平均总薪资: {self.avg_total_salary.get():.2f}元\n"
            result += f"平均交付量: {self.avg_delivery.get()}\n"
            result += f"平均购买服务包数: {self.avg_purchase.get()}\n"
            result += f"平均转化率: {self.avg_conversion_rate.get():.2f}%\n"

            self.store_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("分析错误", f"门店分析时出现错误: {str(e)}")

    def export_excel(self):
        """导出Excel报告"""
        try:
            from datetime import datetime

            # 计算所有模式的薪资
            old_salary = self.calculate_old_salary()
            mode1_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode1())
            mode2_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2())
            mode3_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode3())

            conversion_rate = self.calculate_conversion_rate()

            # 创建数据
            data = {
                '薪资模式': ['旧薪资体系', '新保底', '新底薪（中）', '新底薪（低）'],
                '薪资(元)': [old_salary, mode1_salary, mode2_salary, mode3_salary],
                '与旧模式差异(元)': [0, mode1_salary - old_salary, mode2_salary - old_salary,
                                     mode3_salary - old_salary],
                '差异百分比(%)': [0,
                                  ((mode1_salary - old_salary) / old_salary * 100) if old_salary != 0 else 0,
                                  ((mode2_salary - old_salary) / old_salary * 100) if old_salary != 0 else 0,
                                  ((mode3_salary - old_salary) / old_salary * 100) if old_salary != 0 else 0]
            }

            df = pd.DataFrame(data)

            # 基础信息
            info_data = {
                '项目': ['员工类型', '交付量', '购买服务包数量', '转化率(%)', '服务包单价', '服务包成本', '门店人数'],
                '数值': [self.employee_type.get(), self.delivery_amount.get(), self.purchase_amount.get(),
                         conversion_rate, self.service_price.get(), self.service_cost.get(),
                         self.store_staff_count.get()]
            }

            info_df = pd.DataFrame(info_data)

            # 门店财务数据
            purchase = self.purchase_amount.get()
            service_price = self.service_price.get()
            service_cost = self.service_cost.get()
            staff_count = self.store_staff_count.get()
            city_cost = self.city_cost.get()

            total_revenue = purchase * service_price
            unit_profit = service_price - service_cost
            total_profit = purchase * unit_profit

            finance_data = {
                '财务指标': ['门店总流水', '客单利润', '门店总利润', '城市平均成本'],
                '金额(元)': [total_revenue, unit_profit, total_profit, city_cost]
            }

            finance_df = pd.DataFrame(finance_data)

            # 保存到Excel
            filename = f"薪资对比报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = f"/home/ubuntu/{filename}"

            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                info_df.to_excel(writer, sheet_name='基础信息', index=False)
                df.to_excel(writer, sheet_name='薪资对比', index=False)
                finance_df.to_excel(writer, sheet_name='门店财务', index=False)

            messagebox.showinfo("导出成功", f"Excel报告已导出到: {filepath}")

        except Exception as e:
            messagebox.showerror("导出错误", f"导出Excel时出现错误: {str(e)}")

    def save_config(self):
        """保存参数配置"""
        try:
            config = {
                'delivery_amount': self.delivery_amount.get(),
                'purchase_amount': self.purchase_amount.get(),
                'service_price': self.service_price.get(),
                'service_cost': self.service_cost.get(),
                'store_staff_count': self.store_staff_count.get(),
                'old_base_salary': self.old_base_salary.get(),
                'old_basic_bonus': self.old_basic_bonus.get(),
                'old_position_bonus': self.old_position_bonus.get(),
                'old_extra_bonus': self.old_extra_bonus.get(),
                'new_base_salary_mid': self.new_base_salary_mid.get(),
                'new_base_salary_low': self.new_base_salary_low.get(),
                'old_purchase_baseline': self.old_purchase_baseline.get(),
                'planned_increase': self.planned_increase.get(),
                'new_bonus_coefficient': self.new_bonus_coefficient.get(),
                'min_conversion_rate': self.min_conversion_rate.get(),
                'penalty_rate': self.penalty_rate.get(),
                'current_month': self.current_month.get(),
                'avg_total_salary': self.avg_total_salary.get(),
                'avg_delivery': self.avg_delivery.get(),
                'avg_purchase': self.avg_purchase.get(),
                'avg_conversion_rate': self.avg_conversion_rate.get(),
                'city_cost': self.city_cost.get(),
                'employee_type': self.employee_type.get(),
                'salary_mode': self.salary_mode.get()
            }

            filename = f"salary_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = f"/home/ubuntu/{filename}"

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("保存成功", f"参数配置已保存到: {filepath}")

        except Exception as e:
            messagebox.showerror("保存错误", f"保存配置时出现错误: {str(e)}")

    def load_config(self):
        """加载参数配置"""
        try:
            filepath = filedialog.askopenfilename(
                title="选择配置文件",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if not filepath:
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 加载配置到界面
            self.delivery_amount.set(config.get('delivery_amount', 100))
            self.purchase_amount.set(config.get('purchase_amount', 50))
            self.service_price.set(config.get('service_price', 1000))
            self.service_cost.set(config.get('service_cost', 300))
            self.store_staff_count.set(config.get('store_staff_count', 5))
            self.old_base_salary.set(config.get('old_base_salary', 3000))
            self.old_basic_bonus.set(config.get('old_basic_bonus', 500))
            self.old_position_bonus.set(config.get('old_position_bonus', 300))
            self.old_extra_bonus.set(config.get('old_extra_bonus', 200))
            self.new_base_salary_mid.set(config.get('new_base_salary_mid', 3500))
            self.new_base_salary_low.set(config.get('new_base_salary_low', 2800))
            self.old_purchase_baseline.set(config.get('old_purchase_baseline', 40))
            self.planned_increase.set(config.get('planned_increase', 20))
            self.new_bonus_coefficient.set(config.get('new_bonus_coefficient', 1.2))
            self.min_conversion_rate.set(config.get('min_conversion_rate', 45))
            self.penalty_rate.set(config.get('penalty_rate', 0.8))
            self.current_month.set(config.get('current_month', datetime.now().strftime("%Y-%m")))
            self.avg_total_salary.set(config.get('avg_total_salary', 5000))
            self.avg_delivery.set(config.get('avg_delivery', 80))
            self.avg_purchase.set(config.get('avg_purchase', 40))
            self.avg_conversion_rate.set(config.get('avg_conversion_rate', 50))
            self.city_cost.set(config.get('city_cost', 10000))
            self.employee_type.set(config.get('employee_type', '员工'))
            self.salary_mode.set(config.get('salary_mode', '新保底'))

            messagebox.showinfo("加载成功", f"配置已从 {filepath} 加载")

        except Exception as e:
            messagebox.showerror("加载错误", f"加载配置时出现错误: {str(e)}")

    def generate_charts(self):
        """生成数据可视化图表"""
        try:
            # 计算所有模式的薪资
            old_salary = self.calculate_old_salary()
            mode1_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode1())
            mode2_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2())
            mode3_salary = self.apply_conversion_rate_penalty(self.calculate_new_salary_mode3())

            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False

            # 创建图表
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

            # 1. 薪资对比柱状图
            modes = ['旧薪资体系', '新保底', '新底薪（中）', '新底薪（低）']
            salaries = [old_salary, mode1_salary, mode2_salary, mode3_salary]
            colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

            bars = ax1.bar(modes, salaries, color=colors)
            ax1.set_title('薪资模式对比', fontsize=14, fontweight='bold')
            ax1.set_ylabel('薪资 (元)')
            ax1.tick_params(axis='x', rotation=45)

            # 在柱状图上添加数值标签
            for bar, salary in zip(bars, salaries):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + 50,
                         f'{salary:.0f}', ha='center', va='bottom')

            # 2. 薪资差异饼图
            differences = [mode1_salary - old_salary, mode2_salary - old_salary, mode3_salary - old_salary]
            positive_diffs = [max(0, diff) for diff in differences]

            if sum(positive_diffs) > 0:
                labels = ['新保底', '新底薪（中）', '新底薪（低）']
                ax2.pie(positive_diffs, labels=labels, autopct='%1.1f%%', startangle=90)
                ax2.set_title('薪资提升比例分布')
            else:
                ax2.text(0.5, 0.5, '所有新模式薪资\n均未超过旧模式',
                         ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('薪资提升比例分布')

            # 3. 转化率影响分析
            conversion_rates = [30, 40, 45, 50, 60, 70]
            old_salaries = []
            new_salaries = []

            original_conversion = self.calculate_conversion_rate()
            original_purchase = self.purchase_amount.get()
            original_delivery = self.delivery_amount.get()
            # 临时保存原始值
            original_conversion = self.calculate_conversion_rate()
            original_purchase = self.purchase_amount.get()
            original_delivery = self.delivery_amount.get()

            # 计算不同转化率下的薪资
            for rate in conversion_rates:
                # 设置新的转化率
                self.purchase_amount.set(original_delivery * rate / 100)
                # 计算薪资
                old_salaries.append(self.calculate_old_salary())
                new_salaries.append(self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2()))

            # 恢复原始值
            self.purchase_amount.set(original_purchase)
            self.delivery_amount.set(original_delivery)

            ax3.plot(conversion_rates, old_salaries, 'o-', label='旧薪资体系')
            ax3.plot(conversion_rates, new_salaries, 's-', label='新底薪（中）')
            ax3.set_title('转化率对薪资的影响')
            ax3.set_xlabel('转化率 (%)')
            ax3.set_ylabel('薪资 (元)')
            ax3.legend()
            ax3.grid(True)

            # 4. 购买量对薪资的影响
            purchase_amounts = [20, 40, 60, 80, 100, 120]
            old_salaries = []
            new_salaries = []

            # 计算不同购买量下的薪资
            for amount in purchase_amounts:
                self.purchase_amount.set(amount)
                # 计算薪资
                old_salaries.append(self.calculate_old_salary())
                new_salaries.append(self.apply_conversion_rate_penalty(self.calculate_new_salary_mode2()))

            # 恢复原始值
            self.purchase_amount.set(original_purchase)

            ax4.plot(purchase_amounts, old_salaries, 'o-', label='旧薪资体系')
            ax4.plot(purchase_amounts, new_salaries, 's-', label='新底薪（中）')
            ax4.set_title('购买量对薪资的影响')
            ax4.set_xlabel('购买服务包数量')
            ax4.set_ylabel('薪资 (元)')
            ax4.legend()
            ax4.grid(True)

            # 调整布局
            plt.tight_layout()

            # 保存图表
            filename = f"薪资分析图表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            chart_path = f"/home/ubuntu/{filename}"
            plt.savefig(chart_path)
            plt.close()

            # 在文本框中显示图表信息
            self.viz_text.delete(1.0, tk.END)
            chart_info = f"图表已生成并保存到: {chart_path}\n\n"
            chart_info += "图表说明:\n"
            chart_info += "1. 薪资模式对比: 直观展示不同薪资模式下的薪资水平\n"
            chart_info += "2. 薪资提升比例分布: 展示新模式相比旧模式的薪资提升比例\n"
            chart_info += "3. 转化率对薪资的影响: 分析转化率变化对薪资的影响趋势\n"
            chart_info += "4. 购买量对薪资的影响: 分析购买服务包数量变化对薪资的影响趋势\n\n"

            chart_info += f"当前参数:\n"
            chart_info += f"员工类型: {self.employee_type.get()}\n"
            chart_info += f"选择模式: {self.salary_mode.get()}\n"
            chart_info += f"转化率: {self.calculate_conversion_rate():.2f}%\n"
            chart_info += f"交付量: {self.delivery_amount.get()}\n"
            chart_info += f"购买服务包数量: {self.purchase_amount.get()}\n"

            chart_info += "\n建议:\n"
            chart_info += "根据图表分析结果，选择最适合的薪资模式和业务策略。"

            self.viz_text.insert(tk.END, chart_info)

            messagebox.showinfo("图表生成成功", f"数据可视化图表已保存到: {chart_path}")

        except Exception as e:
            messagebox.showerror("图表生成错误", f"生成图表时出现错误: {str(e)}")

def main():
    root = tk.Tk()
    app = SalaryCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()