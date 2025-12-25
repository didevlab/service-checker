import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: update_docker_docs.py <version>")
        return 1

    version = sys.argv[1].strip()
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"invalid version: {version}")
        return 1

    path = Path("DOCKER.md")
    if not path.exists():
        print("DOCKER.md not found")
        return 1

    content = path.read_text(encoding="utf-8")
    new_tag = f"v{version}"
    updated = re.sub(r"v(?:X\.Y\.Z|\d+\.\d+\.\d+)", new_tag, content)

    if updated != content:
        path.write_text(updated, encoding="utf-8")
        print(f"Updated DOCKER.md to {new_tag}")
    else:
        print("DOCKER.md already up to date")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
