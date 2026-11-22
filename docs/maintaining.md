# Maintaining

How versions, jars, changelogs and releases are kept consistent, and what goes on GitHub, Modrinth and CurseForge.

## Versioning

Semantic versioning. The version is `mod_version` in `gradle.properties` and nowhere else.

| Change | Next version |
| --- | --- |
| Bug fixes, performance work, internal cleanup | Patch, `1.2.0` to `1.2.1` |
| Anything players or pack makers can see that stays compatible, including a new loader or Minecraft version | Minor, `1.2.0` to `1.3.0` |
| Anything that breaks worlds, configs or mods depending on this one, including dropping a loader or Minecraft version | Major, `1.2.0` to `2.0.0` |

Every release rebuilds every jar under the same version.

## Jar names

`RoundTreesCompanion-<version>-<loaders>-<minecraft>.jar`

| Part | Rule |
| --- | --- |
| `<version>` | `mod_version`, without a `v` |
| `<loaders>` | The loaders the jar is built for, lower case, joined with `-`: `fabric`, `neoforge`, `forge`, `fabric-neoforge` |
| `<minecraft>` | Lowest and highest supported version joined with `-`, or the one version if there is only one |

A loader that only runs a jar built for another one is not part of the name: Quilt runs the Fabric jars and NeoForge 1.20.1 runs the Forge jar. Those loaders are ticked on the sites instead.

The folder in `versions/` is named `<loaders>-<minecraft>` and the jar takes its name from it.

## Changelog and commits

[`CHANGELOG.md`](../CHANGELOG.md) has one `## <version>` section per release, newest first, with one plain bullet per change, written for players.

Every commit has a short subject that starts with a verb and says what changed, and a body of plain bullets. A release commit has the bullets of its changelog section as its body.

A release is marked by its tag, `v<version>`, not by its commit subject. Releases on GitHub are immutable and their tags can't be moved, so `main` is never rewritten once a release is tagged.

## Adding a Minecraft version

The mod hooks three pieces of game code, named here as in Mojang's mappings.

| Hook | Source folder | History |
| --- | --- | --- |
| `BlockBehaviour.BlockStateBase.getOffset` and `hasOffsetFunction` | `src/offset-*` | `hasOffsetFunction` exists since 1.19.4, `getOffset` lost its level parameter in 1.21.2 |
| The `hasOffsetFunction` check in the constructor of `BlockStateBase.Cache` | `src/main` | Unchanged since 1.19.4 |
| The sign renderer | `src/sign-*` | `SignRenderer.render` up to 1.21.3, `AbstractSignRenderer.renderSignWithText` for 1.21.4 - 1.21.8, `AbstractSignRenderer.submit` since 1.21.9, the sign board is a block model since 26.2 |

An existing jar covers a new version when all three still have the same names and parameters there. Before 26.1 the Fabric intermediary names have to match as well, since 26.1 the game is not obfuscated and one jar serves Fabric and NeoForge. Covering it then only means raising the upper bound: the range in that folder's `gradle.properties` and the folder name.

When a hook changed, the new version gets its own folder in `versions/` with a `gradle.properties`, and the changed hook gets a new `src/offset-<version>` or `src/sign-<version>` folder. Source folders are named after the first version they apply to. The list of mixins in the jar is generated from the folders named in `sources`.

A supported version is written down in these places, and all of them change together:

| Place | What |
| --- | --- |
| `versions/<loaders>-<minecraft>/` | The folder name and the range in its `gradle.properties` |
| [`tests/cases.txt`](../tests/cases.txt) | The lowest and highest version of the jar |
| [`README.md`](../README.md) | The Downloads table |
| [`description.md`](description.md) | The list under "Which file do I need?" |
| This file | The Files table under Releases |
| [`CHANGELOG.md`](../CHANGELOG.md) | A line for the added version |

## Pre-release checks

`./gradlew build` builds every jar into `dist/`. [`tests/launchtest.py`](../tests/launchtest.py) then runs every case in [`tests/cases.txt`](../tests/cases.txt): the lowest and highest version of each jar, the highest also next to Sodium, Lithium, FerriteCore, ModernFix and Iris, or Embeddium, Oculus and Canary on Forge.

A case installs the loader, starts a dedicated server with the jar, joins the world it made on a client with and without the jar and compares the screenshots. It passes when the server starts, both clients get into the world, the mod's hooks are applied and the ladders, signs and torches on logs have moved. The screenshots are kept in `run/shots/`.

It runs on Linux with Xvfb, xdotool, ImageMagick and JDK 17, 21 and 25. Software rendering is enough.

| Known trap | Handled by |
| --- | --- |
| The newest Sodium and Iris for a version sometimes refuse to load together | Iris is left out of those cases |
| ModernFix on Forge 1.18.2 opens a warning screen that swallows the menu clicks | ModernFix is left out of that case |
| Forge 1.18 and 1.19 don't draw signs when the camera looks exactly along an axis, with or without the mod | The test world holds the camera slightly off-axis |
| 26.3 can't open an OpenGL window on a virtual display | A Vulkan driver such as lavapipe |
| NeoForge's loading window can't be created on a virtual display | The test turns it off |

