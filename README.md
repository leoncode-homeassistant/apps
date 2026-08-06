# LeonCode Home Assistant Apps

[![Lint](https://github.com/leoncode-homeassistant/apps/actions/workflows/lint.yaml/badge.svg)](https://github.com/leoncode-homeassistant/apps/actions/workflows/lint.yaml)
[![Builder](https://github.com/leoncode-homeassistant/apps/actions/workflows/builder.yaml/badge.svg)](https://github.com/leoncode-homeassistant/apps/actions/workflows/builder.yaml)
[![License](https://img.shields.io/github/license/leoncode-homeassistant/apps)](LICENSE)

A curated collection of Home Assistant apps maintained by
**LeonCode**. Each app lives in its own directory, has an
independent version and changelog, and is published as a multi-architecture
container image.

## Available apps

| App | Description | Architectures | Version |
| --- | --- | --- | --- |
| [Codex CLI](codex-cli) | Run OpenAI Codex CLI as a secure SSH-accessible workspace on Home Assistant OS. | `amd64`, `aarch64` | `0.3.0` |

## Add this repository to Home Assistant

[![Open your Home Assistant instance and add the LeonCode app repository.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fleoncode-homeassistant%2Fapps)

Click the button above to open your Home Assistant instance with this app
repository pre-filled. If the redirect is unavailable, add it manually:

1. Open **Settings → Apps → App store** in Home Assistant.
2. Open the menu in the top-right corner and select **Repositories**.
3. Add this URL:

   ```text
   https://github.com/leoncode-homeassistant/apps
   ```
4. Reload the app store.
5. Select and install the app you want.

Home Assistant tracks each app version independently. Updates appear in the
normal app update flow after a new version has been published.

## Repository structure

```text
apps/
├── repository.yaml
├── codex-cli/
│   ├── config.yaml
│   ├── Dockerfile
│   ├── DOCS.md
│   ├── CHANGELOG.md
│   └── rootfs/
└── another-app/
    └── ...
```

The GitHub Actions workflows discover app directories automatically. Pull
requests are linted and built without publishing images. Changes merged into
`main` publish versioned `amd64` and `aarch64` images to the GitHub Container
Registry.

## Security

These apps can interact with sensitive Home Assistant data and services.
Review an app's documentation and requested permissions before installation,
keep recovery backups, and never expose management ports directly to the
public internet.

## License

This repository is licensed under the [Apache License 2.0](LICENSE). Third-party
software installed or referenced by an app remains subject to its respective
license and terms.
