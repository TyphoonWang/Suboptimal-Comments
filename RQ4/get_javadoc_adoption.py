import os
import git
import logging
import multiprocessing
import pandas as pd
import subprocess
from datetime import datetime
from typing import *


def get_file_type(file_name):
    if file_name.endswith("pom.xml"):
        return "Maven"
    if file_name.endswith("build.gradle"):
        return "Gradle"
    return "Unknown"


def has_javadoc(file_lines: List[str], file_type: str) -> bool:
    if file_type == "Maven":
        for line in file_lines:
            if "<artifactId>maven-javadoc-plugin</artifactId>" in line:
                return True
    if file_type == "Gradle":
        for line in file_lines:
            if "apply plugin: 'java'" in line or "apply plugin: 'javadoc'" in line or "id: 'javadoc'" in line:
                return True
    return False


def is_warning_disabled(file_lines: List[str], file_type: str) -> bool:
    for line in file_lines:
        if "-Xdoclint:none" in line or "<doclint>none</doclint>" in line:
            return True
    return False


def get_javadoc_adoption(repo_dir: str, path: str) -> Tuple[str, datetime]:
    """Returns (commit SHA1, commit timestamp)"""
    results = []
    repo = git.Repo(repo_dir, odbt=git.GitCmdObjectDB)
    lines = repo.git.log("--full-index", "-p", path).split("\n")
    commit_sha = None
    file_type = get_file_type(path)
    for line in lines:
        if line.startswith("commit "):
            commit_sha = line.split(" ")[1]
        elif line.startswith("+") and has_javadoc([line], file_type):
            commit = repo.commit(commit_sha)
            results.append((
                commit_sha, 
                datetime.fromtimestamp(commit.committed_date)
            ))
    if len(results) > 0:
        return sorted(results, key=lambda x: x[1])[0]
    return None, None


def get_javadoc_adoption2(repo_dir) -> Tuple[str, datetime]:
    """Returns (commit SHA1, commit timestamp)"""
    results = []
    repo = git.Repo(repo_dir, odbt=git.GitCmdObjectDB)
    os.chdir(repo_dir)
    l1 = subprocess.run("git log -G maven-javadoc-plugin | grep ^commit", stdout=subprocess.PIPE, shell=True).stdout
    l2 = subprocess.run("git log -G \"apply plugin: 'javadoc'\" | grep ^commit", stdout=subprocess.PIPE, shell=True).stdout
    l3 = subprocess.run("git log -G \"id: 'javadoc'\" | grep ^commit", stdout=subprocess.PIPE, shell=True).stdout
    for line in l1.split(b"\n") + l2.split(b"\n") + l3.split(b"\n"):
        line = line.decode(encoding="utf-8", errors="ignore")
        logging.info(line)
        if line.startswith("commit "):
            commit_sha = line.split(" ")[1]
            results.append((commit_sha, datetime.fromtimestamp(repo.commit(commit_sha).committed_date)))
    if len(results) > 0:
        return sorted(results, key=lambda x: x[1])[0]
    return None, None


def run(repo_name: str, repo_dir: str) -> dict:
    logging.info("Start analyzing %s", repo_name)
    results = []
    if not os.path.isdir(repo_dir):
        return []
    for root, subdirs, files in os.walk(repo_dir):
        for f in files:
            d = os.path.join(root, f)
            file_type = get_file_type(f)
            if file_type == "Unknown":
                continue
            
            result = { "repo_name": repo_name, "type": file_type, "path": os.path.relpath(d, repo_dir), 
                       "javadoc": False, "adoption_commit": None, "adoption_time": None, "warning_disabled": False }

            with open(d, "r", encoding="utf-8", errors="ignore") as fd:
                lines = fd.readlines()
                result["javadoc"] = has_javadoc(lines, file_type)
                result["warning_disabled"] = is_warning_disabled(lines, file_type)

            if result["javadoc"]:
                commit, time = get_javadoc_adoption(repo_dir, os.path.relpath(d, repo_dir))
                result["adoption_time"] = time
                result["adoption_commit"] = commit
            
            results.append(result)
    result = { "repo_name": repo_name, "type": "gitlog", "path":None,
                "javadoc": False, "adoption_commit": None, "adoption_time": None, "warning_disabled": False }
    commit, time = get_javadoc_adoption2(repo_dir)
    result["adoption_time"] = time
    result["adoption_commit"] = commit
    if commit is not None:
        result["javadoc"] = True
    results.append(result)
    logging.info("Finish analyzing %s", repo_name)
    return results


REPO_BASEDIR1 = ""
REPO_BASEDIR2 = ""
REPO_DIRS = [(d, os.path.join(REPO_BASEDIR1, d)) for d in os.listdir(REPO_BASEDIR1)] + [(d, os.path.join(REPO_BASEDIR2, d)) for d in os.listdir(REPO_BASEDIR2)]
print(len(REPO_DIRS), "repos")

logging.basicConfig(level=logging.INFO)

with multiprocessing.Pool(48) as pool:
    results = sum(pool.starmap(run, REPO_DIRS), [])
    print(len(results), "dep config files")
    results = pd.DataFrame(results)
    print(len(set(results.repo_name)), "repos")
    print(len(set(results[results.javadoc].repo_name)), "repos with javadoc")
    results.to_csv("javadoc_adoption.csv", index=False)