#!/usr/bin/env python3
from git import Repo, InvalidGitRepositoryError
from git.exc import GitCommandError
from json import JSONDecodeError

import argparse
import json
import os
import warnings

marketplace = {}

metadata_structure = {
    'name': str,
    'version': float,
    'thumbnail': str,
    'release_notes': [
        str
    ]
}

def check_structure(struct, conf):
    if isinstance(struct, dict) and isinstance(conf, dict):
        # struct is a dict of types or other dicts
        return all(k in conf and check_structure(struct[k], conf[k]) for k in struct)
    if isinstance(struct, list) and isinstance(conf, list):
        # struct is list in the form [type or dict]
        return all(check_structure(struct[0], c) for c in conf)
    elif isinstance(struct, type):
        # struct is the type of conf
        return isinstance(conf, struct)
    else:
        # struct is neither a dict, nor list, not type
        return False

def traverse_tree(repo, hexsha, tree):
   for blob in tree.blobs:
        if blob.path.endswith(".lua"):
            file_contents = repo.git.show('{}:{}'.format(hexsha, blob.path))
            readme = os.path.dirname(blob.path) + "/README.md"
            metadata_path = os.path.dirname(blob.path) + "/metadata.json"

            try:
                description = repo.git.show('{}:{}'.format(hexsha, readme))
            except:
                description = "Plugin description is not available"

            try:
                metadata = json.loads(repo.git.show('{}:{}'.format(hexsha, metadata_path)))
            except GitCommandError as e:
                if e.status == 128: # Metadata not found
                    warnings.warn("metadata.json not found when looking at " + str(blob.path) + ". Skipping...")
                    continue
            except JSONDecodeError:
                raise Exception

            if not check_structure(metadata_structure, metadata):
                raise Exception("Invalid metadata.json for plugin " + blob.path)

            name = metadata["name"]
            plugin = marketplace.get(name, {})
            plugin_data = {
                "path": blob.path, \
                "description": description, \
                "thumbnail": metadata["thumbnail"], \
                "release_notes": metadata["release_notes"], \
                "commit": hexsha
            }

            license_path = os.path.dirname(blob.path) + "/LICENSE"
            try:
                plugin_data["license"] = repo.git.show('{}:{}'.format(hexsha, license_path))
            except:
                pass # if no license file the MPL shall be used

            plugin[metadata["version"]] = plugin_data
            marketplace[name] = plugin

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

    try:
        repo = Repo(args.repo_dir)
    except InvalidGitRepositoryError as e:
        print("Invalid git repo. Error: " + str(e))
        exit(1)

    assert not repo.bare

    # 1. Rebase and sign each commit
    with repo.git.custom_environment(EDITOR='true', GIT_SEQUENCE_EDITOR='true'):
        repo.git.rebase("--exec", "/usr/bin/git commit --amend --no-edit -n -S", "-i", "--root")

    # 2. Build the manifest
    for commit in repo.iter_commits('master', reverse=True):
        print("Scanning commit: {}".format(commit))
        traverse_tree(repo, commit.hexsha, commit.tree)

    manifest = {}

    with open(args.repo_dir + "/LICENSE", 'r') as f:
        manifest["license"] = f.read()

    manifest["plugins"] = []
    for (plugin_name, versions) in marketplace.items():
        plugin = {"name": plugin_name, "versions": versions}
        manifest["plugins"].append(plugin)

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
