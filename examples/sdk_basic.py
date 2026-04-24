from llm_judgment_control import JudgmentEngine


engine = JudgmentEngine()

result = engine.evaluate(
    task="Fix retry timeout bug without changing public API",
    context="Preserve audit logs. Async only. Do not change schema.",
)

print("Action:", result.action)
print("Model:", result.model)
print("Risk:", result.risk_score)
print("Thesis:", result.thesis_score)
print("Memory:", result.memory_score)
print("Reason:", result.reason)
