import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

interface ExampleOutput {
  name: string;
  exitCode: number;
  firstLine: string;
}

function runSlop(cwd: string, filePath: string): Promise<{ stdout: string; exitCode: number }> {
  return new Promise((resolvePromise) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", filePath], {
      cwd,
      env: process.env,
    });

    let stdout = "";
    let settled = false;

    const settle = (result: { stdout: string; exitCode: number }) => {
      if (settled) return;
      settled = true;
      resolvePromise(result);
    };

    child.stdout.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk;
    });

    child.stderr.resume();

    child.on("error", () => {
      settle({ stdout, exitCode: 1 });
    });

    child.on("close", (code, signal) => {
      settle({ stdout, exitCode: code ?? (signal ? 1 : 0) });
    });
  });
}

export default Plugin.define({
  id: "sloperator.example-outputs",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each file's name, exit code, and first line of stdout.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            examples: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  name: { type: "string" },
                  exitCode: { type: "integer" },
                  firstLine: { type: "string" },
                },
                required: ["name", "exitCode", "firstLine"],
                additionalProperties: false,
              },
            },
          },
          required: ["examples"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const cwd = ctx.location.project.directory;
          const names = (await readdir(join(cwd, "examples")))
            .filter((name) => name.endsWith(".slop"))
            .sort();

          const examples: ExampleOutput[] = await Promise.all(
            names.map(async (name) => {
              const result = await runSlop(cwd, join("examples", name));
              return {
                name,
                exitCode: result.exitCode,
                firstLine: result.stdout.split("\n")[0].replace(/\r$/, ""),
              };
            }),
          );

          return {
            content: JSON.stringify({ examples }),
            output: { examples },
          };
        },
      });
    });
  },
});
