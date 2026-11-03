import sys
from copy import deepcopy


facts = {
    "power": {"turns_on": True, "charger_connected": True},
    "cooling": {"overheating": True, "fan_noisy": True},
    "performance": {"runs_slowly": True},
}


def rule_power(problem):
    if (not problem["power"]["turns_on"]
            and not problem["power"]["charger_connected"]):
        return "Connect the charger and check the power connection."


def rule_heat(problem):
    if problem["power"]["turns_on"] and problem["cooling"]["overheating"]:
        return "Shut down, let the laptop cool, and check for blocked vents."


def rule_fan(problem):
    if problem["power"]["turns_on"] and problem["cooling"]["fan_noisy"]:
        return "Check airflow; have persistent fan noise inspected."


def rule_slow(problem):
    if (problem["power"]["turns_on"]
            and problem["performance"]["runs_slowly"]):
        return "When safe to restart, close unnecessary background apps."


def infer(problem):
    """Check every rule and collect all matching actions."""
    actions = []
    for rule in [rule_power, rule_heat, rule_fan, rule_slow]:
        action = rule(problem)
        status = "FIRED" if action else "not matched"
        print(f"  {rule.__name__}: {status}")
        if action:
            actions.append(action)
    return actions


case_base = [
    {"id": "C1", "problem": {
        "power": {"turns_on": False, "charger_connected": False},
        "cooling": {"overheating": False, "fan_noisy": False},
        "performance": {"runs_slowly": False}},
     "solution": "Connect the charger and check the power connection."},
    {"id": "C2", "problem": {
        "power": {"turns_on": True, "charger_connected": True},
        "cooling": {"overheating": True, "fan_noisy": True},
        "performance": {"runs_slowly": False}},
     "solution": (
         "Shut down, let the laptop cool, and check for blocked vents. "
         "Have persistent fan noise inspected.")},
    {"id": "C3", "problem": {
        "power": {"turns_on": True, "charger_connected": True},
        "cooling": {"overheating": False, "fan_noisy": False},
        "performance": {"runs_slowly": True}},
     "solution": "Close unnecessary background apps and review startup apps."},
]


def similarity(new_problem, old_problem):
    """Equal-weight exact matching: matching facts / total facts."""
    matches = 0
    total = 0
    for category, values in new_problem.items():
        for feature, value in values.items():
            total += 1
            old_values = old_problem.get(category, {})
            if feature in old_values and old_values[feature] == value:
                matches += 1
    return matches / total if total else 0.0


def retrieve(problem, cases):
    """Return the highest-scoring case; ties keep the first case."""
    best_case, best_score = None, -1.0
    for case in cases:
        score = similarity(problem, case["problem"])
        print(f"  {case['id']}: {score:.0%} similarity")
        if score > best_score:
            best_case, best_score = case, score
    return best_case, best_score


def reuse(case):
    return case["solution"]


def revise(solution, replacement=""):
    """A blank replacement keeps the retrieved solution unchanged."""
    return replacement.strip() or solution


def retain(problem, solution, cases):
    """Store a separate copy, so later input edits cannot alter history."""
    cases.append({"id": f"C{len(cases) + 1}",
                  "problem": deepcopy(problem), "solution": solution})


def main(demo=False):
    print("TA4 - LAPTOP TROUBLESHOOTING")
    print("INPUT: Current laptop facts")
    for category, values in facts.items():
        print(f"  {category}: {values}")

    print("\nRBR PROCESS: Check every IF-THEN rule")
    actions = infer(facts)
    print("Rule-Based Reasoning Actions:")
    for action in actions or ["No matching rule; seek further information."]:
        print(f"- {action}")

    cases = deepcopy(case_base)
    print("\nCBR PROCESS: Retrieve -> Reuse -> Revise -> Retain")
    best_case, score = retrieve(facts, cases)
    if best_case is None:
        print("No past cases available.")
        return
    print(f"Retrieve: {best_case['id']} selected ({score:.0%}).")
    solution = reuse(best_case)
    print(f"Reuse: {solution}")
    if demo:
        replacement = (solution + " When safe to restart, close unnecessary "
                       "background apps.")
        print("Revise: Demo adds an action for the slow performance.")
    else:
        replacement = input("Revised full solution (Enter to keep): ")
    final_solution = revise(solution, replacement)
    print(f"Final CBR solution: {final_solution}")
    before = len(cases)
    retain(facts, final_solution, cases)
    print(f"Retain: Added {cases[-1]['id']}; cases {before} -> {len(cases)}.")
    print("Retention is in memory for this run; no file is saved.")


if __name__ == "__main__":
    main(demo="--demo" in sys.argv)
