import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_LOG = Path(__file__).parent.parent / ".token_usage.json"
VALID_ROLES = {"user", "assistant", "system", "tool"}


def estimate_tokens(text):
    """Estimate tokens as one token per 0.75 words."""
    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    return math.ceil(word_count / 0.75)


def load_usage(path=DEFAULT_LOG):
    path = Path(path)
    if not path.exists():
        return {
            "method": "1 estimated token per 0.75 words",
            "total_tokens": 0,
            "interactions": [],
        }

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_usage(usage, path=DEFAULT_LOG):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(usage, file, indent=2)


def log_interaction(text, role="user", path=DEFAULT_LOG):
    if role not in VALID_ROLES:
        raise ValueError("role must be one of: " + ", ".join(sorted(VALID_ROLES)))

    usage = load_usage(path)
    tokens = estimate_tokens(text)
    interaction = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "tokens": tokens,
        "text": text,
    }
    usage["interactions"].append(interaction)
    usage["total_tokens"] = sum(item["tokens"] for item in usage["interactions"])
    save_usage(usage, path)
    return interaction


def print_usage(path=DEFAULT_LOG):
    usage = load_usage(path)
    print(f"Estimated total: {usage['total_tokens']} tokens")
    print(f"Interactions: {len(usage['interactions'])}")
    print(f"Method: {usage['method']}")


def main():
    parser = argparse.ArgumentParser(description="Log estimated AI interaction tokens.")
    parser.add_argument("text", nargs="?", help="Interaction text; omit to read from standard input.")
    parser.add_argument("--role", choices=sorted(VALID_ROLES), default="user")
    parser.add_argument("--report", action="store_true", help="Show the current total without logging.")
    parser.add_argument("--file", type=Path, default=DEFAULT_LOG, help="Usage log location.")
    args = parser.parse_args()

    if args.report:
        print_usage(args.file)
        return

    text = args.text
    if text is None:
        text = input()
    interaction = log_interaction(text, role=args.role, path=args.file)
    print(f"Logged {interaction['tokens']} estimated tokens as {interaction['role']}.")
    print_usage(args.file)


if __name__ == "__main__":
    main()
