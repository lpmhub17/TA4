# TA4 - Laptop Troubleshooting with RBR and CBR

Technical Assessment 4 for **CS0065 - Intelligent Systems**. This Python program demonstrates knowledge representation, rule-based reasoning (RBR), and case-based reasoning (CBR) using a laptop troubleshooting example.

## Files

| File | Description |
| --- | --- |
| [TA4_laptop_reasoning.py](TA4_laptop_reasoning.py) | Python implementation of the knowledge base, rules, inference engine, and CBR cycle. |
| [TA4 - Technical Assessment.pdf](TA4%20-%20Technical%20Assessment.pdf) | Assessment document containing the code and comparative reflection. |

## Requirements

- Python 3.6 or later (uses only the standard library).
- A terminal, Python IDLE, or VS Code with Python configured.

No additional packages are required.

## Running the program

Clone the repository and enter its folder:

```bash
git clone https://github.com/lpmhub17/TA4.git
cd TA4
```

Run the interactive version:

```bash
python TA4_laptop_reasoning.py
```

At the revision prompt, enter a complete replacement solution or press **Enter** to keep the retrieved solution.

For a repeatable demonstration that automatically adds a slow-performance action:

```bash
python TA4_laptop_reasoning.py --demo
```

On Windows, `py` can be used instead of `python` if the Python launcher is installed. On macOS or Linux, use `python3` if needed. In VS Code, open the Python file and choose **Run Python File** to use the interactive version.

## Knowledge representation

The current laptop is represented by five Boolean facts in three categories:

| Category | Fact | Default value |
| --- | --- | --- |
| Power | `turns_on` | `True` |
| Power | `charger_connected` | `True` |
| Cooling | `overheating` | `True` |
| Cooling | `fan_noisy` | `True` |
| Performance | `runs_slowly` | `True` |

Edit the `facts` dictionary near the top of the script to try a different situation. The same input is passed to both reasoning systems.

## Rule-based reasoning

Four functions implement IF-THEN rules:

- **Power:** If the laptop does not turn on and its charger is disconnected, suggest connecting the charger and checking power.
- **Heat:** If the laptop turns on and overheats, suggest shutting down, allowing it to cool, and checking for blocked vents.
- **Fan:** If the laptop turns on and its fan is noisy, suggest checking airflow and having persistent noise inspected.
- **Performance:** If the laptop turns on and runs slowly, suggest closing unnecessary background apps when safe to restart.

The inference engine checks every rule and returns all matching actions. For the default input, the heat, fan, and performance rules fire.

## Case-based reasoning

Three illustrative past cases contain problem features and matching solutions. The program follows the four-step cycle:

1. **Retrieve:** Compare the current facts with every past case. Similarity is the number of matching facts divided by the number of current facts. All five facts have equal weight, and ties select the first matching best case.
2. **Reuse:** Return the highest-scoring case's solution.
3. **Revise:** Keep the solution or replace it manually. Demo mode adds an action for slow performance.
4. **Retain:** Append the current problem and final solution as a new case, using a separate copy of the problem data.

For the default input:

| Case | Similarity |
| --- | --- |
| C1 | 0% |
| C2 | 80% |
| C3 | 60% |

C2 is selected. After revision, the program retains C4, increasing the case count from three to four.

## Example output

The RBR action section is:

```text
Rule-Based Reasoning Actions:
- Shut down, let the laptop cool, and check for blocked vents.
- Check airflow; have persistent fan noise inspected.
- When safe to restart, close unnecessary background apps.
```

The CBR retrieval scores are:

```text
  C1: 0% similarity
  C2: 80% similarity
  C3: 60% similarity
Retrieve: C2 selected (80%).
```

The program also prints the reused and revised solutions and confirms that the new case was retained.

## Scope and limitations

This is a small educational example using structured Boolean facts and illustrative cases. Similarity measures feature agreement, not diagnostic confidence. There is no minimum similarity threshold, so a nonempty case base always returns its highest-scoring case. Retained cases exist only in memory during the current run; the next run starts with the original three cases. The program does not automatically verify that a proposed solution fixes the laptop.
