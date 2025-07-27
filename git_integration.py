import git
from pathlib import Path
import logging

class GitVCS:
    """Handles version control operations for scene files."""
    def __init__(self, repo_path='.'):
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
            logging.info(f"Git repository found at: {self.repo.working_dir}")
        except git.InvalidGitRepositoryError:
            logging.warning("Not a Git repository. VCS features will be disabled.")
            self.repo = None

    def commit_and_push(self, file_path, message):
        """
        Adds a file to staging, commits it, and pushes to the remote.
        Assumes Git LFS is configured for .blend files.
        """
        if not self.repo:
            return

        full_path = Path(file_path).resolve()
        self.repo.index.add([str(full_path)])
        self.repo.index.commit(message)
        logging.info(f"Committed '{full_path}' with message: '{message}'")
        # For simplicity, push is commented out. Uncomment if auto-push is desired.
        # self.repo.remotes.origin.push()