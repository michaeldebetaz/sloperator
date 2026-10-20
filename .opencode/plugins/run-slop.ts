import { spawn } from "node:child_process";
import { isAbsolute, resolve } from "node:path";
import { Plugin } from "@opencode/plugin";

interface RunSlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSlop(cwd: string, filePath: string): Promise<RunSlopResult> {
  const absolutePath = isAbsolute(filePath) ? filePath : resolve(cwd, filePath);

  return new Promise((resolvePromise) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", absolutePath], {
      cwd,
      env: process.env,
    });

    let stdout = "";
    let stderr = "";
    let settled = false;

    const settle = (result: RunSlopResult) => {
      if (settled) return;
      settled = true;
      resolvePromise(result);
    };

    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");

    child.stdout.on("data", (chunk: string) => {
      stdout += chunk;
    });

    child.stderr.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", (error) => {
      settle({ stdout, stderr: stderr + error.message, exitCode: 1 });
    });

    child.on("close", (code, signal) => {
      settle({
        stdout,
        stderr,
        exitCode: code ?? (signal ? 1 : 0),
      });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) program with Sloperator. Returns stdout, stderr, and exitCode as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file to run, relative to the project root or absolute.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            stdout: { type: "string" },
            stderr: { type: "string" },
            exitCode: { type: "integer" },
          },
          required: ["stdout", "stderr", "exitCode"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSlop(ctx.location.project.directory, path);

          return {
            content: JSON.stringify(result),
            output: result,
          };
        },
      });
    });
  },
});
