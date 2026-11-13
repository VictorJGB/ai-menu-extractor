import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const python = fileURLToPath(
  new URL(
    process.platform === "win32"
      ? "../.venv/Scripts/python.exe"
      : "../.venv/bin/python",
    import.meta.url,
  ),
);

if (!existsSync(python)) {
  console.error(
    "Python environment missing. Run: python -m venv .venv, then install requirements.txt with that environment's Python.",
  );
  process.exit(1);
}

const backend = spawn(
  python,
  ["-m", "uvicorn", "backend.app:app", "--reload", "--reload-dir", "backend", "--host", "127.0.0.1", "--port", "8000"],
  { cwd: root, stdio: "inherit" },
);

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => backend.kill(signal));
}

backend.on("error", (error) => {
  console.error(`Could not start the backend: ${error.message}`);
  process.exitCode = 1;
});

backend.on("exit", (code, signal) => {
  process.exitCode = code ?? (signal ? 1 : 0);
});
