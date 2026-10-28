# OverPass components

The parts [OverPass](https://github.com/McKack/overpass) installs besides itself: what they are, where they come
from, which versions OverPass uses and under which licences.

| Component | In OverPass | Upstream |
|---|---|---|
| [overpass-wine](components/wine) | Windows support (required) | [McKack/overpass-wine](https://github.com/McKack/overpass-wine) |
| [overpass-runtime](components/runtime) | Game graphics | [McKack/overpass-runtime](https://github.com/McKack/overpass-runtime) |
| [Wine Mono & Gecko](components/dotnet-web) | .NET and web pages | [Wine Mono](https://gitlab.winehq.org/wine-mono/wine-mono), Wine Gecko |
| [Winetricks](components/winetricks) | Extra Windows parts | [Winetricks/winetricks](https://github.com/Winetricks/winetricks) |
| [D3DMetal](components/d3dmetal) | Apple's game graphics (imported by you) | [Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/) |
| [x87sidecar](components/x87sidecar) | Faster older games | [athei/x87sidecar](https://github.com/athei/x87sidecar) |
| [Legendary](components/epic) | Epic Games Library | [legendary-gl/legendary](https://github.com/legendary-gl/legendary) |
| [gogdl](components/gog) | GOG Library | [Heroic-Games-Launcher/heroic-gogdl](https://github.com/Heroic-Games-Launcher/heroic-gogdl) |
| [Xodus](components/xbox) | Xbox Library (opt-in, not published yet) | [xodus-gaming/xodus](https://github.com/xodus-gaming/xodus) |

`catalog.json` is generated from the manifests by `scripts/build-catalog.py`; OverPass reads it, so a component
update doesn't need a new OverPass release. [SOCKET.md](SOCKET.md) describes the manifest format and the
`features.json` file a Wine build uses to say what it supports, for anyone who wants to build components or a
Wine that works with them.

## Licence

The manifests, catalog and scripts here are MIT licensed (see `LICENSE`). Each component keeps its own licence,
listed in its manifest; nothing here relicenses them.
