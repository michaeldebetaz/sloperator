import { appendFile, mkdir } from "node:fs/promises"
import path from "node:path"
import { Plugin } from "@opencode/plugin"

const editTools = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "edit-log",
  async setup(ctx) {
    const logFile = path.join(ctx.location.directory, "logs", "plugin-tools.log")

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return
      if (!editTools.has(event.tool)) return

      await mkdir(path.dirname(logFile), { recursive: true })
      await appendFile(logFile, `${JSON.stringify({ tool: event.tool, status: "completed" })}\n`)
    })
  },
})
