import csv
import json
import os
import time
from agent import run_agent

INPUT_FILE = "../support_tickets/support_tickets.csv"
OUTPUT_FILE = "../support_tickets/output.csv"

OUTPUT_FIELDS = ["Issue", "Subject", "Company", "status", "product_area", "response", "justification", "request_type"]

def process_tickets():
    

    # Read input
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tickets = list(reader)

    print(f"Processing {len(tickets)} tickets...\n")

    results = []

    for i, ticket in enumerate(tickets):
        issue = ticket.get("Issue", "").strip()
        subject = ticket.get("Subject", "").strip()
        company = ticket.get("Company", "None").strip()

        print(f"[{i+1}/{len(tickets)}] {company} | {subject or issue[:50]}")

        result = run_agent(issue, subject, company)

        results.append({
            "Issue": issue,
            "Subject": subject,
            "Company": company,
            "status": result.get("status", "escalated"),
            "product_area": result.get("product_area", "unknown"),
            "response": result.get("response", ""),
            "justification": result.get("justification", ""),
            "request_type": result.get("request_type", "product_issue")
        })

        print(f"  → {result.get('status')} | {result.get('request_type')} | {result.get('product_area')}")

        time.sleep(3)  # avoid rate limiting

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    
    

    print(f"\nDone! Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Support Triage Agent — HackerRank · Claude · Visa"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the triage agent on the input file"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="../support_tickets/support_tickets.csv",
        help="Path to input CSV file (default: ../support_tickets/support_tickets.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../support_tickets/output.csv",
        help="Path to output CSV file (default: ../support_tickets/output.csv)"
    )

    args = parser.parse_args()

    if args.run:
        INPUT_FILE = args.input
        OUTPUT_FILE = args.output
        process_tickets()
    else:
        parser.print_help()