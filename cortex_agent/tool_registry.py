import json
import urllib.request

class ToolRegistry:
    """Kho công cụ tác tử chuẩn hóa"""
    
    @staticmethod
    def tool_send_webhook(url, payload_dict, timeout=4):
        """Bắn xung Webhook ra thế giới thực"""
        try:
            data = json.dumps(payload_dict).encode("utf-8")
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={"Content-Type": "application/json", "User-Agent": "Golem-Agent"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return {"status": resp.status, "success": True}
        except Exception as e:
            return {"status": 0, "success": False, "error": str(e)}

    @staticmethod
    def tool_format_payload(decision, epoch, action_name):
        """Đóng gói dữ liệu đầu ra"""
        return {
            "source": "golem_agent",
            "epoch": epoch,
            "action": action_name,
            "decision": decision
        }
