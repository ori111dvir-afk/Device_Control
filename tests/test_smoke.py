import subprocess
import sys
from pathlib import Path
import unittest


class SmokeTest(unittest.TestCase):
    def test_main_runs_with_three_filter_configs(self):
        project_root = Path(__file__).resolve().parents[1]
        src_dir = project_root / "src"
        fixtures_dir = project_root / "tests" / "fixtures"

        config_names = ["moving_average", "moving_median", "low_pass"]

        for name in config_names:
            config_path = fixtures_dir / f"{name}.ini"
            print(f"Running main.py with config: {config_path}")
            result = subprocess.run(
                [sys.executable, str(src_dir / "main.py"), str(config_path)],
                cwd=str(src_dir),
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn(
                "WARNING:",
                result.stdout,
                msg=f"Expected a warning for filter config {name}, got output:\n{result.stdout}",
            )

            print(f"=== {name} output ===\n{result.stdout}")


if __name__ == "__main__":
    unittest.main()