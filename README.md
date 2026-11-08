# Luso-FrEnglish (PT-FR-EN)

US ANSI keyboard layout with AltGr dead keys, tuned for Portuguese, French and English.

- Base layout: QWERTY (US basic).
- Right Alt = AltGr (level 3). Shift + AltGr = level 4.
- Name shown in pickers: "English (Luso-FrEnglish, AltGr dead keys)" (short: PT-FR-EN).
- Localized names: "Luso-Franglês" (Portuguese), "Luso-Franglais" (French).

## What differs from `us(altgr-intl)`

| Area | `us(altgr-intl)` | Luso-FrEnglish |
|---|---|---|
| Nordic letters | Keeps å, ø, æ on AltGr | Removes å and ø; keeps æ/œ for French |
| Rare letters | Keeps þ, ð style symbols | Replaced with PT/FR useful ones (º/ª, ™/®) |
| Direct accents | Mixed, some mnemonic | Consistent vowel/letter accent map (see tables) |
| Dead keys | Same core set | Same core set, cedilla/ogonek on comma |
| Scope | Generic Western EU | Focused on PT + FR + EN |

## Dead keys (AltGr)

| Key | Dead key | Use for |
|---|---|---|
| ` (TLDE) | dead_grave | à, è, ì, ò, ù |
| ` (TLDE) + Shift | dead_tilde | ã, õ, ñ |
| 6 (AE06) | dead_circumflex | â, ê, î, ô, û |
| ' (AC11) | dead_acute | á, é, í, ó, ú |
| ' (AC11) + Shift | dead_diaeresis | ä, ë, ï, ö, ü, ÿ |
| , (AB08) | dead_cedilla | ç |
| . (AB09) | (none) | (none) |
| Other dead keys | dead_macron, dead_breve, dead_abovering, dead_ogonek, dead_stroke, dead_horn, dead_belowdot, dead_doubleacute, dead_abovedot, dead_greek | Less common accents |

## Direct AltGr characters

| Key | AltGr (level 3) | Shift+AltGr (level 4) |
|---|---|---|
| ` (TLDE) | dead_grave | dead_tilde |
| 2 | ² | dead_doubleacute |
| 3 | ³ | dead_macron |
| 4 | ¢ | ¥ |
| 5 | € | £ |
| 6 | dead_circumflex | dead_caron |
| 7 | ™ | ® |
| 8 | dead_abovedot | dead_greek |
| = | ° | dead_abovering |
| Q | à | À |
| W | è | È |
| E | é | É |
| R | ê | Ê |
| Y | ù | Ù |
| U | ú | Ú |
| I | í | Í |
| O | ó | Ó |
| P | ò | Ò |
| [ | « | ‹ |
| ] | » | › |
| A | á | Á |
| G | î | Î |
| H | û | Û |
| J | ù | Ù |
| K | ï | Ï |
| L | õ | Õ |
| ; | ô | Ô |
| ' | dead_acute | dead_diaeresis |
| Z | ã | Ã |
| X | â | Â |
| C | ç | Ç |
| F | æ | Æ |
| . | œ | Œ |
| M | ì | Ì |
| , | ç | dead_cedilla |
| / | questiondown | dead_stroke |

## Install

```bash
./install.py            # current user (default, no sudo)
./install.py --system   # system-wide (needs sudo)
```

Then in KDE: System Settings -> Input Devices -> Keyboard -> Layouts -> Add -> search "Luso-FrEnglish" (PT-FR-EN).

## Uninstall

```bash
./install.py uninstall            # current user
./install.py uninstall --system   # system-wide
```

## Test quickly (X11 / XWayland)

```bash
setxkbmap -layout lusofrenglish
setxkbmap -query
```

## Revert (X11)

```bash
setxkbmap -layout us
```

## Notes
- For a user-only install (no sudo, survives package updates), use `./install.py`. KDE reads `~/.config/xkb` automatically.
- Using Left Alt as AltGr would break normal Alt shortcuts (menus, etc.), so only Right Alt is AltGr. If you really want it, enable XKB option `lv3:lalt_switch` (not recommended).
