import tkinter as tk
from tkinter import ttk, messagebox

class SalaryCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("薪资计算系统")
        self.root.geometry("1200x800")

        # 数据存储
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
            "commission_tier1": tk.StringVar(value="10"),
            "commission_tier2": tk.StringVar(value="15"),
            "commission_tier3": tk.StringVar(value="20"),
            "threshold_percentage": tk.StringVar(value="0.9"),
            "staff_data": []
        }

        # 创建员工数据占位
        for i in range(2):
            self.data["staff_data"].append({
                "old_base": tk.StringVar(value="2000" if i else "2200"),
                "basic_perf": tk.StringVar(value="550" if i else "650"),
                "post_perf": tk.StringVar(value="200" if i else "400"),
                "subsidy": tk.StringVar(value="1100")
            })

        self.create_widgets()

    def create_widgets(self):
        # 创建选项卡
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 参数输入选项卡
        params_frame = ttk.Frame(notebook)
        notebook.add(params_frame, text="参数输入")
        self.create_params_tab(params_frame)

        # 公式说明选项卡
        formulas_frame = ttk.Frame(notebook)
        notebook.add(formulas_frame, text="公式说明")
        self.create_formulas_tab(formulas_frame)

        # 计算结果选项卡
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="计算结果")
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 计算按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        calc_btn = ttk.Button(btn_frame, text="计算薪资", command=self.calculate)
        calc_btn.pack(side=tk.RIGHT, padx=5)

        clear_btn = ttk.Button(btn_frame, text="重置数据", command=self.reset_data)
        clear_btn.pack(side=tk.RIGHT, padx=5)

    def create_params_tab(self, parent):
        # 创建嵌套的Notebook用于参数分类
        params_notebook = ttk.Notebook(parent)
        params_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 基础参数框架
        basic_frame = ttk.Frame(params_notebook)
        params_notebook.add(basic_frame, text="基础参数")

        # 提成参数框架
        commission_frame = ttk.Frame(params_notebook)
        params_notebook.add(commission_frame, text="提成参数")

        # 阈值参数框架
        threshold_frame = ttk.Frame(params_notebook)
        params_notebook.add(threshold_frame, text="阈值参数")

        # 员工数据框架
        staff_frame = ttk.Frame(params_notebook)
        params_notebook.add(staff_frame, text="员工数据")

        # 基础参数输入
        labels = [
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

        for i, (label, key) in enumerate(labels):
            ttk.Label(basic_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(basic_frame, textvariable=self.data[key], width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)

        # 提成参数输入
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

        # 阈值参数输入
        threshold_labels = [
            ("使用阈值计算:", "use_threshold"),
            ("阈值1(%):", "threshold1"),
            ("阈值2(%):", "threshold2"),
            ("档1每包提成:", "commission_tier1"),
            ("档2每包提成:", "commission_tier2"),
            ("档3每包提成:", "commission_tier3")
        ]

        for i, (label, key) in enumerate(threshold_labels):
            ttk.Label(threshold_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)

            if key == "use_threshold":
                chk = ttk.Checkbutton(threshold_frame, variable=self.data[key])
                chk.grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
            else:
                entry = ttk.Entry(threshold_frame, textvariable=self.data[key], width=15)
                entry.grid(row=i, column=1, padx=5, pady=2)

        # 员工数据输入
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

    def create_formulas_tab(self, parent):
        # 创建文本部件显示公式
        text = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 公式内容
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
        阈值1数量 = 过去X月平均每人购买服务包数量 × 门店人数 × 阈值1百分比 / 100
        阈值2数量 = 过去X月平均每人购买服务包数量 × 门店人数 × 阈值2百分比 / 100

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
        # 重置所有数据为默认值
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

        for i, staff in enumerate(self.data["staff_data"]):
            staff["old_base"].set("2000" if i else "2200")
            staff["basic_perf"].set("550" if i else "650")
            staff["post_perf"].set("200" if i else "400")
            staff["subsidy"].set("1100")

        self.results_text.delete(1.0, tk.END)

    def calculate(self):
        try:
            # 准备计算结果文本
            result_text = "=== 薪资计算详细过程 ===\n\n"

            # 提取基础参数
            delivery_volume = float(self.data["delivery_volume"].get())
            service_packs = float(self.data["service_packs"].get())
            store_staff = float(self.data["store_staff"].get())
            pack_price = float(self.data["pack_price"].get())
            pack_cost = float(self.data["pack_cost"].get())
            has_station_license = self.data["has_station_license"].get() == "有"
            avg_monthly_packs = float(self.data["avg_monthly_packs"].get())
            threshold_discount = float(self.data["threshold_discount"].get())
            old_avg_commission = float(self.data["old_avg_commission"].get())
            new_base_mid = float(self.data["new_base_mid"].get())
            new_base_low = float(self.data["new_base_low"].get())
            new_service_packs = float(self.data["new_service_packs"].get())
            use_threshold = self.data["use_threshold"].get()

            # 提取提成参数
            low_conversion_rate = float(self.data["low_conversion_rate"].get())
            high_conversion_rate = float(self.data["high_conversion_rate"].get())
            y_discount = float(self.data["y_discount"].get())
            z_discount = float(self.data["z_discount"].get())
            threshold_percentage = float(self.data["threshold_percentage"].get())

            # 提取三档提成参数
            threshold1 = float(self.data["threshold1"].get())
            threshold2 = float(self.data["threshold2"].get())
            commission_tier1 = float(self.data["commission_tier1"].get())
            commission_tier2 = float(self.data["commission_tier2"].get())
            commission_tier3 = float(self.data["commission_tier3"].get())

            # 提取员工数据
            staff_list = []
            for staff_data in self.data["staff_data"]:
                staff = {
                    "old_base": float(staff_data["old_base"].get()),
                    "basic_perf": float(staff_data["basic_perf"].get()),
                    "post_perf": float(staff_data["post_perf"].get()),
                    "subsidy": float(staff_data["subsidy"].get())
                }
                staff_list.append(staff)

            # === 计算基础指标 ===
            result_text += "=== 1. 基础指标计算 ===\n"
            conversion_rate = (service_packs / delivery_volume) * 100
            per_capita_packs = service_packs / store_staff
            result_text += f"转化率 = 购买服务包数量 / 交付量 × 100% = {service_packs} / {delivery_volume} × 100% = {conversion_rate:.2f}%\n"
            result_text += f"人均购买服务包数 = 购买服务包数 / 门店人数 = {service_packs} / {store_staff} = {per_capita_packs:.2f}\n\n"

            # === 计算旧提成单价 ===
            result_text += "=== 2. 旧提成单价计算 ===\n"
            conditions = [
                (pack_price > 450 and not has_station_license),
                (pack_price > 450 and has_station_license),
                (pack_price <= 450 and not has_station_license),
                (pack_price <= 450 and has_station_license)
            ]

            commission_rate = 0
            if conditions[0]:  # >450 & 无站内
                if conversion_rate < 50:
                    commission_rate = 10
                elif 50 <= conversion_rate < 60:
                    commission_rate = 15
                elif 60 <= conversion_rate < 70:
                    commission_rate = 20
                else:
                    commission_rate = 25
                result_text += f"条件: 服务包价格>450且无站内上牌, 转化率={conversion_rate:.2f}% → 每包提成={commission_rate}元\n"

            elif conditions[1]:  # >450 & 有站内
                if conversion_rate < 60:
                    commission_rate = 10
                elif 60 <= conversion_rate < 70:
                    commission_rate = 15
                elif 70 <= conversion_rate < 80:
                    commission_rate = 20
                else:
                    commission_rate = 25
                result_text += f"条件: 服务包价格>450且有站内上牌, 转化率={conversion_rate:.2f}% → 每包提成={commission_rate}元\n"

            elif conditions[2]:  # <=450 & 无站内
                if conversion_rate < 50:
                    commission_rate = 10
                elif 50 <= conversion_rate < 60:
                    commission_rate = 12
                elif 60 <= conversion_rate < 75:
                    commission_rate = 15
                else:
                    commission_rate = 20
                result_text += f"条件: 服务包价格≤450且无站内上牌, 转化率={conversion_rate:.2f}% → 每包提成={commission_rate}元\n"

            elif conditions[3]:  # <=450 & 有站内
                if conversion_rate < 60:
                    commission_rate = 10
                elif 60 <= conversion_rate < 70:
                    commission_rate = 12
                elif 70 <= conversion_rate < 80:
                    commission_rate = 15
                else:
                    commission_rate = 20
                result_text += f"条件: 服务包价格≤450且有站内上牌, 转化率={conversion_rate:.2f}% → 每包提成={commission_rate}元\n"

            # === 旧薪资计算 ===
            result_text += "\n=== 3. 旧薪资计算 ===\n"
            total_commission = new_service_packs * commission_rate
            commission_per_person = total_commission / store_staff
            result_text += f"总提成 = 新购买服务包数 × 每包提成 = {new_service_packs} × {commission_rate} = {total_commission}\n"
            result_text += f"人均提成 = 总提成 / 门店人数 = {total_commission} / {store_staff} = {commission_per_person:.2f}\n"

            old_salaries = []
            for i, staff in enumerate(staff_list):
                basic_salary = staff["old_base"] + staff["basic_perf"] + staff["post_perf"] + staff["subsidy"]
                total_salary = basic_salary + commission_per_person
                old_salaries.append(total_salary)

                result_text += f"\n员工{i + 1}旧薪资计算:\n"
                result_text += f"基本薪资 = 旧底薪 + 基本绩效 + 岗位绩效 + 补贴 = "
                result_text += f"{staff['old_base']} + {staff['basic_perf']} + {staff['post_perf']} + {staff['subsidy']} = {basic_salary}\n"
                result_text += f"汇总薪资 = 基本薪资 + 人均提成 = {basic_salary} + {commission_per_person} = {total_salary:.2f}\n"

            # === 新薪资计算 ===
            result_text += "\n=== 4. 新薪资计算 ===\n"
            new_salaries = []  # 存储每个员工的三种薪资模式结果

            for i, staff in enumerate(staff_list):
                result_text += f"\n--- 员工{i + 1}新薪资计算 ---\n"

                # 模式一：新保底
                salary_high = 3850
                result_text += f"模式一(新保底): 固定薪资 = 3850元\n"

                # 模式二：新底薪(中)
                result_text += f"\n模式二(新底薪中):\n"
                salary_mid, mid_detail = self.calculate_new_salary_detail(
                    staff, conversion_rate, new_service_packs,
                    avg_monthly_packs, store_staff,
                    staff["old_base"], staff["basic_perf"], staff["post_perf"], staff["subsidy"],
                    old_avg_commission, new_base_mid,
                    low_conversion_rate, high_conversion_rate,
                    y_discount, z_discount, use_threshold,
                    threshold1, threshold2, commission_tier1, commission_tier2, commission_tier3,
                    threshold_percentage, threshold_discount,
                    "中"
                )
                result_text += mid_detail
                new_salaries.append({
                    "high": salary_high,
                    "mid": salary_mid,
                    "low": 0  # 临时值
                })

                # 模式三：新底薪(低)
                result_text += f"\n模式三(新底薪低):\n"
                salary_low, low_detail = self.calculate_new_salary_detail(
                    staff, conversion_rate, new_service_packs,
                    avg_monthly_packs, store_staff,
                    staff["old_base"], staff["basic_perf"], staff["post_perf"], staff["subsidy"],
                    old_avg_commission, new_base_low,
                    low_conversion_rate, high_conversion_rate,
                    y_discount, z_discount, use_threshold,
                    threshold1, threshold2, commission_tier1, commission_tier2, commission_tier3,
                    threshold_percentage, threshold_discount,
                    "低"
                )
                result_text += low_detail
                new_salaries[i]["low"] = salary_low

                # 添加分隔线
                result_text += "-" * 80 + "\n"

            # === 新旧薪资对比 ===
            result_text += "\n=== 5. 新旧薪资对比 ===\n"
            for i in range(len(staff_list)):
                result_text += f"\n员工{i + 1}薪资对比:\n"
                result_text += f"  旧薪资体系: {old_salaries[i]:.2f}元\n"
                result_text += f"  新薪资体系模式一(新保底): {new_salaries[i]['high']:.2f}元\n"
                result_text += f"  新薪资体系模式二(新底薪中): {new_salaries[i]['mid']:.2f}元\n"
                result_text += f"  新薪资体系模式三(新底薪低): {new_salaries[i]['low']:.2f}元\n"

                # 计算差异
                diff_high = new_salaries[i]['high'] - old_salaries[i]
                diff_mid = new_salaries[i]['mid'] - old_salaries[i]
                diff_low = new_salaries[i]['low'] - old_salaries[i]

                result_text += f"\n  对比结果:\n"
                result_text += f"  模式一比旧薪资 {'增加' if diff_high >= 0 else '减少'} {abs(diff_high):.2f}元\n"
                result_text += f"  模式二比旧薪资 {'增加' if diff_mid >= 0 else '减少'} {abs(diff_mid):.2f}元\n"
                result_text += f"  模式三比旧薪资 {'增加' if diff_low >= 0 else '减少'} {abs(diff_low):.2f}元\n"

            # 更新结果文本框
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result_text)
            self.results_text.see(tk.END)  # 滚动到最后

        except Exception as e:
            messagebox.showerror("计算错误", f"发生错误: {str(e)}")

    def calculate_new_salary_detail(self, staff, conversion_rate, new_service_packs,
                                    avg_monthly_packs, store_staff,
                                    old_base, basic_perf, post_perf, subsidy,
                                    old_avg_commission, new_base,
                                    low_conversion_rate, high_conversion_rate,
                                    y_discount, z_discount, use_threshold,
                                    threshold1, threshold2, commission_tier1, commission_tier2, commission_tier3,
                                    threshold_percentage, threshold_discount,
                                    salary_level):
        """
        计算新薪资并返回详细的计算过程文本
        返回值: (最终薪资, 详细计算过程文本)
        """
        detail = ""
        detail += f"模式: {salary_level}, 新底薪: {new_base}元\n"
        detail += f"员工数据: 旧底薪={old_base}, 基本绩效={basic_perf}, 岗位绩效={post_perf}, 补贴={subsidy}\n\n"

        # === 1. 计算提成基数 ===
        detail += f"1. 计算提成基数:\n"
        numerator = old_base + basic_perf + post_perf + subsidy + old_avg_commission - new_base
        denominator = avg_monthly_packs

        detail += f"   分子 = (旧底薪 + 基本绩效 + 岗位绩效 + 补贴 + 旧月均提成) - 新底薪\n"
        detail += f"         = ({old_base} + {basic_perf} + {post_perf} + {subsidy} + {old_avg_commission}) - {new_base}\n"
        detail += f"         = {numerator}\n\n"

        detail += f"   分母 = 过去X月平均每人购买服务包数量 = {denominator}\n\n"

        unit_commission = numerator / denominator
        detail += f"   单位提成 = 分子 / 分母 = {numerator} / {denominator} = {unit_commission:.4f}\n\n"

        per_capita_packs = new_service_packs / store_staff
        detail += f"   人均服务包数 = 新购买服务包数 / 门店人数 = {new_service_packs} / {store_staff} = {per_capita_packs:.2f}\n\n"

        base_commission = per_capita_packs * unit_commission
        detail += f"   基础提成 = 人均服务包数 × 单位提成 = {per_capita_packs:.2f} × {unit_commission:.4f} = {base_commission:.4f}\n\n"

        # === 2. 应用转化率折扣 ===
        detail += f"2. 应用转化率折扣规则:\n"
        detail += f"   当前转化率: {conversion_rate:.2f}%\n"
        detail += f"   下限要求: {low_conversion_rate * 100}%\n"
        detail += f"   上限要求: {high_conversion_rate * 100}%\n"

        commission_after_conversion = base_commission
        if conversion_rate < low_conversion_rate * 100:
            detail += f"   转化率 < 下限要求 → 提成部分打y折扣 ({y_discount})\n"
            commission_after_conversion = base_commission * y_discount
            detail += f"   折扣后提成 = {base_commission:.4f} × {y_discount} = {commission_after_conversion:.4f}\n"
        elif conversion_rate > high_conversion_rate * 100:
            detail += f"   转化率 > 上限要求 → 提成部分打z折扣 ({z_discount})\n"
            commission_after_conversion = base_commission * z_discount
            detail += f"   折扣后提成 = {base_commission:.4f} × {z_discount} = {commission_after_conversion:.4f}\n"
        else:
            detail += f"   转化率在正常范围内 → 提成不变\n"
            detail += f"   最终提成 = {commission_after_conversion:.4f}\n"

        detail += "\n"

        # === 3. 应用阈值逻辑（如果启用）===
        if use_threshold:
            detail += f"3. 应用三档提成逻辑(新底薪{salary_level}):\n"

            # 计算阈值数量
            threshold1_value = avg_monthly_packs * store_staff * (threshold1 / 100.0)
            threshold2_value = avg_monthly_packs * store_staff * (threshold2 / 100.0)

            detail += f"   阈值1数量 = 平均每人购买量 × 门店人数 × 阈值1百分比\n"
            detail += f"            = {avg_monthly_packs} × {store_staff} × {threshold1 / 100} = {threshold1_value:.2f}\n"
            detail += f"   阈值2数量 = 平均每人购买量 × 门店人数 × 阈值2百分比\n"
            detail += f"            = {avg_monthly_packs} × {store_staff} × {threshold2 / 100} = {threshold2_value:.2f}\n"

            # 应用三档提成规则
            if new_service_packs <= threshold1_value:
                detail += f"   服务包数量({new_service_packs}) ≤ 阈值1({threshold1_value:.2f}) → 使用档1\n"
                total_commission = new_service_packs * commission_tier1
                detail += f"   总提成 = 服务包数量 × 档1每包提成 = {new_service_packs} × {commission_tier1} = {total_commission}\n"
            elif threshold1_value < new_service_packs <= threshold2_value:
                detail += f"   阈值1({threshold1_value:.2f}) < 服务包数量({new_service_packs}) ≤ 阈值2({threshold2_value:.2f}) → 使用档2\n"
                base_commission = threshold1_value * commission_tier1
                extra_commission = (new_service_packs - threshold1_value) * commission_tier2
                total_commission = base_commission + extra_commission
                detail += f"   总提成 = (阈值1数量 × 档1每包提成) + (超过部分 × 档2每包提成)\n"
                detail += f"           = ({threshold1_value:.2f} × {commission_tier1}) + ({(new_service_packs - threshold1_value):.2f} × {commission_tier2})\n"
                detail += f"           = {base_commission} + {extra_commission} = {total_commission}\n"
            else:
                detail += f"   服务包数量({new_service_packs}) > 阈值2({threshold2_value:.2f}) → 使用档3\n"
                base_commission1 = threshold1_value * commission_tier1
                base_commission2 = (threshold2_value - threshold1_value) * commission_tier2
                extra_commission = (new_service_packs - threshold2_value) * commission_tier3
                total_commission = base_commission1 + base_commission2 + extra_commission
                detail += f"   总提成 = (阈值1数量 × 档1每包提成) + (阈值1-2之间数量 × 档2每包提成) + (超过阈值2部分 × 档3每包提成)\n"
                detail += f"           = ({threshold1_value:.2f} × {commission_tier1}) + ({(threshold2_value - threshold1_value):.2f} × {commission_tier2}) + ({(new_service_packs - threshold2_value):.2f} × {commission_tier3})\n"
                detail += f"           = {base_commission1} + {base_commission2} + {extra_commission} = {total_commission}\n"

            # 计算人均提成
            commission_per_person = total_commission / store_staff
            detail += f"\n   人均提成 = 总提成 / 门店人数 = {total_commission} / {store_staff} = {commission_per_person:.4f}\n"

            # 更新commission变量为人均提成
            commission_after_conversion = commission_per_person
        else:
            detail += f"3. 未启用阈值计算 → 使用基础提成\n"
            detail += f"   最终提成 = {commission_after_conversion:.4f}\n"

        detail += "\n"

        # === 4. 计算基础薪资 ===
        detail += f"4. 计算基础薪资:\n"
        salary_base = new_base + commission_after_conversion
        detail += f"   汇总薪资基数 = 新底薪 + 提成 = {new_base} + {commission_after_conversion:.4f} = {salary_base:.4f}\n\n"

        # === 5. 应用门店逻辑（包数不足折扣）===
        detail += f"5. 应用门店逻辑(包数不足折扣):\n"

        # 计算阈值：过去X月平均每人购买量 × 门店人数 × 门店逻辑阈值百分比
        threshold = avg_monthly_packs * store_staff * threshold_percentage
        detail += f"   阈值 = 过去X月平均每人购买量 × 门店人数 × 门店逻辑阈值百分比\n"
        detail += f"        = {avg_monthly_packs} × {store_staff} × {threshold_percentage}\n"
        detail += f"        = {threshold:.2f}\n"

        detail += f"   当前服务包数量 = {new_service_packs}\n"

        if new_service_packs < threshold:
            detail += f"   服务包数量 < 阈值 → 汇总薪资打{threshold_discount}折\n"
            final_salary = salary_base * threshold_discount
            detail += f"   最终薪资 = {salary_base:.4f} × {threshold_discount} = {final_salary:.4f}\n"
        else:
            final_salary = salary_base
            detail += f"   服务包数量 ≥ 阈值 → 汇总薪资不变\n"
            detail += f"   最终薪资 = {final_salary:.4f}\n"

        detail += f"最终{salary_level}模式薪资: {final_salary:.2f}元\n"

        return final_salary, detail


if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryCalculatorApp(root)
    root.mainloop()