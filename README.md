# 🦾 BODHI-GOLEM: TÁC TỬ HÀNH ĐỘNG TỰ THÂN (AUTONOMOUS ACTION AGENT)
> *"Nhận mệnh lệnh vĩ mô từ Nexus, lập kế hoạch hành động, chấp hành cơ bắp ra thế giới thực và bảo toàn khế ước đạo đức EMETH."*

---

## 🏛️ CẤU TRÚC ĐIỀU HÀNH GOLEM:
1. **`cortex_agent/planner.py`:** Bẻ nhỏ chỉ thị vĩ mô thành chuỗi bước đi thực tế.
2. **`cortex_agent/safety_guardrail.py`:** Màng lọc an toàn EMETH kiểm soát lực cơ bắp và chống hành động phá hoại.
3. **`actuators/motor_bridge.py`:** Dẫn truyền vector động lực học 3 chiều `[dx, dy, F]` trực tiếp cho cơ quan vận động `motor`.
4. **`kernel.py`:** Thống lĩnh tác tử tự động hóa 100%, bảo đảm luật Apoptosis của `contract`.

```
100048777766367/golem/
├── contract.json                  # 📜 [HIẾN ƯỚC q]: Vai trò AUTONOMOUS_ACTION_AGENT
├── kernel.py                      # 🦾 [THỐNG LĨNH TÁC TỬ]: Lập kế hoạch, kiểm tra an toàn, Apoptosis
│
├── cortex_agent/                  # 🧠 [BỘ NÃO ĐIỀU PHỐI HÀNH ĐỘNG]
│   ├── __init__.py
│   ├── planner.py                 # Bẻ nhỏ mệnh lệnh cấp cao thành chuỗi hành động (Action Plan)
│   ├── tool_registry.py           # Kho vũ khí/công cụ thực thi (HTTP Webhook, Dispatch, File IO)
│   └── safety_guardrail.py        # Màng kiểm soát an toàn EMETH (Khóa hành động vi phạm hợp đồng)
│
├── actuators/                     # 🦾 [CƠ CẤU CHẤP HÀNH THỰC TẾ]
│   ├── __init__.py
│   ├── network_actuator.py        # Bắn xung thần kinh & Webhook ra Internet
│   └── motor_bridge.py            # Cầu nối ra lệnh co/duỗi cho cơ bắp Level 4 (motor [dx, dy, F])
│
├── organs/                        # 🧩 Nơi cắm thêm công cụ tác tử mở rộng [r] (lỗi cú pháp tự hủy)
│   └── .gitkeep
├── synapses/                      # 💾 Sổ cái tác tử & Danh bạ
│   ├── .gitkeep
│   ├── peers.json                 # Danh bạ các nút chỉ huy và cơ bắp
│   ├── state.json                 # Kỷ nguyên tác tử
│   └── action_ledger.json         # Sổ vết tích lịch sử hành động đã thực thi
│
├── Dockerfile                     # python:3.14-slim
├── README.md                      # Tuyên ngôn Tác Tử Golem
└── .github/
    └── workflows/
        └── node.yml               # Workflow setup-python@v7 & python 3.14
```







