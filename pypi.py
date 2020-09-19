import re
import shutil
import sys
from pathlib import Path
from subprocess import check_call

version_re = re.compile(r'version="[\d.]+",')


def upload(new_version: str) -> None:
    """Upload new version to pypi."""
    # Set new version
    setup = Path(__file__).parent / "setup.py"

    contents = setup.read_text(encoding="utf-8")
    contents = version_re.sub(f'version="{new_version.strip()}",', contents, count=1)

    setup.write_text(contents, encoding="utf-8")

    # Build release
    check_call([sys.executable, "setup.py", "sdist", "bdist_wheel"])

    # Upload release
    check_call([sys.executable, "-m", "twine", "upload", "dist/*"])


if __name__ == "__main__":
    try:
        upload(sys.argv[1])
    finally:
        # Cleanup
        for folder in ("build", "color_wallpaper.egg-info", "dist"):
            shutil.rmtree(folder, ignore_errors=True)
