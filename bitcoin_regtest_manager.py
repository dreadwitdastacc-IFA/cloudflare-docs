import shutil
import subprocess
from pathlib import Path
from typing import Optional

DOCKER_COMPOSE_FILE = Path("docker-compose.bitcoin-regtest.yml")


class BitcoinRegtestManager:
    def __init__(self, compose_file: Optional[Path] = None):
        self.compose_file = compose_file or DOCKER_COMPOSE_FILE

    @staticmethod
    def _which(executable: str) -> Optional[str]:
        return shutil.which(executable) or shutil.which(f"{executable}.exe")

    @classmethod
    def docker_available(cls) -> bool:
        return bool(cls._which("docker-compose") or cls._which("docker"))

    def compose_command(self, *args: str) -> list[str]:
        compose_bin = self._which("docker-compose")
        if compose_bin:
            return [compose_bin, "-f", str(self.compose_file), *args]

        docker_bin = self._which("docker")
        if docker_bin:
            return [docker_bin, "compose", "-f", str(self.compose_file), *args]

        raise RuntimeError("Docker CLI is not installed or not available in PATH.")

    def _run_compose(self, *args: str) -> str:
        if not self.compose_file.exists():
            raise FileNotFoundError(f"Compose file not found: {self.compose_file}")

        command = self.compose_command(*args)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed: {' '.join(command)}\n"
                f"stdout: {result.stdout.strip()}\n"
                f"stderr: {result.stderr.strip()}"
            )

        return result.stdout.strip()

    def start_cluster(self) -> bool:
        if not self.docker_available():
            raise RuntimeError("Docker is not installed or not available in PATH.")
        self._run_compose("up", "-d")
        return True

    def stop_cluster(self) -> bool:
        if not self.docker_available():
            raise RuntimeError("Docker is not installed or not available in PATH.")
        self._run_compose("down")
        return True

    def status_cluster(self) -> str:
        if not self.docker_available():
            return "Docker unavailable"
        try:
            return self._run_compose("ps")
        except RuntimeError as exc:
            return str(exc)


if __name__ == "__main__":
    manager = BitcoinRegtestManager()
    print("Bitcoin regtest compose file:", manager.compose_file)
    if not manager.compose_file.exists():
        raise FileNotFoundError(f"Missing {manager.compose_file}")
    print(manager.status_cluster())
