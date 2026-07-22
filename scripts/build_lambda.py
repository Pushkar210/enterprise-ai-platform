import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python build_lambda.py <lambda_source_directory>")
    sys.exit(1)

source = Path(sys.argv[1]).resolve()

if not source.exists():
    raise FileNotFoundError(f"{source} does not exist")

build_dir = source / ".build"
zip_file = source / "lambda.zip"

# Clean previous build
if build_dir.exists():
    shutil.rmtree(build_dir)

if zip_file.exists():
    zip_file.unlink()

build_dir.mkdir()

# Install dependencies inside the official AWS Lambda Python 3.13 container
requirements = source / "requirements.txt"

if requirements.exists():
    subprocess.check_call([
    "docker",
    "run",
    "--rm",
    "--platform",
    "linux/amd64",
    "--entrypoint",
    "/bin/bash",
    "-v",
    f"{source}:/var/task",
    "-v",
    f"{build_dir}:/opt/build",
    "public.ecr.aws/lambda/python:3.13",
    "-c",
    "pip install -r /var/task/requirements.txt -t /opt/build"
])

# Copy source files
for item in source.iterdir():
    if item.name in {
        ".build",
        "__pycache__",
        "lambda.zip"
    }:
        continue

    destination = build_dir / item.name

    if item.is_dir():
        shutil.copytree(item, destination)
    else:
        shutil.copy2(item, destination)

# Create ZIP
shutil.make_archive(
    str(zip_file.with_suffix("")),
    "zip",
    build_dir
)

# Cleanup
shutil.rmtree(build_dir)

print(f"✅ Created {zip_file}") 