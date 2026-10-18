class MotorBridge:
    """Cầu nối dẫn truyền xung lực cho repo cơ bắp motor"""
    @staticmethod
    def format_motor_command(dx, dy, force, state):
        return {
            "target": "motor",
            "action_vector": [round(dx, 4), round(dy, 4), round(force, 4)],
            "muscle_contraction": state,
            "actuation_certified": True
        }
