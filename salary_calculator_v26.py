import tkinter as tk
from tkinter import ttk, messagebox


class SalaryCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("薪资计算系统")
        self.root.geometry("1200x800")

        # 创建数据存储
        self.data = {
            "delivery_volume": tk.StringVar(value="175"),
            "service_packs": tk.StringVar(value="102"),
            "store_staff": tk.StringVar(value="2"),
            "pack_price": tk.StringVar(value="510"),
            "pack_cost": tk.StringVar(value="100"),
            "has_station_license": tk.StringVar(value="无"),
            "avg_monthly_packs": tk.StringVar(value="58"),
            "threshold_discount": tk.StringVar(value="0.7"),
            "old_avg_commission": tk.StringVar(value="1962"),
            "new_base_mid": tk.StringVar(value="3100"),
            "new_base_low": tk.StringVar(value="2000"),
            "new_service_packs": tk.StringVar(value="102"),
            "low_conversion_rate": tk.StringVar(value="0.5"),
            "high_conversion_rate": tk.StringVar(value="0.7"),
            "y_discount": tk.StringVar(value="0.9"),
            "z_discount": tk.StringVar(value="1.1"),
            "use_threshold": tk.BooleanVar(value=False),
            "threshold1": tk.StringVar(value="90"),
            "threshold2": tk.StringVar(value="100"),
            "commission_tier1": tk.StringVar(value="10"),  # 档1每包提成（自动计算、只读）
            "commission_tier2": tk.StringVar(value="15"),
            "commission_tier3": tk.StringVar(value="20"),
            "threshold_percentage": tk.StringVar(value="0.9"),
            "calculated_commission_rate": tk.StringVar(value=""),
            "threshold_suggestion": tk.StringVar(value=""),
            "staff_data": []
        }

        # 添加员工数据
        for i in range(2):
            self.data["staff_data"].append({
                "old_base": tk.StringVar(value="2000" if i == 0 else "2200"),
                "basic_perf": tk.StringVar(value="550" if i == 0 else "650"),
                "post_perf": tk.StringVar(value="200" if i == 0 else "400"),
                "subsidy": tk.StringVar(value="1100")
            })

        self.create_widgets()

        # 绑定事件
        self.data["use_threshold"].trace_add("write", self.toggle_threshold_fields)
        self.data["commission_tier2"].trace_add("write", self.calculate_threshold_suggestion)

    def calculate_threshold_suggestion(self, *args):
        if not self.data["use_threshold"].get():
            return

        try:
            new_service_packs = int(self.data["new_service_packs"].get())
            commission_tier1 = float(self.data["commission_tier1"].get())
            commission_tier2 = float(self.data["commission_tier2"].get())
            commission_tier3 = float(self.data["commission_tier3"].get())
            old_avg_commission = float(self.data["old_avg_commission"].get() or 0)

            # 用档1提成自动推荐打平
            old_commission_total = new_service_packs * commission_tier1

            best_suggestion = ""
            min_diff = float('inf')
            step = 5
            for t1 in range(10, new_service_packs, step):
                for t2 in range(t1 + step, new_service_packs + step, step):
                    if new_service_packs <= t1:
                        total_commission = new_service_packs * commission_tier1
                    elif new_service_packs <= t2:
                        total_commission = t1 * commission_tier1 + (new_service_packs - t1) * commission_tier2
                    else:
                        total_commission = t1 * commission_tier1 + (t2 - t1) * commission_tier2 + (
                                new_service_packs - t2) * commission_tier3
                    diff = abs(total_commission - old_commission_total)
                    if diff < min_diff:
                        min_diff = diff
                        best_suggestion = f"建议阈值1: {t1}包, 阈值2: {t2}包 (差异: {diff:.2f}元)"

            self.data["threshold_suggestion"].set(best_suggestion)

        except Exception as e:
            self.data["threshold_suggestion"].set(f"计算错误: {str(e)}")

    def toggle_threshold_fields(self, *args):
        # 档1提成始终禁用、只显示
        self.commission_tier1_entry.config(state=tk.DISABLED)

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        params_frame = ttk.Frame(notebook)
        notebook.add(params_frame, text="参数输入")
        self.create_params_tab(params_frame)

        formulas_frame = ttk.Frame(notebook)
        notebook.add(formulas_frame, text="公式说明")
        self.create_formulas_tab(formulas_frame)

        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="计算结果")

        self.results_text = tk.Text(results_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        calc_btn = ttk.Button(btn_frame, text="计算薪资", command=self.calculate)
        calc_btn.pack(side=tk.RIGHT, padx=5)
        reset_btn = ttk.Button(btn_frame, text="重置数据", command=self.reset_data)
        reset_btn.pack(side=tk.RIGHT, padx=5)

    def create_params_tab(self, parent):
        params_notebook = ttk.Notebook(parent)
        params_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        basic_frame = ttk.Frame(params_notebook)
        params_notebook.add(basic_frame, text="基础参数")

        commission_frame = ttk.Frame(params_notebook)
        params_notebook.add(commission_frame, text="提成参数")

        threshold_frame = ttk.Frame(params_notebook)
        params_notebook.add(threshold_frame, text="阈值参数")

        staff_frame = ttk.Frame(params_notebook)
        params_notebook.add(staff_frame, text="员工数据")

        basic_labels = [
            ("交付量:", "delivery_volume"),
            ("购买服务包数量:", "service_packs"),
            ("门店人数:", "store_staff"),
            ("服务包价格:", "pack_price"),
            ("服务包成本:", "pack_cost"),
            ("是否站内上牌(有/无):", "has_station_license"),
            ("过去X月平均每人购买服务包数量:", "avg_monthly_packs"),
            ("阈值折扣比例(0-1):", "threshold_discount"),
            ("旧月均提成:", "old_avg_commission"),
            ("新底薪(中):", "new_base_mid"),
            ("新底薪(低):", "new_base_low"),
            ("新购买服务包数:", "new_service_packs")
        ]

        for i, (label, key) in enumerate(basic_labels):
            ttk.Label(basic_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(basic_frame, textvariable=self.data[key], width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)

        commission_labels = [
            ("下线转化率要求(小数):", "low_conversion_rate"),
            ("上线转化率要求(小数):", "high_conversion_rate"),
            ("折扣y(小数):", "y_discount"),
            ("折扣z(小数):", "z_discount"),
            ("门店逻辑阈值百分比(小数):", "threshold_percentage")
        ]

        for i, (label, key) in enumerate(commission_labels):
            ttk.Label(commission_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(commission_frame, textvariable=self.data[key], width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)

        threshold_labels = [
            ("使用阈值计算:", "use_threshold"),
            ("阈值1(服务包数):", "threshold1"),
            ("阈值2(服务包数):", "threshold2"),
            ("档1每包提成:", "commission_tier1"),
            ("档2每包提成:", "commission_tier2"),
            ("档3每包提成:", "commission_tier3")
        ]

        for i, (label, key) in enumerate(threshold_labels):
            row_frame = ttk.Frame(threshold_frame)
            row_frame.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)

            ttk.Label(row_frame, text=label).pack(side=tk.LEFT)

            if key == "use_threshold":
                chk = ttk.Checkbutton(row_frame, variable=self.data[key])
                chk.pack(side=tk.LEFT, padx=5)
            elif key == "commission_tier1":
                # 档1提成显示只读
                self.commission_tier1_entry = ttk.Entry(row_frame, textvariable=self.data[key], width=10, state="disabled")
                self.commission_tier1_entry.pack(side=tk.LEFT)
                self.tier1_note_label = ttk.Label(row_frame, text="", foreground="blue")
                self.tier1_note_label.pack(side=tk.LEFT, padx=5)
            elif key == "commission_tier2":
                entry = ttk.Entry(row_frame, textvariable=self.data[key], width=10)
                entry.pack(side=tk.LEFT)
                entry.bind("<FocusOut>", lambda e: self.calculate_threshold_suggestion())
            else:
                entry = ttk.Entry(row_frame, textvariable=self.data[key], width=10)
                entry.pack(side=tk.LEFT)

        suggestion_row = ttk.Frame(threshold_frame)
        suggestion_row.grid(row=len(threshold_labels), column=0, sticky=tk.W, padx=5, pady=10)
        ttk.Label(suggestion_row, text="阈值建议:").pack(side=tk.LEFT)
        suggestion_label = ttk.Label(suggestion_row, textvariable=self.data["threshold_suggestion"], foreground="green")
        suggestion_label.pack(side=tk.LEFT, padx=5)

        ttk.Label(staff_frame, text="员工类型").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(staff_frame, text="旧底薪").grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(staff_frame, text="基本绩效").grid(row=0, column=2, padx=5, pady=2)
        ttk.Label(staff_frame, text="岗位绩效").grid(row=0, column=3, padx=5, pady=2)
        ttk.Label(staff_frame, text="补贴").grid(row=0, column=4, padx=5, pady=2)

        for i in range(len(self.data["staff_data"])):
            ttk.Label(staff_frame, text=f"员工{i + 1}").grid(row=i + 1, column=0, padx=5, pady=2)
            staff = self.data["staff_data"][i]
            ttk.Entry(staff_frame, textvariable=staff["old_base"], width=8).grid(row=i + 1, column=1, padx=5, pady=2)
            ttk.Entry(staff_frame, textvariable=staff["basic_perf"], width=8).grid(row=i + 1, column=2, padx=5, pady=2)
            ttk.Entry(staff_frame, textvariable=staff["post_perf"], width=8).grid(row=i + 1, column=3, padx=5, pady=2)
            ttk.Entry(staff_frame, textvariable=staff["subsidy"], width=8).grid(row=i + 1, column=4, padx=5, pady=2)

        self.toggle_threshold_fields()

    def create_formulas_tab(self, parent):
        text = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        formulas = """
        ================== 薪资计算公式说明 ==================

        1. 基础指标计算
        ---------------------------------
        转化率 = 购买服务包数量 / 交付量 × 100%
        人均购买服务包数 = 购买服务包数 / 门店人数

        2. 旧薪资体系计算
        ---------------------------------
        基本薪资 = 旧底薪 + 基本绩效 + 岗位绩效 + 补贴
        总提成 = 新购买服务包数 × 每包提成
        人均提成 = 总提成 / 门店人数
        汇总薪资 = 基本薪资 + 人均提成

        3. 新薪资体系计算
        ---------------------------------
        模式一(新保底): 固定薪资 = 3850元

        模式二(新底薪中)和模式三(新底薪低)计算:
        提成 = (新购买服务包数 / 门店人数) × ((旧底薪 + 基本绩效 + 岗位绩效 + 补贴 + 旧月均提成 - 新底薪) / 过去X月平均每人购买服务包数量)

        4. 三档提成计算规则(仅当启用阈值时)
        ---------------------------------
        档1单价自动计算，不可手填，仅为提成基数。
        阈值1数量 = 服务包数阈值1
        阈值2数量 = 服务包数阈值2

        提成计算:
          - 服务包数量 ≤ 阈值1数量: 提成 = 服务包数量 × 档1每包提成
          - 阈值1数量 < 服务包数量 ≤ 阈值2数量: 
                提成 = (阈值1数量 × 档1每包提成) + (服务包数量 - 阈值1数量) × 档2每包提成
          - 服务包数量 > 阈值2数量: 
                提成 = (阈值1数量 × 档1每包提成) + 
                      (阈值2数量 - 阈值1数量) × 档2每包提成 + 
                      (服务包数量 - 阈值2数量) × 档3每包提成

        5. 门店逻辑
        ---------------------------------
        1. 转化率折扣:
          - 转化率 < 下线要求: 提成部分打y折扣
          - 转化率 > 上线要求: 提成部分打z折扣
          - 否则: 提成不变

        2. 包数不足折扣:
          如果新购买服务包数 < 过去X月平均每人购买服务包数量 × 门店人数 × 门店逻辑阈值百分比
          则模式二和模式三的汇总薪资都要乘以配置的折扣比例

        6. 新旧薪资对比
        ---------------------------------
        差异 = 新薪资 - 旧薪资
        """
        text.insert(tk.END, formulas)
        text.config(state=tk.DISABLED)

    def reset_data(self):
        self.data["delivery_volume"].set("175")
        self.data["service_packs"].set("102")
        self.data["store_staff"].set("2")
        self.data["pack_price"].set("510")
        self.data["pack_cost"].set("100")
        self.data["has_station_license"].set("无")
        self.data["avg_monthly_packs"].set("58")
        self.data["threshold_discount"].set("0.7")
        self.data["old_avg_commission"].set("1962")
        self.data["new_base_mid"].set("3100")
        self.data["new_base_low"].set("2000")
        self.data["new_service_packs"].set("102")
        self.data["low_conversion_rate"].set("0.5")
        self.data["high_conversion_rate"].set("0.7")
        self.data["y_discount"].set("0.9")
        self.data["z_discount"].set("1.1")
        self.data["use_threshold"].set(False)
        self.data["threshold1"].set("90")
        self.data["threshold2"].set("100")
        self.data["commission_tier1"].set("10")
        self.data["commission_tier2"].set("15")
        self.data["commission_tier3"].set("20")
        self.data["threshold_percentage"].set("0.9")
        self.data["calculated_commission_rate"].set("")
        self.data["threshold_suggestion"].set("")
        for i, staff in enumerate(self.data["staff_data"]):
            staff["old_base"].set("2000" if i == 0 else "2200")
            staff["basic_perf"].set("550" if i == 0 else "650")
            staff["post_perf"].set("200" if i == 0 else "400")
            staff["subsidy"].set("1100")
        self.results_text.delete(1.0, tk.END)
        self.toggle_threshold_fields()

    def calculate(self):
        try:
            result_text = "=== 薪资计算详细过程 ===\n\n"

            delivery_volume = int(self.data["delivery_volume"].get())
            service_packs = int(self.data["service_packs"].get())
            store_staff = int(self.data["store_staff"].get())
            pack_price = int(self.data["pack_price"].get())
            pack_cost = int(self.data["pack_cost"].get())
            has_station_license = self.data["has_station_license"].get() == "有"
            avg_monthly_packs = int(self.data["avg_monthly_packs"].get())
            threshold_discount = float(self.data["threshold_discount"].get())
            old_avg_commission = float(self.data["old_avg_commission"].get())
            new_base_mid = float(self.data["new_base_mid"].get())
            new_base_low = float(self.data["new_base_low"].get())
            new_service_packs = int(self.data["new_service_packs"].get())
            use_threshold = self.data["use_threshold"].get()

            low_conversion_rate = float(self.data["low_conversion_rate"].get())
            high_conversion_rate = float(self.data["high_conversion_rate"].get())
            y_discount = float(self.data["y_discount"].get())
            z_discount = float(self.data["z_discount"].get())
            threshold_percentage = float(self.data["threshold_percentage"].get())

            threshold1 = int(self.data["threshold1"].get())
            threshold2 = int(self.data["threshold2"].get())
            commission_tier2 = float(self.data["commission_tier2"].get())
            commission_tier3 = float(self.data["commission_tier3"].get())

            staff_list = []
            for staff_data in self.data["staff_data"]:
                staff = {
                    "old_base": float(staff_data["old_base"].get()),
                    "basic_perf": float(staff_data["basic_perf"].get()),
                    "post_perf": float(staff_data["post_perf"].get()),
                    "subsidy": float(staff_data["subsidy"].get())
                }
                staff_list.append(staff)

            result_text += "=== 1. 基础指标计算 ===\n"
            conversion_rate = (service_packs / delivery_volume) * 100 if delivery_volume > 0 else 0
            per_capita_packs = service_packs / store_staff if store_staff > 0 else 0
            result_text += f"转化率 = 购买服务包数量 / 交付量 × 100% = {service_packs} / {delivery_volume} × 100% = {conversion_rate:.2f}%\n"
            result_text += f"人均购买服务包数 = 购买服务包数 / 门店人数 = {service_packs} / {store_staff} = {per_capita_packs:.2f}\n\n"

            result_text += "=== 2. 旧提成单价计算 ===\n"
            conditions = [
                (pack_price > 450 and not has_station_license),
                (pack_price > 450 and has_station_license),
                (pack_price <= 450 and not has_station_license),
                (pack_price <= 450 and has_station_license)
            ]

            commission_rate = 0
            if conditions[0]:
                if conversion_rate < 50:
                    commission_rate = 10
                elif 50 <= conversion_rate < 60:
                    commission_rate = 15
                else:
                    commission_rate = 20
                result_text += f"条件: 服务包价格 > 450 且 无站内上牌\n"
            elif conditions[1]:
                if conversion_rate < 50:
                    commission_rate = 15
                elif 50 <= conversion_rate < 60:
                    commission_rate = 20
                else:
                    commission_rate = 25
                result_text += f"条件: 服务包价格 > 450 且 有站内上牌\n"
            elif conditions[2]:
                if conversion_rate < 50:
                    commission_rate = 5
                elif 50 <= conversion_rate < 60:
                    commission_rate = 10
                else:
                    commission_rate = 15
                result_text += f"条件: 服务包价格 ≤ 450 且 无站内上牌\n"
            elif conditions[3]:
                if conversion_rate < 50:
                    commission_rate = 10
                elif 50 <= conversion_rate < 60:
                    commission_rate = 15
                else:
                    commission_rate = 20
                result_text += f"条件: 服务包价格 ≤ 450 且 有站内上牌\n"

            self.data["calculated_commission_rate"].set(str(commission_rate))
            result_text += f"旧提成单价 = {commission_rate}元/包\n\n"

            # === 3. 旧薪资体系 ===
            result_text += "=== 3. 旧薪资体系计算 ===\n"
            for i, staff in enumerate(staff_list):
                basic_salary = staff["old_base"] + staff["basic_perf"] + staff["post_perf"] + staff["subsidy"]
                total_commission = service_packs * commission_rate
                per_capita_commission = total_commission / store_staff if store_staff > 0 else 0
                total_salary = basic_salary + per_capita_commission
                result_text += f"员工{i + 1}:\n"
                result_text += f"  基本薪资 = 旧底薪 + 基本绩效 + 岗位绩效 + 补贴 = {staff['old_base']} + {staff['basic_perf']} + {staff['post_perf']} + {staff['subsidy']} = {basic_salary:.2f}元\n"
                result_text += f"  总提成 = 服务包数 × 提成单价 = {service_packs} × {commission_rate} = {total_commission:.2f}元\n"
                result_text += f"  人均提成 = 总提成 / 门店人数 = {total_commission:.2f} / {store_staff} = {per_capita_commission:.2f}元\n"
                result_text += f"  汇总薪资 = 基本薪资 + 人均提成 = {basic_salary:.2f} + {per_capita_commission:.2f} = {total_salary:.2f}元\n\n"

            result_text += "=== 4. 新薪资体系计算 ===\n"
            result_text += "模式一(新保底):\n"
            for i, staff in enumerate(staff_list):
                salary_mode1 = 3850
                result_text += f"  员工{i + 1}薪资 = {salary_mode1}元\n"

            # ================== 新底薪中 =========================
            result_text += "\n模式二(新底薪中):\n"
            for i, staff in enumerate(staff_list):
                numerator = staff["old_base"] + staff["basic_perf"] + staff["post_perf"] + staff["subsidy"] + old_avg_commission - new_base_mid
                denominator = avg_monthly_packs
                if denominator == 0:
                    messagebox.showerror("错误", "过去X月平均每人购买服务包数量不能为零")
                    return
                unit_commission = numerator / denominator  # 档1自动算

                # UI只读显示
                self.data["commission_tier1"].set(f"{unit_commission:.2f}")
                self.tier1_note_label.config(text=f"(档1单价为：{unit_commission:.2f}元/包，仅做自动显示)")

                per_capita_new_packs = new_service_packs / store_staff if store_staff > 0 else 0

                if use_threshold:
                    commission_tier1 = unit_commission  # 只用自动算出来的
                    if new_service_packs <= threshold1:
                        total_commission = new_service_packs * commission_tier1
                    elif new_service_packs <= threshold2:
                        total_commission = threshold1 * commission_tier1 + (new_service_packs - threshold1) * commission_tier2
                    else:
                        total_commission = threshold1 * commission_tier1 + (threshold2 - threshold1) * commission_tier2 + (
                                new_service_packs - threshold2) * commission_tier3
                    commission_per_person = total_commission / store_staff if store_staff > 0 else 0
                    commission_after_conversion = commission_per_person
                    discount_note = " (应用阈值计算)"
                    salary_base = new_base_mid + commission_after_conversion
                else:
                    base_commission = per_capita_new_packs * unit_commission
                    commission_after_conversion = base_commission
                    if conversion_rate < low_conversion_rate * 100:
                        commission_after_conversion = base_commission * y_discount
                        discount_note = f" (应用y折扣: {y_discount})"
                    elif conversion_rate > high_conversion_rate * 100:
                        commission_after_conversion = base_commission * z_discount
                        discount_note = f" (应用z折扣: {z_discount})"
                    else:
                        discount_note = ""
                    salary_base = new_base_mid + commission_after_conversion

                threshold = avg_monthly_packs * store_staff * threshold_percentage
                if new_service_packs < threshold:
                    final_salary = salary_base * threshold_discount
                    discount_note += f" (包数不足, 应用折扣: {threshold_discount})"
                else:
                    final_salary = salary_base

                result_text += f"  员工{i + 1}:\n"
                result_text += f"    提成基数 = (旧底薪+基本绩效+岗位绩效+补贴+旧月均提成-新底薪) / 过去月均每人包数 = ({staff['old_base']}+{staff['basic_perf']}+{staff['post_perf']}+{staff['subsidy']}+{old_avg_commission}-{new_base_mid}) / {avg_monthly_packs} = {unit_commission:.2f}\n"
                if use_threshold:
                    result_text += f"    总提成 = {total_commission:.2f}元{discount_note}\n"
                    result_text += f"    人均提成 = 总提成 / 门店人数 = {total_commission:.2f} / {store_staff} = {commission_per_person:.2f}元\n"
                else:
                    result_text += f"    基础提成 = 人均新包数 × 提成基数 = {per_capita_new_packs:.2f} × {unit_commission:.2f} = {base_commission:.2f}{discount_note}\n"
                result_text += f"    基础薪资 = 新底薪中 + 提成 = {new_base_mid} + {commission_after_conversion:.2f} = {salary_base:.2f}\n"
                result_text += f"    最终薪资 = {final_salary:.2f}元\n"

            # ================== 新底薪低 =========================
            result_text += "\n模式三(新底薪低):\n"
            for i, staff in enumerate(staff_list):
                numerator = staff["old_base"] + staff["basic_perf"] + staff["post_perf"] + staff["subsidy"] + old_avg_commission - new_base_low
                denominator = avg_monthly_packs
                if denominator == 0:
                    messagebox.showerror("错误", "过去X月平均每人购买服务包数量不能为零")
                    return
                unit_commission = numerator / denominator  # 档1自动算
                # 可扩展：也可给档1低模式加一个只读显示

                per_capita_new_packs = new_service_packs / store_staff if store_staff > 0 else 0

                if use_threshold:
                    commission_tier1 = unit_commission  # 只用自动算出来的
                    if new_service_packs <= threshold1:
                        total_commission = new_service_packs * commission_tier1
                    elif new_service_packs <= threshold2:
                        total_commission = threshold1 * commission_tier1 + (new_service_packs - threshold1) * commission_tier2
                    else:
                        total_commission = threshold1 * commission_tier1 + (threshold2 - threshold1) * commission_tier2 + (
                                new_service_packs - threshold2) * commission_tier3
                    commission_per_person = total_commission / store_staff if store_staff > 0 else 0
                    commission_after_conversion = commission_per_person
                    discount_note = " (应用阈值计算)"
                    salary_base = new_base_low + commission_after_conversion
                else:
                    base_commission = per_capita_new_packs * unit_commission
                    commission_after_conversion = base_commission
                    if conversion_rate < low_conversion_rate * 100:
                        commission_after_conversion = base_commission * y_discount
                        discount_note = f" (应用y折扣: {y_discount})"
                    elif conversion_rate > high_conversion_rate * 100:
                        commission_after_conversion = base_commission * z_discount
                        discount_note = f" (应用z折扣: {z_discount})"
                    else:
                        discount_note = ""
                    salary_base = new_base_low + commission_after_conversion

                threshold = avg_monthly_packs * store_staff * threshold_percentage
                if new_service_packs < threshold:
                    final_salary = salary_base * threshold_discount
                    discount_note += f" (包数不足, 应用折扣: {threshold_discount})"
                else:
                    final_salary = salary_base

                result_text += f"  员工{i + 1}:\n"
                result_text += f"    提成基数 = (旧底薪+基本绩效+岗位绩效+补贴+旧月均提成-新底薪) / 过去月均每人包数 = ({staff['old_base']}+{staff['basic_perf']}+{staff['post_perf']}+{staff['subsidy']}+{old_avg_commission}-{new_base_low}) / {avg_monthly_packs} = {unit_commission:.2f}\n"
                if use_threshold:
                    result_text += f"    总提成 = {total_commission:.2f}元{discount_note}\n"
                    result_text += f"    人均提成 = 总提成 / 门店人数 = {total_commission:.2f} / {store_staff} = {commission_per_person:.2f}元\n"
                else:
                    result_text += f"    基础提成 = 人均新包数 × 提成基数 = {per_capita_new_packs:.2f} × {unit_commission:.2f} = {base_commission:.2f}{discount_note}\n"
                result_text += f"    基础薪资 = 新底薪低 + 提成 = {new_base_low} + {commission_after_conversion:.2f} = {salary_base:.2f}\n"
                result_text += f"    最终薪资 = {final_salary:.2f}元\n"

            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result_text)
            self.results_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中发生错误: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryCalculatorApp(root)
    root.mainloop()
