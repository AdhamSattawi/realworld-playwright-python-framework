import argparse
import sys
import time

import requests


def main() -> int:
    parser = argparse.ArgumentParser(description="Wait for an HTTP endpoint to become reachable.")
    parser.add_argument("--url", required=True, help="URL to probe")
    parser.add_argument("--timeout", type=int, default=120, help="Maximum wait time in seconds")
    parser.add_argument("--interval", type=int, default=3, help="Seconds between retries")
    args = parser.parse_args()

    deadline = time.time() + args.timeout
    last_error = None

    while time.time() < deadline:
        try:
            response = requests.get(args.url, timeout=5)
            if response.status_code in (200, 302):
                print(f"[CI] Target is reachable: {args.url} ({response.status_code})")
                return 0
        except Exception as error:
            last_error = error

        print("[CI] Waiting for app from test container network...")
        time.sleep(args.interval)

    print(f"[CI] App not reachable from test container: {args.url}; last_error={last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
