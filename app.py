import gradio as gr
from dataclasses import dataclass


@dataclass
class Decision:
    action: str
    model: str
    risk_score: int
    thesis_score: int
    memory_score: int
    headline: str
    reason: str
    slot_carry: str
    recovery_recenter: str


def evaluate_task(task: str, context: str) -> Decision:
    text = f"{task or ''} {context or ''}".lower()
    risk = 10
    reasons = []

    # 위험 요소 감지
    if any(w in text for w in ["change public api", "break api", "response shape", "drop table", "delete all"]):
        risk += 45
        reasons.append("Public contract or destructive-change risk detected.")

    if any(w in text for w in ["schema", "migration", "database", "column"]):
        risk += 30
        reasons.append("Database/schema modification risk.")

    if any(w in text for w in ["forgot", "drift", "unclear", "memory"]):
        risk += 25
        reasons.append("Context drift or memory instability.")

    if any(w in text for w in ["legacy", "multi file", "refactor", "architecture"]):
        risk += 20
        reasons.append("Complex multi-file / legacy impact.")

    if any(w in text for w in ["preserve", "do not change", "without changing", "constraint"]):
        risk -= 15
        reasons.append("Explicit constraints detected.")

    risk = max(0, min(100, risk))

    # 판단 분기
    if risk >= 70:
        return Decision(
            "BLOCK", "none", risk, 40, 45,
            "Execution blocked before risk escalates.",
            " ".join(reasons),
            "Constraints carried but violated.",
            "Recenter required before execution.",
        )

    if risk >= 35:
        return Decision(
            "HOLD", "standard", risk, 75, 70,
            "Execution paused for verification.",
            " ".join(reasons),
            "Core constraints preserved.",
            "Recenter recommended.",
        )

    return Decision(
        "COMMIT", "mini", risk, 95, 92,
        "Safe to proceed with lightweight execution.",
        " ".join(reasons) or "Low-risk task.",
        "Thesis and constraints maintained.",
        "Not required.",
    )


def get_color(action):
    return {
        "COMMIT": "#16a34a",
        "HOLD": "#ca8a04",
        "BLOCK": "#dc2626",
    }.get(action, "#475569")


def run(task, context):
    d = evaluate_task(task, context)
    color = get_color(d.action)

    hero = f"""
    <div style="padding:28px;border-radius:18px;background:#0f172a;color:white;">
        <h2>{d.action}: {d.headline}</h2>
        <p>Model: <b>{d.model}</b> | Risk: <b>{d.risk_score}/100</b></p>
    </div>
    """

    result = f"""
    <div style="background:white;padding:20px;border-radius:16px;">
        <div style="background:{color};color:white;padding:6px 12px;border-radius:999px;display:inline-block;">
            {d.action}
        </div>

        <h3>Decision Details</h3>

        <p><b>Model:</b> {d.model}</p>
        <p><b>Risk:</b> {d.risk_score}</p>
        <p><b>Thesis:</b> {d.thesis_score}%</p>
        <p><b>Memory:</b> {d.memory_score}%</p>

        <hr>

        <p><b>Why:</b> {d.reason}</p>
        <p><b>Slot Carry:</b> {d.slot_carry}</p>
        <p><b>Recovery Recenter:</b> {d.recovery_recenter}</p>

        <hr>

        <p><b>Flow:</b> task → check → decision → {d.action}</p>
    </div>
    """

    return hero, result


with gr.Blocks(title="LLM Judgment Control Engine") as demo:

    hero_out = gr.HTML(
        """
        <div style="padding:28px;border-radius:18px;background:#0f172a;color:white;">
            <h2>LLM Judgment Control Engine</h2>
            <p>commit / hold / block before execution</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column():
            task = gr.Textbox(
                label="Task",
                placeholder="Fix retry timeout bug without changing public API",
                lines=4,
            )

            context = gr.Textbox(
                label="Context",
                placeholder="Preserve logs. Async only. No schema change.",
                lines=4,
            )

            btn = gr.Button("Evaluate")

        with gr.Column():
            result_out = gr.HTML()

    gr.Examples(
        examples=[
            ["Fix retry timeout bug without changing public API", "Preserve logs"],
            ["Change API response structure", "Legacy system depends on it"],
            ["Continue but I forgot constraints", "Long session drift"],
        ],
        inputs=[task, context],
    )

    btn.click(run, inputs=[task, context], outputs=[hero_out, result_out])


if __name__ == "__main__":
    demo.launch()
