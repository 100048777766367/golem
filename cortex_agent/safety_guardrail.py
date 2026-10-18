class SafetyGuardrail:
    """Màng bảo hộ EMETH: Khóa chặt mọi hành vi phá hoại hoặc cực đoan"""
    @staticmethod
    def audit_plan(plan, contract_rules):
        approved_steps = []
        veto_count = 0

        for step in plan:
            action = step.get("action", "")
            payload = step.get("payload", {})
            
            # Khóa 1: Không cho phép xuất vector lực quá lớn gây hỏng cơ bắp
            if action == "dispatch_motor_pulse":
                vector = payload.get("vector", [0, 0, 0])
                if any(abs(v) > 5.0 for v in vector):
                    print(f"🛑 [EMETH VETO] Lực cơ bắp quá tải {vector}! Từ chối chấp hành.")
                    veto_count += 1
                    continue

            approved_steps.append(step)

        return approved_steps, veto_count
