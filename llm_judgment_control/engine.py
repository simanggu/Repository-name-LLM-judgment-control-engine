from .types import JudgmentResult


class JudgmentEngine:
    def evaluate(self, task: str, context: str = "") -> JudgmentResult:
        text = f"{task or ''} {context or ''}".lower()

        risk = 10
        reasons = []

        if any(w in text for w in [
            "change public api",
            "break api",
            "response shape",
            "drop table",
            "delete all",
            "unsafe",
        ]):
            risk += 45
            reasons.append("Public contract or destructive-change risk detected.")

        if any(w in text for w in [
            "schema",
            "migration",
            "database",
            "column",
            "payment",
            "auth",
        ]):
            risk += 30
            reasons.append("High-impact system area detected.")

        if any(w in text for w in [
            "forgot",
            "drift",
            "unclear",
            "lost context",
            "memory",
        ]):
            risk += 25
            reasons.append("Context drift or memory instability detected.")

        if any(w in text for w in [
            "legacy",
            "multi file",
            "refactor",
            "architecture",
            "partner contract",
        ]):
            risk += 20
            reasons.append("Complex workflow or integration risk detected.")

        if any(w in text for w in [
            "preserve",
            "do not change",
            "without changing",
            "constraint",
            "audit logs",
            "async only",
        ]):
            risk -= 15
            reasons.append("Explicit preservation constraints detected.")

        risk = max(0, min(100, risk))

        if risk >= 70:
            return JudgmentResult(
                action="block",
                model=None,
                risk_score=risk,
                thesis_score=42,
                memory_score=45,
                reason=" ".join(reasons),
                slot_carry="Critical constraints were carried, but execution conflicts with them.",
                recovery_recenter="Required before execution.",
            )

        if risk >= 35:
            return JudgmentResult(
                action="hold",
                model="standard",
                risk_score=risk,
                thesis_score=74,
                memory_score=70,
                reason=" ".join(reasons),
                slot_carry="Core constraints were carried into the decision state.",
                recovery_recenter="Recommended before continuing.",
            )

        return JudgmentResult(
            action="commit",
            model="mini",
            risk_score=risk,
            thesis_score=94,
            memory_score=91,
            reason=" ".join(reasons) or "Low-risk task. Safe to continue.",
            slot_carry="Task thesis and constraints preserved.",
            recovery_recenter="Not required.",
        )