Not covered by the script, and checked by hand on a real machine with a round tree pack: a large modpack on each loader, and 26.3 on a real GPU.

| Check | Expected |
| --- | --- |
| Wall sign, ladder, wall torch, soul wall torch and redstone wall torch on the side of an upright log | Each sits slightly off the bark, nothing clips |
| The same blocks on stone | Unchanged |
| A sign on the flat end of a sideways log | Unchanged |
| Sign text | On the board, not floating in front of it or hidden behind it |
| Breaking a ladder on a log | The crack overlay lines up with the ladder |
| `logs/latest.log` | No error mentioning `roundtreescompanion` |

## Upkeep

Things that go stale or break without anything in the mod changing.

| What | Where | Needs attention when |
| --- | --- | --- |
| The three hooks into the game | `src/offset-*`, `src/sign-*`, `src/main` | A Minecraft release changes one of them, see Adding a Minecraft version |
| Versions of Fabric Loom, ModDevGradle and Gradle | `build.gradle`, `gradle/wrapper` | A new Minecraft version needs newer ones. Loom also decides which JDK Gradle has to run on |
| The Forge, NeoForge and Fabric Loader versions the jars are compiled against | `versions/*/gradle.properties`, `gradle.properties` | Rarely, an old one disappears from its repository |
| Loader versions in the test cases | `tests/cases.txt` | A new Minecraft version is added, or an installer for an old one stops working |
| Mods the tests run next to | `tests/cases.txt` | Two of them stop loading together, or one drops a version |
| The supported versions, written down in six places | The table in Adding a Minecraft version | A jar's range changes. This is the easiest thing to let drift |
| What the test script expects from the game: profile and installer formats, the log lines it waits for, console commands, the menu positions it clicks before 1.20, the parts of the screenshot it compares | `tests/launcher.py`, `tests/launchtest.py` | A case fails with and without the mod. Each new Minecraft version can break one of these |
| Category names | [`topics.md`](topics.md) | A site renames or removes a category |

## Listings

| Text | File | Used for |
| --- | --- | --- |
| Summary | [`summary.md`](summary.md) | The GitHub About line and the summary field on Modrinth and CurseForge |
| Topics and tags | [`topics.md`](topics.md) | The GitHub topics and the categories on Modrinth and CurseForge |
| Description | [`description.md`](description.md) | The description on Modrinth and CurseForge |

## Releases

`<version>` is `mod_version` in `gradle.properties`, without a `v`. Every jar in `dist/` is uploaded to all three sites with the same changelog, the section for that version in [`CHANGELOG.md`](../CHANGELOG.md) without its heading.

### GitHub

| Field | Value |
| --- | --- |
| Tag | `v<version>`, on `main` |
| Title | `<version>` |
| Notes | The changelog section |
| Files | Every jar |
| Label | Latest |

### Modrinth

Loaders and game versions are detected from the jar. Quilt is never detected, and neither is NeoForge on the Forge file.

| Field | Value |
| --- | --- |
| Loaders, game versions | From the table under Files |
| Environment | Client-side only |
| Dependencies | None |
| Version type | Release |
| Version number | `<version>-<file>` |
| Version subtitle | The label |
| Version changelog | The changelog section |

### CurseForge

| Field | Value |
| --- | --- |
| Display name | `<version> (<label>)` |
| Environment | Client |
| Mod loaders, Java version, Minecraft versions | From the table under Files |
| Release type | Release |
| Changelog | The changelog section, as Markdown |
| Related projects | None |

### Files

`<file>` is the jar's name without `RoundTreesCompanion-<version>-` and `.jar`. NeoForge on the Forge file is for 1.20.1 only, NeoForge doesn't exist for anything older.

| File | Label | Loaders | Game versions | Java |
| --- | --- | --- | --- | --- |
| `fabric-neoforge-26.1-26.3` | Fabric, NeoForge 26.1 - 26.3 | Fabric, Quilt, NeoForge | 26.1, 26.1.1, 26.1.2, 26.2, 26.3 | 25 |
| `fabric-1.21.9-1.21.11` | Fabric 1.21.9 - 1.21.11 | Fabric, Quilt | 1.21.9, 1.21.10, 1.21.11 | 21 |
| `fabric-1.21.4-1.21.8` | Fabric 1.21.4 - 1.21.8 | Fabric, Quilt | 1.21.4, 1.21.5, 1.21.6, 1.21.7, 1.21.8 | 21 |
| `fabric-1.21.2-1.21.3` | Fabric 1.21.2 - 1.21.3 | Fabric, Quilt | 1.21.2, 1.21.3 | 21 |
| `fabric-1.18.2-1.21.1` | Fabric 1.18.2 - 1.21.1 | Fabric, Quilt | 1.18.2, 1.19, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.20, 1.20.1, 1.20.2, 1.20.3, 1.20.4, 1.20.5, 1.20.6, 1.21, 1.21.1 | 17, 21 |
| `neoforge-1.21-1.21.1` | NeoForge 1.21 - 1.21.1 | NeoForge | 1.21, 1.21.1 | 21 |
| `forge-1.18.2-1.20.1` | Forge 1.18.2 - 1.20.1 | Forge, NeoForge | 1.18.2, 1.19, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.20, 1.20.1 | 17 |
