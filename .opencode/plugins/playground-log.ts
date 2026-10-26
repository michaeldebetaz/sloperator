import { appendFile, mkdir } from "node:fs/promises"
import path from "node:path"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "playground-log",
  async setup(ctx) {
    const logFile = path.join(ctx.location.directory, "logs", "plugin-playground.log")

    await ctx.shell.hook("create.before", async (event) => {
      if (!event.command.includes("playground/server.py")) return

      await mkdir(path.dirname(logFile), { recursive: true })
      await appendFile(logFile, `${new Date().toISOString()} playground shell request: ${event.command}\n`)
    })
  },
})
