from control import Engine

engine = Engine()

result = engine.evaluate("Fix timeout bug without breaking API")

print("Action:", result.action)
print("Model:", result.model)
