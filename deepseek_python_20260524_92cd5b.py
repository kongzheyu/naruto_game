class HokageShinobi:
    """火影手游忍者结印机制模拟器"""
    
    def __init__(self):
        # 印槽位（长度3，FIFO，从左到右：旧→新）
        self.seal_slots = [2, 3, 4]
        
        # 子技能槽位（长度2，去重FIFO）
        self.skill_slots = ["油火弹"]  # 初始只有一个油火弹
        
        # 技能冷却（上滑/左滑/右滑/下滑）
        self.skill_cooldown = 0
        
        # 操作日志
        self.log = []
    
    def get_seal_set(self):
        """获取当前印的集合"""
        return set(self.seal_slots)
    
    def judge_skill(self):
        """根据当前印集合判定子技能"""
        S = self.get_seal_set()
        
        # {1,2,3} → 通灵之术
        if 1 in S and 2 in S and 3 in S:
            return "通灵之术"
        # {1,3,4} → 毛针千本
        elif 1 in S and 3 in S and 4 in S:
            return "毛针千本"
        # {1,4} 且无3 → 黄泉沼
        elif 1 in S and 4 in S and 3 not in S:
            return "黄泉沼"
        # 以上都不满足 → 油火弹
        else:
            return "油火弹"
    
    def add_seal(self, seal):
        """添加新印，FIFO"""
        self.seal_slots.append(seal)
        if len(self.seal_slots) > 3:
            self.seal_slots.pop(0)  # 挤掉最早的
    
    def update_skills(self):
        """根据当前印组合更新子技能队列"""
        new_skill = self.judge_skill()
        
        # 去重：如果新技能已在队列中，不加入
        if new_skill in self.skill_slots:
            return False
        
        # 加入队列
        self.skill_slots.append(new_skill)
        if len(self.skill_slots) > 2:
            self.skill_slots.pop(0)  # 挤掉最早的
        return True
    
    def normal_attack(self, stage):
        """
        普攻
        stage: 1-5，表示第几段普攻
        """
        if stage == 1:
            # 1A：无印
            pass
        elif stage == 2:
            # 2A：获得1印
            self.add_seal(1)
        elif stage == 3:
            # 3A：获得2印
            self.add_seal(2)
        elif stage == 4:
            # 4A：获得3印
            self.add_seal(3)
        elif stage == 5:
            # 5A：获得4印
            self.add_seal(4)
        
        self.update_skills()
        self.log.append(f"普攻{stage}段 → 印槽:{self.seal_slots} 技能:{self.skill_slots.copy()}")
    
    def skill_joystick(self, direction):
        """
        技能摇杆
        direction: 'up'上(1), 'left'左(2), 'right'右(3), 'down'下(4)
        """
        direction_map = {
            'up': 1,
            'left': 2,
            'right': 3,
            'down': 4
        }
        
        if direction not in direction_map:
            raise ValueError("方向必须是 up/left/right/down")
        
        seal = direction_map[direction]
        self.add_seal(seal)
        self.update_skills()
        self.log.append(f"摇杆{direction} → 印槽:{self.seal_slots} 技能:{self.skill_slots.copy()}")
    
    def execute_combo(self, actions):
        """
        执行一连串操作
        actions: 操作列表，如 ['1A', '2A', '3A', 'up', 'down']
        """
        self.log = []
        for action in actions:
            if action.endswith('A'):
                stage = int(action[0])
                self.normal_attack(stage)
            else:
                self.skill_joystick(action)
    
    def get_current_skills(self):
        """获取当前子技能队列"""
        return self.skill_slots.copy()
    
    def get_current_seals(self):
        """获取当前印槽"""
        return self.seal_slots.copy()
    
    def print_state(self):
        """打印当前状态"""
        print(f"印槽: {self.seal_slots}")
        print(f"当前印集合: {self.get_seal_set()}")
        print(f"当前判定技能: {self.judge_skill()}")
        print(f"子技能队列: {self.skill_slots}")
    
    def print_log(self):
        """打印操作日志"""
        for entry in self.log:
            print(entry)


# ============ 测试用例 ============

if __name__ == "__main__":
    
    print("=" * 50)
    print("测试1：开局上滑")
    print("=" * 50)
    ninja = HokageShinobi()
    ninja.skill_joystick('up')
    ninja.print_state()
    print()
    
    print("=" * 50)
    print("测试2：开局2A")
    print("=" * 50)
    ninja2 = HokageShinobi()
    ninja2.normal_attack(1)  # 1A
    ninja2.normal_attack(2)  # 2A
    ninja2.print_state()
    print()
    
    print("=" * 50)
    print("测试3：开局3A+右滑")
    print("=" * 50)
    ninja3 = HokageShinobi()
    ninja3.execute_combo(['1A', '2A', '3A', 'right'])
    ninja3.print_state()
    ninja3.print_log()
    print()
    
    print("=" * 50)
    print("测试4：任意状态 下滑+4A")
    print("=" * 50)
    ninja4 = HokageShinobi()
    # 先做点操作让状态变化
    ninja4.execute_combo(['up', 'left', '1A', '2A'])
    print("操作前状态:")
    ninja4.print_state()
    print("\n执行 下滑+4A:")
    ninja4.execute_combo(['down', '1A', '2A', '3A', '4A'])
    ninja4.print_state()
    ninja4.print_log()
    print()
    
    print("=" * 50)
    print("测试5：任意状态 5A+上滑")
    print("=" * 50)
    ninja5 = HokageShinobi()
    # 先做点操作
    ninja5.execute_combo(['right', 'down', '1A'])
    print("操作前状态:")
    ninja5.print_state()
    print("\n执行 5A+上滑:")
    ninja5.execute_combo(['1A', '2A', '3A', '4A', '5A', 'up'])
    ninja5.print_state()
    ninja5.print_log()
    print()
    
    print("=" * 50)
    print("测试6：去重机制验证")
    print("=" * 50)
    ninja6 = HokageShinobi()
    print("初始状态:")
    ninja6.print_state()
    print("\n连续产生油火弹（不应重复加入）:")
    ninja6.execute_combo(['1A', '2A', '3A', '4A', '5A'])
    ninja6.print_state()
    print(f"操作日志:")
    ninja6.print_log()