# The component socket

How OverPass finds, checks and installs its components, and what a Wine build has to offer for them. Written
for OverPass first; other apps and Wine builds can follow the same rules.

## 1. features.json: what a Wine build supports

An OverPass Wine release carries `share/overpass/features.json`:

```json
{
  "format": 1,
  "features": {
    "af-unix": { "version": 1, "summary": "AF_UNIX sockets in Winsock" },
    "dll-file-map": { "version": 1, "env": "WINE_DLL_FILE_MAP", "summary": "..." }
  }
}
```

- A feature's `version` goes up only when its behaviour or its switches change incompatibly.
- `env` names the environment variable that drives it, when there is one.
- A Wine build without the file is treated as having no features. OverPass still runs it, but components that
  need features are offered only on a build that lists them.

The current list lives in overpass-wine: `overpass/features.json`, with each patch described in
`overpass/PATCHES.md`.

### Giving another Wine the same features

Each feature is one or a few commits in [overpass-wine](https://github.com/McKack/overpass-wine), kept small so
they cherry-pick onto other Wine 11 trees. Copy the matching entries into your own `features.json` only for what
your build really has.

| Feature | Commits (overpass-wine) | Notes |
|---|---|---|
| `af-unix` | "Add support for AF_UNIX sockets" (Wine MR !7650) | Plain upstream Wine 11 |
| `winhttp-http2` | "libnghttp2: nghttp2 1.70.0 …", "winhttp: HTTP/2 through nghttp2 …", "winhttp: response decompression …", "libnghttp2: drop nghttp2's optional config.h includes …", "fix: asphalt legends http connect failure" | Adds the `libnghttp2` builtin DLL |
| `dll-file-map` | "ntdll: Support loading the main image from an inherited file descriptor." | |
| `gdk-winrt` | "fix: add mc gdk patchset", "fix: remove unused hr variable", "wine-appstate-registration", "wine-winhttp-gdk-options", "wine-mscoree-mono-path-bounds", "kernelbase: Add stub for GetIntegratedDisplaySize()." | |
| `dll-path-prepend`, `compat-rules`, `d3d9-backend-rule`, `no-mac-frame`, `max-resolution`, `services-elevated`, `rosetta-code-regions`, `game-mode-bundle`, `x87sidecar` | Patches 1–13 in `overpass/PATCHES.md` | Several build on CodeWeavers' LGPL changes |

## 2. Component manifests

Each folder in `components/` holds a `manifest.json` (plus README and licence notes where needed).
`scripts/build-catalog.py` checks them all and writes `catalog.json`, the one file OverPass downloads.

| Key | Meaning |
|---|---|
| `id` | Same as the folder name. Never changes once published |
| `name`, `plainName`, `summary` | Technical name, the name in OverPass's simple view, one line for people |
| `kind` | `wine`, `dlls` (loaded through the DLL path), `wine-addons`, `tool` (a program OverPass runs), `store` (a store client), `import` (the person brings it, e.g. from Apple's download) |
| `required`, `recommended`, `optIn` | How OverPass offers it. `optIn` components stay off until the person turns them on |
| `available` | `false` while nothing is published yet |
| `requires.wineFeatures` | `name` or `name>=version` from the installed Wine's `features.json` |
| `requires.arch` | Mac architectures it runs on (`arm64`, `x86_64`) |
| `install.location` | Folder under `~/Library/Application Support/OverPass/`. These match where OverPass 0.2.0 already installs, so nothing reinstalls when the catalog takes over |
| `install.executable` | The program inside that folder, for tools and stores |
| `parts` | What the component is made of, for credits and checks |

Each part has `name`, `version`, `authors`, `licence` (SPDX where there is one), `upstream` and `assets`. An asset
has an `arch` and either a pinned `url` with its `sha256`, or a `urlTemplate` that OverPass fills in (`{version}`,
`{arch}`) when the version comes from somewhere else: the installed Wine for Wine Mono and Gecko, the latest tag
for Winetricks. `format` is `tar.xz` (extracted into the location) or `file` (one executable).

## 3. How OverPass uses the catalog

1. It downloads `catalog.json` from this repository's default branch at start and when checking for updates,
   and keeps the last good copy.
2. Offline, or when the download fails or doesn't parse, it uses that copy, and failing that the versions built
   into the app.
3. A component is offered when its `requires` are met. An installed component whose catalog version differs
   from the installed one shows as an update.
4. Every pinned download is checked against its `sha256` before anything is replaced.

A catalog change reaches every OverPass user without an app release, so a version bump here is a release:
test it in OverPass first.
