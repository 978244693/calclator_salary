import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
from datetime import datetime


class SalaryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("薪资计算器")
        self.root.geometry("1200x800")  # 扩大窗口以适应新内容

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
        self.purchase_amount = tk.DoubleVar(value=50.0)
        self.service_price = tk.DoubleVar(value=1000.0)
        self.service_cost = tk.DoubleVar(value=300.0)

        # 员工类型和数量
        self.employee_count = tk.IntVar(value=2)
        self.supervisor_count = tk.IntVar(value=1)
        self.consultant_count = tk.IntVar(value=0)
        self.regional_manager_count = tk.IntVar(value=0)

        self.city_manager_count = tk.IntVar(value=0)

        # 职位补贴
        self.supervisor_bonus = tk.DoubleVar(value=500.0)
        self.consultant_bonus = tk.DoubleVar(value=800.0)
        self.regional_manager_bonus = tk.DoubleVar(value=1200.0)
        self.city_manager_bonus = tk.DoubleVar(value=1500.0)

        # 员工类型选择（用于计算单个员工薪资）
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

        # 三档提成配置
        self.bonus_tier1_threshold = tk.DoubleVar(value=0.9)  # 90%
        self.bonus_tier1_amount = tk.DoubleVar(value=7.5)  # 档1每包提成
        self.bonus_tier2_threshold = tk.DoubleVar(value=1.0)  # 100%
        self.bonus_tier2_amount = tk.DoubleVar(value=50.0)  # 档2每包提成
        self.bonus_tier3_amount = tk.DoubleVar(value=60.0)  # 档3每包提成

        self.min_conversion_rate = tk.DoubleVar(value=45.0)
        self.penalty_rate = tk.DoubleVar(value=0.8)
        self.salary_mode = tk.StringVar(value="新保底")
        self.new_purchase_amount = tk.DoubleVar(value=0.0)

        # 社保参数
        self.social_insurance_base = tk.DoubleVar(value=10000.0)  # 社保基数
        self.pension_rate = tk.DoubleVar(value=8.0)  # 养老保险比例
        self.medical_rate = tk.DoubleVar(value=2.0)  # 医疗保险比例
        self.unemployment_rate = tk.DoubleVar(value=0.2)  # 失业保险比例
        self.injury_rate = tk.DoubleVar(value=0.0)  # 工伤保险比例
        self.maternity_rate = tk.DoubleVar(value=0.0)  # 生育保险比例
        self.housing_fund_rate = tk.DoubleVar(value=12.0)  # 住房公积金比例

        # 展示模块参数
        self.current_month = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        self.avg_total_salary = tk.DoubleVar(value=5000.0)
        self.avg_delivery = tk.DoubleVar(value=80.0)
        self.avg_purchase = tk.DoubleVar(value=40.0)
        self.avg_conversion_rate = tk.DoubleVar(value=50.0)
        self.city_cost = tk.DoubleVar(value=10000.0)

    def update_tier1_bonus(self):
        old_base = self.old_base_salary.get()
        mode = self.salary_mode.get()
        if mode == "新底薪（中）":
            new_base = self.new_base_salary_mid.get()
        elif mode == "新底薪（低）":
            new_base = self.new_base_salary_low.get()
        else:
            new_base = self.new_base_salary_mid.get()  # 默认给个值
        old_baseline = self.old_purchase_baseline.get()
        tier1 = (old_base - new_base) / old_baseline if old_baseline else 0
        self.bonus_tier1_amount.set(tier1)

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
        self.create_formula_tab()  # 公式说明标签页
        self.create_social_insurance_tab()  # 新增社保计算标签页
        self.old_base_salary.trace_add("write", lambda *a: self.update_tier1_bonus())
        self.new_base_salary_mid.trace_add("write", lambda *a: self.update_tier1_bonus())
        self.new_base_salary_low.trace_add("write", lambda *a: self.update_tier1_bonus())
        self.old_purchase_baseline.trace_add("write", lambda *a: self.update_tier1_bonus())
        self.salary_mode.trace_add("write", lambda *a: self.update_tier1_bonus())
        self.update_tier1_bonus()


    def create_social_insurance_tab(self):
        """创建社保计算标签页"""
        self.social_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.social_frame, text="社保计算")

        # 创建滚动框架
        canvas = tk.Canvas(self.social_frame)
        scrollbar = ttk.Scrollbar(self.social_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 社保参数组
        insurance_group = ttk.LabelFrame(scrollable_frame, text="社保参数设置", padding=10)
        insurance_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(insurance_group, text="社保基数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.social_insurance_base, width=15).grid(row=0, column=1, padx=5,
                                                                                           pady=2)

        ttk.Label(insurance_group, text="养老保险比例(%):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.pension_rate, width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(insurance_group, text="医疗保险比例(%):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.medical_rate, width=15).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(insurance_group, text="失业保险比例(%):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.unemployment_rate, width=15).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(insurance_group, text="工伤保险比例(%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.injury_rate, width=15).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(insurance_group, text="生育保险比例(%):").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.maternity_rate, width=15).grid(row=2, column=3, padx=5, pady=2)

        ttk.Label(insurance_group, text="住房公积金比例(%):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(insurance_group, textvariable=self.housing_fund_rate, width=15).grid(row=3, column=1, padx=5, pady=2)

        # 计算按钮
        calc_button = ttk.Button(insurance_group, text="计算社保", command=self.calculate_social_insurance)
        calc_button.grid(row=3, column=2, columnspan=2, pady=10)

        # 结果显示区域
        result_frame = ttk.LabelFrame(scrollable_frame, text="社保计算结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建结果显示的文本框
        self.social_result_text = tk.Text(result_frame, height=15, width=80)
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.social_result_text.yview)
        self.social_result_text.configure(yscrollcommand=result_scrollbar.set)

        self.social_result_text.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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

        # 1. 薪资模式选择（直接加在最上面！）
        salary_mode_group = ttk.LabelFrame(scrollable_frame, text="薪资模式")
        salary_mode_group.pack(fill=tk.X, padx=5, pady=5)

        self.salary_mode = tk.StringVar()
        self.salary_mode.set("新保底")  # 默认值

        mode_list = [("新保底", "新保底"), ("新底薪（中）", "新底薪（中）"), ("新底薪（低）", "新底薪（低）")]
        for idx, (text, value) in enumerate(mode_list):
            ttk.Radiobutton(
                salary_mode_group, text=text, variable=self.salary_mode, value=value
            ).grid(row=0, column=idx, padx=10, pady=2)

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

        # 员工数量配置
        staff_group = ttk.LabelFrame(scrollable_frame, text="门店人员配置", padding=10)
        staff_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(staff_group, text="员工数量:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(staff_group, textvariable=self.employee_count, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(staff_group, text="主管数量:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(staff_group, textvariable=self.supervisor_count, width=10).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(staff_group, text="顾问数量:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(staff_group, textvariable=self.consultant_count, width=10).grid(row=0, column=5, padx=5, pady=2)

        ttk.Label(staff_group, text="区总数量:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(staff_group, textvariable=self.regional_manager_count, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(staff_group, text="市总数量:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(staff_group, textvariable=self.city_manager_count, width=10).grid(row=1, column=3, padx=5, pady=2)

        # 职位补贴配置
        bonus_group = ttk.LabelFrame(scrollable_frame, text="职位补贴配置", padding=10)
        bonus_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(bonus_group, text="主管补贴:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(bonus_group, textvariable=self.supervisor_bonus, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(bonus_group, text="顾问补贴:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(bonus_group, textvariable=self.consultant_bonus, width=10).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(bonus_group, text="区总补贴:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(bonus_group, textvariable=self.regional_manager_bonus, width=10).grid(row=0, column=5, padx=5, pady=2)

        ttk.Label(bonus_group, text="市总补贴:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(bonus_group, textvariable=self.city_manager_bonus, width=10).grid(row=0, column=7, padx=5, pady=2)

        # 员工类型选择（用于计算单个员工薪资）
        employee_type_group = ttk.LabelFrame(scrollable_frame, text="员工类型选择", padding=10)
        employee_type_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(employee_type_group, text="计算类型:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        employee_combo = ttk.Combobox(employee_type_group, textvariable=self.employee_type,
                                      values=["员工", "主管", "顾问", "区总", "市总"], width=12)
        employee_combo.grid(row=0, column=1, padx=5, pady=2)
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

        ttk.Label(new_salary_group, text="档1占比阈值(%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier1_threshold, width=15).grid(row=2, column=1, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="档2占比阈值(%):").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier2_threshold, width=15).grid(row=2, column=3, padx=5,
                                                                                            pady=2)

        ttk.Label(new_salary_group, text="档1每包提成:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        tier1_entry = ttk.Entry(new_salary_group, textvariable=self.bonus_tier1_amount, width=15, state="readonly")
        tier1_entry.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(new_salary_group, text="档2每包提成:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier2_amount, width=15).grid(row=3, column=3, padx=5,
                                                                                         pady=2)

        ttk.Label(new_salary_group, text="档3每包提成:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.bonus_tier3_amount, width=15).grid(row=4, column=1, padx=5,
                                                                                         pady=2)

        ttk.Label(new_salary_group, text="新服务包购买数量:").grid(row=4, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.new_purchase_amount, width=15).grid(row=4, column=3, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="下线转化率(%):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.min_conversion_rate, width=15).grid(row=5, column=1, padx=5,
                                                                                          pady=2)

        ttk.Label(new_salary_group, text="未达标折扣率:").grid(row=5, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(new_salary_group, textvariable=self.penalty_rate, width=15).grid(row=5, column=3, padx=5, pady=2)

        # 展示模块参数组
        display_group = ttk.LabelFrame(scrollable_frame, text="展示模块参数", padding=10)
        display_group.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(display_group, text="当前月份:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(display_group, textvariable=self.current_month, width=15).grid(row=0, column=5, padx=5, pady=2)

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

        # 薪资模式选择（属于当前薪资计算tab页，不是参数设置tab）
        salary_mode_group = ttk.LabelFrame(self.calc_frame, text="薪资模式")
        salary_mode_group.pack(fill=tk.X, padx=10, pady=10)

        # 注意：如果self.salary_mode已在别处定义，下面两行可以不要
        self.salary_mode = tk.StringVar()
        self.salary_mode.set("新保底")  # 默认值

        mode_list = [("新保底", "新保底"), ("新底薪（中）", "新底薪（中）"), ("新底薪（低）", "新底薪（低）")]
        for idx, (text, value) in enumerate(mode_list):
            ttk.Radiobutton(
                salary_mode_group, text=text, variable=self.salary_mode, value=value
            ).grid(row=0, column=idx, padx=10, pady=2)

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

        # 计算按钮（这里加一个按钮区Frame，更清晰）
        button_frame = ttk.Frame(self.calc_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        calc_button = ttk.Button(button_frame, text="计算薪资", command=self.calculate_salary)
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

        主管、顾问、区总、市总额外有岗位补贴:
            主管补贴: XXX元, 顾问补贴: XXX元, 区总补贴: XXX元, 市总补贴: XXX元

     3. 新薪资体系计算公式（模式二/三）:

    A. 新保底模式（模式一）:
       使用旧薪资计算公式。

    B. 新底薪（中）模式（模式二）与 新底薪（低）模式（模式三）:
       新薪资 = 新底薪 + 三档提成总额

       三档提成逻辑如下（以旧底薪为基准）：

       - 档1: 服务包数量 ≤ 阈值1 (如90%)
          提成 = 服务包数量 × 档1每包提成

       - 档2: 阈值1 < 服务包数量 ≤ 阈值2 (如100%)
          提成 = (阈值1数量 × 档1每包提成) + (超过部分 × 档2每包提成)

       - 档3: 服务包数量 > 阈值2
          提成 = (阈值1数量 × 档1每包提成) + (阈值2内数量 × 档2每包提成) + (超过部分 × 档3每包提成)

       如果转化率低于下线值，则提成总额 × 折扣比例（如0.8）

     4. 门店财务分析公式:
        门店总流水 = 购买服务包数量 × 服务包单价
        客单利润 = 服务包单价 - 服务包必要支出
        门店总利润 = 购买服务包数量 × 客单利润
        门店总成本 = (员工工资×数量 + 主管工资×数量 + 顾问工资×数量 + 区总工资×数量 + 市总工资×数量) + 社保成本
        净利润 = 门店总利润 - 门店总成本 - 城市平均成本
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
        """更新底薪显示值"""
        try:
            # 安全获取旧底薪值
            old_base = self.old_base_salary.get()
            self.old_base_display.config(text=f"{float(old_base):.2f}")
        except Exception:
            self.old_base_display.config(text="0.00")

        try:
            # 安全获取中底薪值
            mid_base = self.new_base_salary_mid.get()
            self.mid_base_display.config(text=f"{float(mid_base):.2f}")
        except Exception:
            self.mid_base_display.config(text="0.00")

        try:
            # 安全获取低底薪值
            low_base = self.new_base_salary_low.get()
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
        staff_count = self.employee_count.get() + self.supervisor_count.get() + self.consultant_count.get() + self.regional_manager_count.get() + self.city_manager_count.get()

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

        # 根据职位添加补贴
        if self.employee_type.get() == "主管":
            salary += self.supervisor_bonus.get()
        elif self.employee_type.get() == "顾问":
            salary += self.consultant_bonus.get()
        elif self.employee_type.get() == "区总":
            salary += self.regional_manager_bonus.get()
        elif self.employee_type.get() == "市总":
            salary += self.city_manager_bonus.get()

        return salary

    def calculate_new_salary_mode1(self, return_detail=False, role=None):
        """
        新薪资体系模式一：新保底（与旧薪资相同，只有底薪，没有提成和补贴）
        return_detail=True时返回(底薪, 提成, 补贴)
        """
        if role is not None:
            self.employee_type.set(role)
        salary = self.calculate_old_salary()
        if return_detail:
            return salary, 0, 0  # 只算底薪，没有提成和补贴
        else:
            return salary

    def calculate_new_salary_mode2(self, return_detail=False, role=None):
        """
        新薪资体系模式二：新底薪（中），三档提成+补贴
        return_detail=True时返回(底薪, 提成, 补贴)
        """
        if role is not None:
            self.employee_type.set(role)
        purchase_amount = self.new_purchase_amount.get() or self.purchase_amount.get()
        old_purchase_baseline = self.old_purchase_baseline.get()
        new_base = self.new_base_salary_mid.get()  # 新底薪（中）
        old_base = self.old_base_salary.get()  # 旧底薪

        tier1_threshold = old_purchase_baseline * self.bonus_tier1_threshold.get()
        tier2_threshold = old_purchase_baseline * self.bonus_tier2_threshold.get()

        # 档1每包提成 = (旧底薪 - 新底薪) ➗ 旧购买服务包数
        tier1_amount = (old_base - new_base) / old_purchase_baseline if old_purchase_baseline else 0
        tier2_amount = self.bonus_tier2_amount.get()
        tier3_amount = self.bonus_tier3_amount.get()

        # 计算三档提成
        if purchase_amount <= tier1_threshold:
            bonus = purchase_amount * tier1_amount
        elif purchase_amount <= tier2_threshold:
            bonus = (tier1_threshold * tier1_amount) + ((purchase_amount - tier1_threshold) * tier2_amount)
        else:
            bonus = (tier1_threshold * tier1_amount) + ((tier2_threshold - tier1_threshold) * tier2_amount) + (
                    (purchase_amount - tier2_threshold) * tier3_amount)

        # 转化率未达标，提成部分打折
        bonus = self.apply_conversion_rate_penalty_to_bonus(bonus)

        # 补贴（不同角色不同）
        subsidy = 0
        emp_type = self.employee_type.get()
        if emp_type == "主管":
            subsidy = self.supervisor_bonus.get()
        elif emp_type == "顾问":
            subsidy = self.consultant_bonus.get()
        elif emp_type == "区总":
            subsidy = self.regional_manager_bonus.get()
        elif emp_type == "市总":
            subsidy = self.city_manager_bonus.get()

        if return_detail:
            return new_base, bonus, subsidy  # 底薪、提成、补贴
        else:
            return new_base + bonus + subsidy

    def calculate_new_salary_mode3(self, return_detail=False, role=None):
        """
        新薪资体系模式三：新底薪（低），三档提成+补贴
        return_detail=True时返回(底薪, 提成, 补贴)
        """
        if role is not None:
            self.employee_type.set(role)
        purchase_amount = self.new_purchase_amount.get() or self.purchase_amount.get()
        old_purchase_baseline = self.old_purchase_baseline.get()
        new_base = self.new_base_salary_low.get()  # 新底薪（低）
        old_base = self.old_base_salary.get()  # 旧底薪

        tier1_threshold = old_purchase_baseline * self.bonus_tier1_threshold.get()
        tier2_threshold = old_purchase_baseline * self.bonus_tier2_threshold.get()

        # 档1每包提成 = (旧底薪 - 新底薪) ➗ 旧购买服务包数
        tier1_amount = (old_base - new_base) / old_purchase_baseline if old_purchase_baseline else 0
        tier2_amount = self.bonus_tier2_amount.get()
        tier3_amount = self.bonus_tier3_amount.get()

        # 计算三档提成
        if purchase_amount <= tier1_threshold:
            bonus = purchase_amount * tier1_amount
        elif purchase_amount <= tier2_threshold:
            bonus = (tier1_threshold * tier1_amount) + ((purchase_amount - tier1_threshold) * tier2_amount)
        else:
            bonus = (tier1_threshold * tier1_amount) + ((tier2_threshold - tier1_threshold) * tier2_amount) + (
                    (purchase_amount - tier2_threshold) * tier3_amount)

        # 转化率未达标，提成部分打折
        bonus = self.apply_conversion_rate_penalty_to_bonus(bonus)

        # 补贴（不同角色不同）
        subsidy = 0
        emp_type = self.employee_type.get()
        if emp_type == "主管":
            subsidy = self.supervisor_bonus.get()
        elif emp_type == "顾问":
            subsidy = self.consultant_bonus.get()
        elif emp_type == "区总":
            subsidy = self.regional_manager_bonus.get()
        elif emp_type == "市总":
            subsidy = self.city_manager_bonus.get()

        if return_detail:
            return new_base, bonus, subsidy  # 底薪、提成、补贴
        else:
            return new_base + bonus + subsidy

    def format_formula(self, formula: str, values: dict, result: float, unit: str = "元"):
        formula = formula.replace("/", "➗")
        value_str = "，".join([f"{k}={v}" for k, v in values.items()])
        return f"公式：{formula}\n代入：{value_str}\n结果：{result:.2f}{unit}\n"

    def apply_conversion_rate_penalty_to_bonus(self, bonus):
        """应用转化率未达标的折扣（仅对提成部分）"""
        conversion_rate = self.calculate_conversion_rate()
        min_rate = self.min_conversion_rate.get()
        penalty_rate = self.penalty_rate.get()

        if conversion_rate < min_rate:
            return bonus * penalty_rate
        return bonus

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

            result = f"=== 薪资计算详细步骤 ===\n\n"
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
                result += f"新保底模式薪资: {new_salary:.2f}元\n"
            elif salary_mode == "新底薪（中）":
                new_salary = self.calculate_new_salary_mode2()
                result += f"新底薪（中）模式薪资: {new_salary:.2f}元\n"
            else:  # 新底薪（低）
                new_salary = self.calculate_new_salary_mode3()
                result += f"新底薪（低）模式薪资: {new_salary:.2f}元\n"

            # 薪资差异分析
            difference = new_salary - old_salary
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
            mode1_salary = self.calculate_new_salary_mode1()
            mode2_salary = self.calculate_new_salary_mode2()
            mode3_salary = self.calculate_new_salary_mode3()

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
                result += f"\n⚠️ 警告: 当前转化率({conversion_rate:.2f}%)低于要求({min_rate}%)，提成已应用折扣\n"
                result += f"如果转化率达到{min_rate}%，提成将有所提升\n"

            self.comparison_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("对比错误", f"生成对比报告时出现错误: {str(e)}")

    def calculate_social_insurance(self):
        """计算社保费用"""
        try:
            self.social_result_text.delete(1.0, tk.END)

            base = self.social_insurance_base.get()
            pension = base * (self.pension_rate.get() / 100)
            medical = base * (self.medical_rate.get() / 100)
            unemployment = base * (self.unemployment_rate.get() / 100)
            injury = base * (self.injury_rate.get() / 100)
            maternity = base * (self.maternity_rate.get() / 100)
            housing_fund = base * (self.housing_fund_rate.get() / 100)

            total_per_employee = pension + medical + unemployment + injury + maternity + housing_fund

            total_staff = (self.employee_count.get() + self.supervisor_count.get() +
                           self.consultant_count.get() + self.regional_manager_count.get() +
                           self.city_manager_count.get())

            total_cost = total_per_employee * total_staff

            result = "=== 社保计算结果 ===\n\n"
            result += f"社保基数: {base:.2f}元\n"
            result += f"养老保险: {pension:.2f}元 (费率: {self.pension_rate.get()}%)\n"
            result += f"医疗保险: {medical:.2f}元 (费率: {self.medical_rate.get()}%)\n"
            result += f"失业保险: {unemployment:.2f}元 (费率: {self.unemployment_rate.get()}%)\n"
            result += f"工伤保险: {injury:.2f}元 (费率: {self.injury_rate.get()}%)\n"
            result += f"生育保险: {maternity:.2f}元 (费率: {self.maternity_rate.get()}%)\n"
            result += f"住房公积金: {housing_fund:.2f}元 (费率: {self.housing_fund_rate.get()}%)\n"
            result += f"每位员工社保成本: {total_per_employee:.2f}元\n"
            result += f"总员工数: {total_staff}人\n"
            result += f"社保总成本: {total_cost:.2f}元\n"

            self.social_result_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("社保计算错误", f"计算社保时出现错误: {str(e)}")

    def safe_get(self, var, default=0):
        """兼容tk变量.get()空字符串或异常，保证返回数字"""
        try:
            v = var.get()
            if isinstance(v, str) and v.strip() == "":
                return default
            return v
        except Exception:
            return default
    def analyze_store(self):
        """门店财务分析报告-多模式对比+分项明细+完整指标"""
        try:
            self.store_text.delete(1.0, tk.END)

            # === 基础参数 ===
            purchase = self.safe_get(self.purchase_amount)
            service_price = self.safe_get(self.service_price)
            service_cost = self.safe_get(self.service_cost)
            city_cost = self.safe_get(self.city_cost)

            employees = int(self.safe_get(self.employee_count))
            supervisors = int(self.safe_get(self.supervisor_count))
            consultants = int(self.safe_get(self.consultant_count))
            regional_managers = int(self.safe_get(self.regional_manager_count))
            city_managers = int(self.safe_get(self.city_manager_count))
            total_staff = employees + supervisors + consultants + regional_managers + city_managers

            base = self.safe_get(self.social_insurance_base)
            pension = base * self.safe_get(self.pension_rate) / 100
            medical = base * self.safe_get(self.medical_rate) / 100
            unemployment = base * self.safe_get(self.unemployment_rate) / 100
            injury = base * self.safe_get(self.injury_rate) / 100
            maternity = base * self.safe_get(self.maternity_rate) / 100
            housing_fund = base * self.safe_get(self.housing_fund_rate) / 100
            social_per_employee = pension + medical + unemployment + injury + maternity + housing_fund
            social_total_cost = social_per_employee * total_staff

            total_revenue = purchase * service_price
            unit_profit = service_price - service_cost
            total_profit = purchase * unit_profit

            # ====== 开头基础信息 ======
            result = "=== 门店财务分析报告 ===\n\n"

            result += "=== 基础数据 ===\n"
            result += f"购买服务包数量: {purchase}\n"
            result += f"服务包单价: {service_price:.2f}元\n"
            result += f"服务包成本: {service_cost:.2f}元\n"
            result += f"城市平均成本: {city_cost:.2f}元\n\n"

            result += "=== 人员配置 ===\n"
            result += f"员工数量: {employees}\n"
            result += f"主管数量: {supervisors}\n"
            result += f"顾问数量: {consultants}\n"
            result += f"区总数量: {regional_managers}\n"
            result += f"市总数量: {city_managers}\n"
            result += f"总人数: {total_staff}\n\n"

            result += "=== 社保成本 ===\n"
            result += f"社保基数: {base:.2f}元\n"
            result += f"每人社保成本: {social_per_employee:.2f}元\n"
            result += f"社保总成本: {social_total_cost:.2f}元\n\n"

            result += "=== 门店财务指标 ===\n"
            result += f"门店总流水: {total_revenue:.2f}元\n"
            result += f"客单利润: {unit_profit:.2f}元\n"
            result += f"门店总利润: {total_profit:.2f}元\n\n"

            result += "=== 不同薪资模式下的成本分析 ===\n\n"

            # ==== 定义薪资模式列表 ====
            modes = [
                ("旧薪资体系", lambda role: (self.employee_type.set(role) or (self.calculate_old_salary(), 0, 0)),
                 "旧薪资体系"),
                ("新保底", lambda role: self.calculate_new_salary_mode1(return_detail=True, role=role), "新保底"),
                ("新底薪（中）", lambda role: self.calculate_new_salary_mode2(return_detail=True, role=role),
                 "新底薪（中）"),
                (
                "新底薪（低）", lambda role: self.calculate_new_salary_mode3(return_detail=True, role=role), "新底薪（低）")
            ]
            employee_roles = [
                ("员工", employees),
                ("主管", supervisors),
                ("顾问", consultants),
                ("区总", regional_managers),
                ("市总", city_managers)
            ]

            for mode_name, calc_func, _ in modes:
                result += f"{mode_name}:\n"
                # 统计总薪资
                total_salary = 0
                detail_lines = []
                for role, count in employee_roles:
                    if count == 0:
                        salary, bonus, subsidy = 0, 0, 0
                    else:
                        salary, bonus, subsidy = calc_func(role)
                    per_total = (salary + bonus + subsidy) * count

                    # 分项明细（仅新体系分底薪/提成/补贴）
                    if mode_name == "旧薪资体系":
                        detail_lines.append(
                            f"  {role}薪资: {salary:.2f}元 × {count}人 = {salary * count:.2f}元"
                        )
                        total_salary += salary * count
                    else:
                        detail_lines.append(
                            f"  {role}底薪: {salary:.2f}元 × {count}人 = {salary * count:.2f}元"
                        )
                        detail_lines.append(
                            f"  {role}提成: {bonus:.2f}元 × {count}人 = {bonus * count:.2f}元"
                        )
                        detail_lines.append(
                            f"  {role}补贴: {subsidy:.2f}元 × {count}人 = {subsidy * count:.2f}元"
                        )
                        total_salary += (salary + bonus + subsidy) * count

                # 汇总
                result += "\n".join(detail_lines) + "\n"
                result += f"  总薪资成本: {total_salary:.2f}元\n"
                result += f"  社保成本: {social_total_cost:.2f}元\n"
                total_cost = total_salary + social_total_cost + city_cost
                result += f"  总成本: {total_cost:.2f}元 (薪资+社保+城市成本)\n"
                net_profit = total_profit - total_cost
                result += f"  净利润: {net_profit:.2f}元\n"
                if net_profit > 0:
                    result += "  ✓ 盈利状况良好\n\n"
                else:
                    result += "  ✗ 盈利需优化\n\n"

            self.store_text.insert(tk.END, result)
        except Exception as e:
            import traceback
            self.store_text.insert(tk.END, f"分析时发生错误:\n{e}\n{traceback.format_exc()}")

    def export_excel(self):
        """导出Excel报告"""
        try:
            # 获取当前时间作为文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"薪资计算报告_{timestamp}.xlsx"

            # 询问用户保存位置
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
                initialfile=filename
            )

            if not file_path:
                return  # 用户取消了保存

            # 创建Excel写入器
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

            # 收集所有数据
            data = {
                "基础参数": {
                    "交付量": self.delivery_amount.get(),
                    "购买服务包数量": self.purchase_amount.get(),
                    "服务包单价": self.service_price.get(),
                    "服务包必要支出": self.service_cost.get(),
                },
                "人员配置": {
                    "员工数量": self.employee_count.get(),
                    "主管数量": self.supervisor_count.get(),
                    "顾问数量": self.consultant_count.get(),
                    "区总数量": self.regional_manager_count.get(),
                    "市总数量": self.city_manager_count.get(),
                },
                "职位补贴": {
                    "主管补贴": self.supervisor_bonus.get(),
                    "顾问补贴": self.consultant_bonus.get(),
                    "区总补贴": self.regional_manager_bonus.get(),
                    "市总补贴": self.city_manager_bonus.get(),
                },
                "旧薪资体系": {
                    "底薪": self.old_base_salary.get(),
                    "基本绩效": self.old_basic_bonus.get(),
                    "岗位绩效": self.old_position_bonus.get(),
                    "奖金": self.old_extra_bonus.get(),
                },
                "新薪资体系": {
                    "新底薪（中）": self.new_base_salary_mid.get(),
                    "新底薪（低）": self.new_base_salary_low.get(),
                    "旧购买服务包基准": self.old_purchase_baseline.get(),
                    "档1占比阈值": self.bonus_tier1_threshold.get(),
                    "档2占比阈值": self.bonus_tier2_threshold.get(),
                    "档1每包提成": self.bonus_tier1_amount.get(),
                    "档2每包提成": self.bonus_tier2_amount.get(),
                    "档3每包提成": self.bonus_tier3_amount.get(),
                    "新服务包购买数量": self.new_purchase_amount.get(),
                    "下线转化率": self.min_conversion_rate.get(),
                    "未达标折扣率": self.penalty_rate.get(),
                },
                "社保参数": {
                    "社保基数": self.social_insurance_base.get(),
                    "养老保险比例": self.pension_rate.get(),
                    "医疗保险比例": self.medical_rate.get(),
                    "失业保险比例": self.unemployment_rate.get(),
                    "工伤保险比例": self.injury_rate.get(),
                    "生育保险比例": self.maternity_rate.get(),
                    "住房公积金比例": self.housing_fund_rate.get(),
                },
                "展示模块": {
                    "当前月份": self.current_month.get(),
                    "平均总薪资": self.avg_total_salary.get(),
                    "平均交付量": self.avg_delivery.get(),
                    "平均购买服务包数": self.avg_purchase.get(),
                    "平均转化率": self.avg_conversion_rate.get(),
                    "城市平均成本": self.city_cost.get(),
                }
            }

            # 将数据写入Excel的不同工作表
            for sheet_name, sheet_data in data.items():
                df = pd.DataFrame(list(sheet_data.items()), columns=["参数", "值"])
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            # 保存Excel文件
            writer.close()
            messagebox.showinfo("导出成功", f"报告已成功导出到: {file_path}")

        except Exception as e:
            messagebox.showerror("导出错误", f"导出Excel时出现错误: {str(e)}")

    def save_config(self):
        """保存参数配置"""
        try:
            # 获取所有变量值
            config = {
                "delivery_amount": self.delivery_amount.get(),
                "purchase_amount": self.purchase_amount.get(),
                "service_price": self.service_price.get(),
                "service_cost": self.service_cost.get(),
                "employee_count": self.employee_count.get(),
                "supervisor_count": self.supervisor_count.get(),
                "consultant_count": self.consultant_count.get(),
                "regional_manager_count": self.regional_manager_count.get(),
                "city_manager_count": self.city_manager_count.get(),
                "supervisor_bonus": self.supervisor_bonus.get(),
                "consultant_bonus": self.consultant_bonus.get(),
                "regional_manager_bonus": self.regional_manager_bonus.get(),
                "city_manager_bonus": self.city_manager_bonus.get(),
                "employee_type": self.employee_type.get(),
                "old_base_salary": self.old_base_salary.get(),
                "old_basic_bonus": self.old_basic_bonus.get(),
                "old_position_bonus": self.old_position_bonus.get(),
                "old_extra_bonus": self.old_extra_bonus.get(),
                "new_base_salary_mid": self.new_base_salary_mid.get(),
                "new_base_salary_low": self.new_base_salary_low.get(),
                "old_purchase_baseline": self.old_purchase_baseline.get(),
                "bonus_tier1_threshold": self.bonus_tier1_threshold.get(),
                "bonus_tier1_amount": self.bonus_tier1_amount.get(),
                "bonus_tier2_threshold": self.bonus_tier2_threshold.get(),
                "bonus_tier2_amount": self.bonus_tier2_amount.get(),
                "bonus_tier3_amount": self.bonus_tier3_amount.get(),
                "new_purchase_amount": self.new_purchase_amount.get(),
                "min_conversion_rate": self.min_conversion_rate.get(),
                "penalty_rate": self.penalty_rate.get(),
                "salary_mode": self.salary_mode.get(),
                "social_insurance_base": self.social_insurance_base.get(),
                "pension_rate": self.pension_rate.get(),
                "medical_rate": self.medical_rate.get(),
                "unemployment_rate": self.unemployment_rate.get(),
                "injury_rate": self.injury_rate.get(),
                "maternity_rate": self.maternity_rate.get(),
                "housing_fund_rate": self.housing_fund_rate.get(),
                "current_month": self.current_month.get(),
                "avg_total_salary": self.avg_total_salary.get(),
                "avg_delivery": self.avg_delivery.get(),
                "avg_purchase": self.avg_purchase.get(),
                "avg_conversion_rate": self.avg_conversion_rate.get(),
                "city_cost": self.city_cost.get(),
            }

            # 询问保存位置
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
                initialfile="薪资计算器配置.json"
            )

            if not file_path:
                return  # 用户取消了保存

            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("保存成功", f"配置已成功保存到: {file_path}")

        except Exception as e:
            messagebox.showerror("保存错误", f"保存配置时出现错误: {str(e)}")

    def load_config(self):
        """加载参数配置"""
        try:
            # 询问加载文件
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
                title="选择配置文件"
            )

            if not file_path:
                return  # 用户取消了加载

            # 从文件加载配置
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 设置所有变量值
            self.delivery_amount.set(config.get("delivery_amount", 100.0))
            self.purchase_amount.set(config.get("purchase_amount", 50.0))
            self.service_price.set(config.get("service_price", 1000.0))
            self.service_cost.set(config.get("service_cost", 300.0))
            self.employee_count.set(config.get("employee_count", 2))
            self.supervisor_count.set(config.get("supervisor_count", 1))
            self.consultant_count.set(config.get("consultant_count", 0))
            self.regional_manager_count.set(config.get("regional_manager_count", 0))
            self.city_manager_count.set(config.get("city_manager_count", 0))
            self.supervisor_bonus.set(config.get("supervisor_bonus", 500.0))
            self.consultant_bonus.set(config.get("consultant_bonus", 800.0))
            self.regional_manager_bonus.set(config.get("regional_manager_bonus", 1200.0))
            self.city_manager_bonus.set(config.get("city_manager_bonus", 1500.0))
            self.employee_type.set(config.get("employee_type", "员工"))
            self.old_base_salary.set(config.get("old_base_salary", 3000.0))
            self.old_basic_bonus.set(config.get("old_basic_bonus", 500.0))
            self.old_position_bonus.set(config.get("old_position_bonus", 300.0))
            self.old_extra_bonus.set(config.get("old_extra_bonus", 200.0))
            self.new_base_salary_mid.set(config.get("new_base_salary_mid", 3500.0))
            self.new_base_salary_low.set(config.get("new_base_salary_low", 2800.0))
            self.old_purchase_baseline.set(config.get("old_purchase_baseline", 40.0))
            self.bonus_tier1_threshold.set(config.get("bonus_tier1_threshold", 0.9))
            self.bonus_tier1_amount.set(config.get("bonus_tier1_amount", 7.5))
            self.bonus_tier2_threshold.set(config.get("bonus_tier2_threshold", 1.0))
            self.bonus_tier2_amount.set(config.get("bonus_tier2_amount", 50.0))
            self.bonus_tier3_amount.set(config.get("bonus_tier3_amount", 60.0))
            self.new_purchase_amount.set(config.get("new_purchase_amount", 0.0))
            self.min_conversion_rate.set(config.get("min_conversion_rate", 45.0))
            self.penalty_rate.set(config.get("penalty_rate", 0.8))
            self.salary_mode.set(config.get("salary_mode", "新保底"))
            self.social_insurance_base.set(config.get("social_insurance_base", 10000.0))
            self.pension_rate.set(config.get("pension_rate", 8.0))
            self.medical_rate.set(config.get("medical_rate", 2.0))
            self.unemployment_rate.set(config.get("unemployment_rate", 0.2))
            self.injury_rate.set(config.get("injury_rate", 0.0))
            self.maternity_rate.set(config.get("maternity_rate", 0.0))
            self.housing_fund_rate.set(config.get("housing_fund_rate", 12.0))
            self.current_month.set(config.get("current_month", datetime.now().strftime("%Y-%m")))
            self.avg_total_salary.set(config.get("avg_total_salary", 5000.0))
            self.avg_delivery.set(config.get("avg_delivery", 80.0))
            self.avg_purchase.set(config.get("avg_purchase", 40.0))
            self.avg_conversion_rate.set(config.get("avg_conversion_rate", 50.0))
            self.city_cost.set(config.get("city_cost", 10000.0))

            # 更新显示
            self.update_salary_displays()

            messagebox.showinfo("加载成功", f"配置已成功从 {file_path} 加载")

        except Exception as e:
            messagebox.showerror("加载错误", f"加载配置时出现错误: {str(e)}")

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryCalculator(root)
    root.mainloop()
