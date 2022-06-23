import os
import git
import logging
import multiprocessing
import pandas as pd
from datetime import datetime
from typing import *


def get_file_type(file_name):
    if file_name.endswith("pom.xml"):
        return "Maven"
    if file_name.endswith("build.gradle"):
        return "Gradle"
    if file_name.endswith("checkstyle.xml"):
        return "Checkstyle"
    return "Unknown"


def has_checkstyle(file_lines: List[str], file_type: str) -> bool:
    if file_type == "Maven":
        for line in file_lines:
            if "<artifactId>maven-checkstyle-plugin</artifactId>" in line:
                return True
    elif file_type == "Gradle":
        for line in file_lines:
            if "apply plugin: 'checkstyle'" in line:
                return True
    elif file_type == "Checkstyle":
        return True
    return False


def get_checkstyle_adoption(repo_dir: str, path: str) -> Tuple[str, datetime]:
    """Returns (commit SHA1, commit timestamp, has checkstyle)"""
    results = []
    repo = git.Repo(repo_dir, odbt=git.GitCmdObjectDB)
    lines = repo.git.log("--full-index", "-p", path).split("\n")
    commit_sha = None
    file_type = get_file_type(path)
    for line in lines:
        if line.startswith("commit "):
            commit_sha = line.split(" ")[1]
        elif line.startswith("+") and has_checkstyle([line], file_type):
            commit = repo.commit(commit_sha)
            results.append((
                commit_sha, 
                datetime.fromtimestamp(commit.committed_date)
            ))
    if len(results) > 0:
        return sorted(results, key=lambda x: x[1])[0]
    return None, None


def run(repo_name: str, repo_dir: str) -> dict:
    logging.info("Start analyzing %s", repo_name)
    results = []
    for root, subdirs, files in os.walk(repo_dir):
        for f in files:
            d = os.path.join(root, f)
            file_type = get_file_type(f)
            if file_type == "Unknown":
                continue
            
            result = { "repo_name": repo_name, "type": file_type, "path": os.path.relpath(d, repo_dir), 
                       "checkstyle": False, "adoption_commit": None, "adoption_time": None }

            with open(d, "r", encoding="utf-8", errors="ignore") as fd:
                lines = fd.readlines()
                result["checkstyle"] = has_checkstyle(lines, file_type)

            if result["checkstyle"]:
                commit, time = get_checkstyle_adoption(repo_dir, os.path.relpath(d, repo_dir))
                result["adoption_time"] = time
                result["adoption_commit"] = commit
            
            results.append(result)
    logging.info("Finish analyzing %s", repo_name)
    return results


REPO_BASEDIR1 = ""
REPO_BASEDIR2 = ""
REPO_DIRS = [(d, os.path.join(REPO_BASEDIR1, d)) for d in os.listdir(REPO_BASEDIR1)] + [(d, os.path.join(REPO_BASEDIR2, d)) for d in os.listdir(REPO_BASEDIR2)]
print(len(REPO_DIRS), "repos")


logging.basicConfig(level=logging.INFO)

with multiprocessing.Pool(16) as pool:
    results = sum(pool.starmap(run, REPO_DIRS), [])
    print(len(results), "dep config files")
    results = pd.DataFrame(results)
    print(len(set(results.repo_name)), "repos")
    print(len(set(results[results.checkstyle].repo_name)), "repos with checkstyle")
    results.to_csv("checkstyle_adoption.csv", index=False)
