"""
Reporting for runner.
"""

def generate_report(scorecard, findings):
    report = "Assessment Report\n\n"
    report += "Scorecard:\n"
    for cit, score in scorecard.items():
        report += f"- {cit}: {score}\n"
    report += "\nFindings:\n"
    for finding in findings:
        report += f"- {finding}\n"
    return report