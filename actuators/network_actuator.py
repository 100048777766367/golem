from cortex_agent.tool_registry import ToolRegistry

class NetworkActuator:
    """Chấp hành các hành động truyền phát mạng lưới"""
    @staticmethod
    def emit_pulse(target_url, action_payload):
        if not target_url or not target_url.startswith("http"):
            return {"dispatched": False, "reason": "local_mock_pulse"}
        
        res = ToolRegistry.tool_send_webhook(target_url, action_payload)
        return {"dispatched": res.get("success", False), "details": res}
