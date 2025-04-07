import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup


def get_git_log_date(file_path, git_log_args):
    try:
        result = subprocess.run(
            ["git", "log"] + git_log_args + ["--", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout:
            date_str = result.stdout.splitlines()[0]
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except subprocess.CalledProcessError:
        pass
    raise ValueError(f"Could not find date for {file_path}")


def get_creation_date(file_path):
    return get_git_log_date(file_path, ["--diff-filter=A", "--format=%aD"]).strftime(
        "%b %d, %Y"
    )


def get_last_updated_date(file_path):
    return get_git_log_date(file_path, ["-1", "--format=%aD"]).strftime("%b %d, %Y")


def find_source_file(base_path):
    # Try with provided extensions
    for ext in [".rst", ".py", ".md"]:
        source_file_path = base_path + ext
        if os.path.exists(source_file_path):
            return source_file_path

    # Try looking in the current directory
    if os.path.exists(base_path):
        return base_path

    # Try looking in the parent directory
    parent_dir = os.path.dirname(base_path)
    base_name = os.path.basename(base_path)
    for ext in [".rst", ".py", ".md"]:
        parent_source_path = os.path.join(parent_dir, base_name + ext)
        if os.path.exists(parent_source_path):
            return parent_source_path

    return None


def process_html_files(
    build_dir: str,
    paths_to_skip: List[str],
    source_to_build_mapping: Dict[str, str],
):
    print(f"Processing HTML files in {build_dir}")
    print(f"Source to build mapping: {source_to_build_mapping}")

    for build_subdir, source_subdir in source_to_build_mapping.items():
        build_path = os.path.join(build_dir, build_subdir)
        print(f"Checking build path: {build_path}")

        if not os.path.exists(build_path):
            print(f"Build path does not exist: {build_path}")
            continue

        for root, _, files in os.walk(build_path):
            for file in files:
                if not file.endswith(".html"):
                    continue

                html_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(html_file_path, build_dir)
                path_without_ext = os.path.splitext(rel_path)[0]

                print(f"Processing HTML file: {html_file_path}")
                print(f"Relative path: {path_without_ext}")

                if path_without_ext in paths_to_skip:
                    print(f"Skipping path: {path_without_ext}")
                    continue

                source_file_path = None
                for prefix, src_dir in source_to_build_mapping.items():
                    if path_without_ext.startswith(prefix):
                        base_source_path = (
                            os.path.join(src_dir, path_without_ext[len(prefix) + 1 :])
                            if prefix
                            else os.path.join(src_dir, path_without_ext)
                        )
                        print(f"Looking for source file at: {base_source_path}")
                        source_file_path = find_source_file(base_source_path)
                        if source_file_path:
                            print(f"Found source file: {source_file_path}")
                            break

                if not source_file_path:
                    print(f"Warning: Source file not found for path {path_without_ext}")
                    continue

                try:
                    created_on = get_creation_date(source_file_path)
                    last_updated = get_last_updated_date(source_file_path)
                    print(f"Created on: {created_on}, Last updated: {last_updated}")
                except ValueError as e:
                    print(f"Warning: {e}")
                    continue

                with open(html_file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")

                existing_date_info = soup.find("p", {"class": "date-info"})
                if existing_date_info:
                    print(f"Found existing date info, removing it")
                    existing_date_info.decompose()

                h1_tag = soup.find("h1")
                if h1_tag:
                    print(f"Found h1 tag, adding date info")
                    date_info_tag = soup.new_tag("p", **{"class": "date-info"})
                    date_info_tag["style"] = "color: #6c6c6d; font-size: small;"
                    date_info_tag.string = (
                        f"Created On: {created_on} | " f"Last Updated: {last_updated}"
                    )
                    h1_tag.insert_after(date_info_tag)

                    with open(html_file_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    print(f"Updated HTML file with date info")
                else:
                    print(f"Warning: <h1> tag not found in {html_file_path}")


def add_dates_to_html(
    build_dir: str,
    paths_to_skip: Optional[List[str]] = None,
    source_to_build_mapping: Optional[Dict[str, str]] = None,
    enabled: bool = True,
):
    """
    Add creation and last updated dates to HTML files.

    Args:
        build_dir: Directory containing built HTML files
        paths_to_skip: List of paths to skip processing
        source_to_build_mapping: Mapping of source directories to build directories
        enabled: Whether to enable date addition (default: True)
    """
    if not enabled:
        print("Date addition is disabled. Skipping.")
        return

    if paths_to_skip is None:
        paths_to_skip = []

    if source_to_build_mapping is None:
        source_to_build_mapping = {"": ""}

    print(f"Adding dates to HTML files in {build_dir}")
    process_html_files(build_dir, paths_to_skip, source_to_build_mapping)
    print("Finished processing HTML files.")
