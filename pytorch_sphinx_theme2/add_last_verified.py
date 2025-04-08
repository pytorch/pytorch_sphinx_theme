import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Set

from bs4 import BeautifulSoup

def find_source_file(base_path):
    """Find the source file for a given base path."""
    # Try with provided extensions
    for ext in [".rst", ".py", ".md"]:
        source_file_path = base_path + ext
        if os.path.exists(source_file_path):
            return source_file_path
            
    # Try docs directory
    for ext in [".rst", ".py", ".md"]:
        docs_path = os.path.join("docs", base_path + ext)
        if os.path.exists(docs_path):
            return docs_path
    
    return None

def add_dates_to_html(
    build_dir: str,
    paths_to_skip: List[str],
    source_to_build_mapping: Dict[str, str],
    enabled: bool = True,
):
    """Add dates to HTML files."""
    if not enabled:
        print("Date info is disabled. Skipping.")
        return
    
    print(f"Adding dates to HTML files in {build_dir}")
    process_html_files(build_dir, paths_to_skip, source_to_build_mapping)
    print("Finished processing HTML files.")


def get_git_dates(file_path):
    """Get creation and last update dates for a file."""
    try:
        # Get last update date
        git_command = [
            "git", "log", "-1", "--date=format:%B %d, %Y", 
            "--format=%ad", "--", file_path
        ]
        last_updated = subprocess.check_output(git_command).decode().strip()
        
        # Get creation date
        git_command = [
            "git", "log", "--diff-filter=A", "--date=format:%B %d, %Y",
            "--format=%ad", "--", file_path
        ]
        created_on = subprocess.check_output(git_command).decode().strip()
        
        return created_on, last_updated
    except:
        return "Unknown", "Unknown"

def process_html_files(
    build_dir: str,
    paths_to_skip: List[str],
    source_to_build_mapping: Dict[str, str],
):
    print(f"Processing HTML files in {build_dir}")
    print(f"Source to build mapping: {source_to_build_mapping}")
    
    # Collect all HTML files and source files first
    html_files = []
    
    for build_subdir, source_subdir in source_to_build_mapping.items():
        build_path = os.path.join(build_dir, build_subdir)
        print(f"Checking build path: {build_path}")

        if not os.path.exists(build_path):
            print(f"Build path does not exist: {build_path}")
            continue

        for root, dirs, files in os.walk(build_path):
            # Skip directories in paths_to_skip
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith('_static') and not d.startswith('_images') and not any(
                    os.path.join(root, d).replace(build_dir + os.path.sep, "").rstrip("/") == skip_path.rstrip("/") or
                    os.path.join(root, d).replace(build_dir + os.path.sep, "").startswith(skip_path.rstrip("/") + "/")
                    for skip_path in paths_to_skip
                )
            ]

            for file in files:
                if not file.endswith(".html"):
                    continue

                html_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(html_file_path, build_dir)
                path_without_ext = os.path.splitext(rel_path)[0]

                if path_without_ext in paths_to_skip or any(
                    path_without_ext.startswith(skip_path)
                    for skip_path in paths_to_skip
                ):
                    continue

                source_file_path = find_source_file(path_without_ext)
                if source_file_path:
                    html_files.append((html_file_path, path_without_ext, source_file_path))
    
    # Process HTML files with the dates
    for html_file_path, path_without_ext, source_file_path in html_files:
        print(f"Processing HTML file: {html_file_path}")
        print(f"Relative path: {path_without_ext}")
        print(f"Found source file: {source_file_path}")
        
        created_on, last_updated = get_git_dates(source_file_path)
        print(f"Created on: {created_on}, Last updated: {last_updated}")
        
        try:
            # Add dates to HTML file
            with open(html_file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            # Check if date info already exists
            if soup.find("p", {"class": "date-info-last-verified"}):
                print(f"Date info already exists in {html_file_path}")
                continue
            
            h1_tag = soup.find("h1")
            if h1_tag:
                print("Found h1 tag, adding date info")
                date_info_tag = soup.new_tag("p", **{"class": "date-info-last-verified"})
                date_info_tag["style"] = "color: #6c6c6d; font-size: small;"
                date_info_tag.string = f"Created on: {created_on} | Last updated: {last_updated}"
                h1_tag.insert_after(date_info_tag)
                
                with open(html_file_path, "w", encoding="utf-8") as file:
                    file.write(str(soup))
                print("Updated HTML file with date info")
            else:
                print(f"Warning: No h1 tag found in {html_file_path}")
        except Exception as e:
            print(f"Error processing {html_file_path}: {e}")
