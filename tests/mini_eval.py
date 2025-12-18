import subprocess


def run(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")


def main():
    run(["python3", "-m", "src.run", "configs/exp_epochs_5.yaml"])
    run(["python3", "src/export_csv.py"])
    run(["python3", "src/analyze_results.py"])
    run(["python3", "src/compare_experiments.py"])

    print("Mini-eval passed successfully.")


if __name__ == "__main__":
    main()

