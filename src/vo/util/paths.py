from pathlib import Path

def get_repo_root(cwd:Path) -> Path:
    for p in [cwd, *cwd.parents]:
        if (p / "pyproject.toml").exists():
            return p
    raise RuntimeError("Could not find the project root!")

__cwd = Path(__file__).resolve()
VO_TOP = get_repo_root(__cwd)
VO_SRC = VO_TOP / "src"
VO_DATA = VO_TOP / "data"
VO_TESTS = VO_TOP / "tests"
TEST_DATA = VO_TESTS / "data"