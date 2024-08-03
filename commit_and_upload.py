import subprocess

def commit_and_upload(SYNC_SOURCE, SYNC_GH_URL):

    if subprocess.run(["git", "add", "-A"], cwd=SYNC_SOURCE).returncode != 0:
        print("git add returned a nonzero return code")
        print("Stopping Sync")
        exit(1)

    diff = subprocess.run(["git", "diff", "HEAD", "--name-only"], cwd=SYNC_SOURCE, capture_output=True)

    if diff.returncode != 0:
        print("git diff returned a nonzero return code")
        print("Stopping Sync")
        exit(diff.returncode)

    diff_contains_filename = False

    for b in diff.stdout:
        if b > 32:
            diff_contains_filename = True
            break

    if not diff_contains_filename:
        print("No changes detected")
        print("Stopping Sync")
        exit(0)

    most_recent_commit = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd="source", capture_output=True)

    if most_recent_commit.returncode != 0:
        print("git log -1 returned nonzero return code")
        print("Stopping Sync")
        exit(most_recent_commit.returncode)

    commit_message_bytes = list(most_recent_commit.stdout)

    while len(commit_message_bytes) > 0 and commit_message_bytes[-1] <= 32:
        commit_message_bytes.pop()

    try:
        commit_message_string = bytes(commit_message_bytes).decode('UTF-8')
    except:
        print("Most recent commit message is not valid UTF-8")
        print(f"Commit message bytes: {commit_message_bytes}")
        print("Stopping Sync")
        exit(1)

    if subprocess.run(["git", "commit", "-m", commit_message_string], cwd=SYNC_SOURCE).returncode != 0:
        print("git commit returned a nonzero return code")
        print("Stopping Sync")
        exit(1)

    if subprocess.run(["git", "push", SYNC_GH_URL, "main"], cwd=SYNC_SOURCE).returncode != 0:
        print("git push returned a nonzero return code")
        print("Stopping Sync")
        exit(1)