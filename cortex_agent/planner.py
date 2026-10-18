class ActionPlanner:
    """Bẻ nhỏ chỉ thị vĩ mô từ Nexus thành chuỗi hành động cụ thể"""
    @staticmethod
    def create_plan(directive_decision, directed_commands):
        plan = []
        
        # 1. Bước chuẩn bị: Thu thập thông số
        plan.append({
            "step": 1,
            "action": "gather_telemetry",
            "target": "internal_sensors"
        })
        
        # 2. Bước chấp hành cơ bắp
        motor_cmd = directed_commands.get("motor", {})
        torque = motor_cmd.get("torque_pulse", [directive_decision, round(1.0 - directive_decision, 4)])
        plan.append({
            "step": 2,
            "action": "dispatch_motor_pulse",
            "payload": {
                "vector": [round(directive_decision - 0.5, 4), round(abs(directive_decision - 0.5), 4), 1.0],
                "state": "contract" if directive_decision > 0.5 else "relax",
                "torque": torque
            }
        })
        
        # 3. Bước báo cáo: Gửi tín hiệu hoàn thành
        plan.append({
            "step": 3,
            "action": "broadcast_beacon",
            "channel": "global_synapse"
        })
        
        return plan
