#!/usr/bin/env node

import fs from "node:fs";

const targetVersion = process.argv[2];
if (!/^\d+\.\d+\.\d+$/.test(targetVersion ?? "")) {
  throw new Error("Usage: update-codex-cli.mjs <stable-semver>");
}

const dockerfilePath = "codex-cli/Dockerfile";
const configPath = "codex-cli/config.yaml";
const readmePath = "README.md";
const changelogPath = "codex-cli/CHANGELOG.md";

const dockerfile = fs.readFileSync(dockerfilePath, "utf8");
const currentMatch = dockerfile.match(/^ARG CODEX_VERSION=(\d+\.\d+\.\d+)$/m);
if (!currentMatch) {
  throw new Error("Could not find the pinned CODEX_VERSION in the Dockerfile");
}

const currentVersion = currentMatch[1];
if (currentVersion === targetVersion) {
  console.log(`Codex CLI is already pinned to ${targetVersion}.`);
  process.exit(0);
}

const currentParts = currentVersion.split(".").map(Number);
const targetParts = targetVersion.split(".").map(Number);
const firstDifferentPart = targetParts.findIndex(
  (part, index) => part !== currentParts[index],
);
if (targetParts[firstDifferentPart] < currentParts[firstDifferentPart]) {
  throw new Error(`Refusing to downgrade Codex CLI from ${currentVersion} to ${targetVersion}`);
}

fs.writeFileSync(
  dockerfilePath,
  dockerfile.replace(
    /^ARG CODEX_VERSION=\d+\.\d+\.\d+$/m,
    `ARG CODEX_VERSION=${targetVersion}`,
  ),
);

const config = fs.readFileSync(configPath, "utf8");
const appVersionMatch = config.match(/^version: "(\d+)\.(\d+)\.(\d+)"$/m);
if (!appVersionMatch) {
  throw new Error("Could not find the Home Assistant app version");
}

const appVersion = [
  appVersionMatch[1],
  appVersionMatch[2],
  String(Number(appVersionMatch[3]) + 1),
].join(".");
fs.writeFileSync(
  configPath,
  config.replace(/^version: "\d+\.\d+\.\d+"$/m, `version: "${appVersion}"`),
);

const readme = fs.readFileSync(readmePath, "utf8");
const readmeLines = readme.split("\n");
const appRow = readmeLines.findIndex((line) => line.startsWith("| [Codex CLI](codex-cli) |"));
if (appRow === -1) {
  throw new Error("Could not find the Codex CLI row in README.md");
}
readmeLines[appRow] = readmeLines[appRow].replace(/`\d+\.\d+\.\d+` \|$/, `\`${appVersion}\` |`);
fs.writeFileSync(readmePath, readmeLines.join("\n"));

const changelog = fs.readFileSync(changelogPath, "utf8");
const heading = "# Changelog\n\n";
if (!changelog.startsWith(heading)) {
  throw new Error("Unexpected changelog header");
}
const entry = [
  `## ${appVersion}`,
  "",
  `- Updates OpenAI Codex CLI from \`${currentVersion}\` to \`${targetVersion}\`.`,
  "",
].join("\n");
fs.writeFileSync(changelogPath, heading + entry + changelog.slice(heading.length));

console.log(JSON.stringify({ currentVersion, targetVersion, appVersion }, null, 2));
