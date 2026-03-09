import hashlib
import os
def compute_repo_hash(repo):
    m = hashlib.sha256()
    # Sort modules by module_id to ensure consistent hashing
    for module in sorted(repo.modules.values(), key=lambda m: m.module_id):
        content = module.abs_path.read_bytes()
        m.update(content)

    return m.hexdigest()

def save_repo_hash(repo, hash_file):
    repo_hash = compute_repo_hash(repo)
    with open(hash_file, "w") as f:
        f.write(repo_hash)

def check_repo_hash(repo, hash_file):
    if not os.path.exists(hash_file):
        return False

    with open(hash_file, "r") as f:
        saved_hash = f.read().strip()

    current_hash = compute_repo_hash(repo)

    return saved_hash == current_hash

