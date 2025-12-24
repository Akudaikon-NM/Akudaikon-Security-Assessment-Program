"""
CLI runner for the assessor.
"""

import argparse
import json
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from core.scoring import load_module, generate_scorecard
from core.findings import generate_findings

def run_assessment(module: str, input_file: str, export: str):
    """Run the assessment."""
    # Load answers (assume JSON with overall compliance)
    with open(input_file, 'r') as f:
        answers = json.load(f)
    
    # Load module
    module_data = load_module(module)
    
    # Generate scorecard
    scorecard = generate_scorecard(module_data, answers)
    
    # Generate findings
    findings = generate_findings(module_data, scorecard)
    
    # Export
    if export == 'json':
        output = {
            'module': module_data['title'],
            'scorecard': scorecard,
            'findings': findings
        }
        print(json.dumps(output, indent=2))
    elif export == 'pdf':
        # Placeholder for PDF export
        print("PDF export not implemented yet.")
        print("Scorecard:", scorecard)
        print("Findings:", findings)
    else:
        print("Scorecard:", scorecard)
        print("Findings:", findings)

def main():
    parser = argparse.ArgumentParser(description="Akudaikon Security Assessor CLI")
    subparsers = parser.add_subparsers(dest='command')
    
    run_parser = subparsers.add_parser('run', help='Run assessment')
    run_parser.add_argument('--module', required=True, help='Module name (e.g., 748)')
    run_parser.add_argument('--input', required=True, help='Input answers JSON file')
    run_parser.add_argument('--export', choices=['json', 'pdf'], default='text', help='Export format')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_assessment(args.module, args.input, args.export)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()