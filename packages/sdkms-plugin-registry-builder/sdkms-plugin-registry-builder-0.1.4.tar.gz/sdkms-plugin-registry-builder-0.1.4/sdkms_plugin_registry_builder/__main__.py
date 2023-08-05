#!/usr/bin/env python3
from git import Repo

import argparse
import json
import os

marketplace = {}

def parse_file_contents(file_name, file_contents):
    lines = file_contents.splitlines()
    name = lines[0].partition("Name:")[2].strip()
    if not name:
        print("Skipping file {}. Plugin should start with Name: <display_name>".format(file_name))
        return None, None, None

    version = lines[1].partition("Version:")[2].strip()
    if not version:
        print("Skipping file {}. Plugin should start with -- Version: <major>.<minor>".format(file_name))
        return None, None, None
    else:
        try:
            major = int(version.partition(".")[0])
            minor = int(version.partition(".")[2])
            if major < 0 or minor < 0:
                raise ValueError
        except ValueError:
            print("Skipping file {}. Plugin should start with -- Version: <major>.<minor>".format(file_name))
            return None, None, None

    description = lines[2].partition("Description:")[2].strip()

    if description:
        in_block = False
        for descr in file_contents.splitlines()[3:]:
            if descr.startswith("--[["):
                in_block = True
                continue
            if descr.startswith("]]--"):
                in_block = False
                continue

            if descr.startswith("--"):
                description += "\n"
                description += descr[2:].strip()
            elif in_block:
                description += "\n"
                description += descr
            else:
                break
    else:
        description = "Plugin description is not available"
    return (name, version, description)

def traverse_tree(repo, hexsha, tree):
   for blob in tree.blobs:
        if blob.path.endswith(".lua"):
            file_contents = repo.git.show('{}:{}'.format(hexsha, blob.path))
            name, version, description = parse_file_contents(blob.path, file_contents)
            if name:
                plugin = marketplace.get(name, {})
                plugin[version] = { "path": blob.path, "description": description, "commit": hexsha }
                marketplace[name] = plugin
        else:
            print("Skipping file {}. Plugins should have .lua extension".format(blob.path))
   for subtree in tree.trees:
       traverse_tree(repo, hexsha, subtree)


def main():
    parser = argparse.ArgumentParser(description=help, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--repo-dir", action="store",
                        default=".",
                        required=True,
                        help="Path to the plugin registry git repo")
    parser.add_argument("--commit-count", action="store",
                        default=1,
                        help="Number of commits from master to sign")
    parser.add_argument("--start-commit-id", action="store",
                        help="Commit hash from which the manifest should be built")
    parser.add_argument("--complete", action="store",
                        default=False,
                        help="Build registry since first commit")

    args = parser.parse_args()

    repo = Repo(args.repo_dir)
    assert not repo.bare


    # 1. Rebase and sign each commit
    with repo.git.custom_environment(EDITOR='true', GIT_SEQUENCE_EDITOR='true'):
        repo.git.rebase("--exec", "/usr/bin/git commit --amend --no-edit -n -S", "-i", "--root")

    # 2. Build the manifest
    for commit in repo.iter_commits('master', reverse=True):
        print("Scanning commit: {}".format(commit))
        traverse_tree(repo, commit.hexsha, commit.tree)

    manifest = []
    for (plugin_name, versions) in marketplace.items():
        plugin = {"name": plugin_name, "versions": versions}
        manifest.append(plugin)

    print("----- MANIFEST -----")
    print(json.dumps(manifest, indent=4))
    print("--------------------")

    # 3. Create manifest/commit
    filepath = os.path.join(args.repo_dir, 'manifest')
    f = open(filepath, "w")
    f.write(json.dumps(manifest, indent=4))
    f.close()

    repo.index.add([filepath])
    repo.git.commit("-S", "-m", "Added manifest")

if __name__ == '__main__':
    main()
