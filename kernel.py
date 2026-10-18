import os
import sys
import json
import time
import hashlib
import urllib.request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex_agent.planner import ActionPlanner
from cortex_agent.safety_guardrail import SafetyGuardrail
from actuators.motor_bridge import MotorBridge

STATE_FILE = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"
LEDGER_FILE = "synapses/action_ledger.json"

class GolemKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/golem")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.contract_repo = f"{self.owner}/contract"
        
        self.ensure_skeleton()
        self.epoch = self.load_epoch()
        self.sources = self.load_sources()

    def ensure_skeleton(self):
        for folder in ["cortex_agent", "actuators", "organs", "synapses"]:
            os.makedirs(folder, exist_ok=True)

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def load_sources(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("command_sources", [])
            except Exception: pass
        return [f"{self.owner}/nexus-08", f"{self.owner}/motor", self.contract_repo]

    def enforce_contract_apoptosis(self):
        """[t] Áp dụng luật Apoptosis của Contract: tự hủy tệp lỗi trong organs/"""
        for root, _, files in os.walk("organs"):
            for f in files:
                if f.endswith(".py"):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "r", encoding="utf-8") as cf:
                            compile(cf.read(), fp, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS CONTRACT] '{f}' lỗi cú pháp ({se})! Xóa sổ tệp.")
                        try: os.remove(fp)
                        except Exception: pass

    def harvest_directive(self):
        """Hút chỉ thị vĩ mô từ Nexus-08"""
        nexus_repo = f"{self.owner}/nexus-08"
        url = f"https://raw.githubusercontent.com/{nexus_repo}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Golem-Agent"})
            with urllib.request.urlopen(req, timeout=3.5) as r:
                if r.status == 200:
                    data = json.loads(r.read().decode("utf-8"))
                    print(f"📥 [CHỈ THỊ VĨ MÔ] Đã bắt sóng nhịp đập từ '{nexus_repo}'!")
                    return data
        except Exception: pass
        return {"decision": 0.542, "transmuted_signals": {}}

    def run(self):
        print("=" * 80)
        print(f"🦾 [GOLEM ACTION AGENT] KHỞI ĐỘNG VÒNG ĐỜI TÁC TỬ #{self.epoch}")
        print(f"🧱 Bản Thể: Tác Tử Hành Động Tự Thân – Khế Ước EMETH Bất Tử")
        print("=" * 80)

        # 0. Thanh lọc lỗi theo luật Apoptosis
        self.enforce_contract_apoptosis()

        # 1. Hút chỉ thị từ Nexus
        directive = self.harvest_directive()
        decision = float(directive.get("decision", 0.542))
        transmuted = directive.get("transmuted_signals", {})
        directed_cmds = directive.get("directed_commands", {})

        # 2. Lập kế hoạch hành động tác tử (Planning)
        print("🧠 [LẬP KẾ HOẠCH] Đang bẻ nhỏ chỉ thị thành chuỗi hành động...")
        raw_plan = ActionPlanner.create_plan(decision, directed_cmds)
        print(f"  └── 📋 Kế hoạch sơ bộ gồm {len(raw_plan)} bước hành động.")

        # 3. Kiểm soát an toàn EMETH (Safety Guardrails)
        approved_plan, vetoes = SafetyGuardrail.audit_plan(raw_plan, {})
        print(f"🛡️ [MÀNG LỌC EMETH] Đã phê duyệt {len(approved_plan)}/{len(raw_plan)} bước (Veto={vetoes}).")

        # 4. Chấp hành hành động thực tế (Execution)
        executed_records = []
        for step in approved_plan:
            action_name = step.get("action")
            if action_name == "dispatch_motor_pulse":
                payload = step.get("payload", {})
                vec = payload.get("vector", [0, 0, 1.0])
                state = payload.get("state", "relax")
                motor_cmd = MotorBridge.format_motor_command(vec[0], vec[1], vec[2], state)
                print(f"  └── 🦾 [CƠ BẮP MOTOR]: Vector Lực={motor_cmd['action_vector']} | Trạng thái={state}")
                executed_records.append({"step": step["step"], "action": action_name, "status": "DISPATCHED"})
            else:
                executed_records.append({"step": step["step"], "action": action_name, "status": "SIMULATED_LOCAL"})

        # 5. Lưu sổ cái hành động (Action Ledger)
        ledger_data = {"ledger_version": "1.0.0", "records": []}
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                    ledger_data = json.load(f)
            except Exception: pass

        ledger_data["records"].append({
            "epoch": self.epoch,
            "timestamp": int(time.time()),
            "executed_count": len(executed_records),
            "decision": decision
        })
        ledger_data["records"] = ledger_data["records"][-50:]
        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(ledger_data, f, indent=4)

        # 6. Đóng dấu chứng thực Quantum CID
        t = int(time.time())
        seed = f"golem_{self.epoch}_{t}_{len(executed_records)}_{decision}".encode()
        cid = hashlib.shake_256(seed).hexdigest(64)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "generation_epoch": self.epoch,
                "last_action_timestamp": t,
                "actions_executed_count": len(executed_records),
                "quantum_cid": cid,
                "status": "actions_fully_dispatched"
            }, f, indent=4)

        # Xuất gói tin nhịp đập tác tử
        fwd_packet = {
            "contract": "bodhi.contract.v1",
            "identity": self.repo_name,
            "role": "AUTONOMOUS_ACTION_AGENT",
            "epoch": self.epoch,
            "timestamp": t,
            "action_summary": {
                "plan_steps_count": len(approved_plan),
                "motor_dispatched": True,
                "emeth_vetoes": vetoes
            },
            "quantum_cid": cid,
            "status": "golem_acting_with_integrity"
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4)

        print("=" * 80)
        print(f"💾 [CHỨNG THỰC TÁC TỬ CID]: {cid[:24]}...")
        print(f"✨ [CHẤP HÀNH THÀNH CÔNG] Golem Kỷ nguyên #{self.epoch} đã hoàn tất sứ mệnh hành động!")
        print("=" * 80)

if __name__ == "__main__":
    GolemKernel().run()
