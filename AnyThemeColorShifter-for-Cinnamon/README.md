# AnyThemeColorShifter-for-Cinnamon

Change the accent color of any Cinnamon/GTK theme in seconds.

This tool clones a theme, detects its dominant accent color and all derived variants (hover, active, borders, disabled states), shifts them to a new target color using HSV scaling, and applies the modified theme instantly via gsettings.

#### Insert image of before/after comparison ####

## Quick Start

```bash
# Install
mkdir -p ~/.local/bin
curl -o ~/.local/bin/themecolorshift.py https://raw.githubusercontent.com/pzim-devdata/Tools-for-Linux/main/AnyThemeColorShifter-for-Cinnamon/themecolorshift.py
chmod +x ~/.local/bin/themecolorshift.py

# Run
themecolorshift.py --pick --theme-source Qogir-Light --variant mycolor
```

## Dependencies

- `python3` (standard on all Linux distributions)
- `gsettings` (bundled with Cinnamon/GNOME)
- `zenity` (optional, for `--pick` interactive color picker)

```bash
sudo apt install zenity   # Debian/Ubuntu/Mint
```

## Usage Examples

```bash
# Pick a color interactively, apply to Desktop + Applications
themecolorshift.py --pick --theme-source Qogir-Light

# Random color on Applications (GTK) only
themecolorshift.py --random --theme-app Orchis-Light --variant random

# Random color on Desktop (Cinnamon) only
themecolorshift.py --random --theme-desktop cinnamon --variant random

# Specific hex color, different themes for Desktop and Applications
themecolorshift.py "#6d4aff" --theme-app Orchis-Light --theme-desktop CBlack --variant mix

# Preview substitutions without applying
themecolorshift.py "#e66100" --theme-source Qogir-Light --dry-run
```

## Arguments

| Argument | Description |
|----------|-------------|
| `color` | Target hex color (e.g. `"#6d4aff"`) |
| `--pick` | Open interactive color picker (zenity) |
| `--random` | Generate a random pleasant color |
| `--theme-source NAME` | Use one theme for both Desktop + Applications |
| `--theme-app NAME` | Source theme for Applications (GTK) only |
| `--theme-desktop NAME` | Source theme for Desktop (Cinnamon) only |
| `--variant SUFFIX` | Suffix for the new theme name (default: `-custom`) |
| `--dry-run` | Preview substitutions without modifying files |
| `--no-refresh` | Skip live CSS reload (for SSH/headless) |

At least one of `--theme-source`, `--theme-app`, or `--theme-desktop` is required.
One of `color`, `--pick`, or `--random` is required.

## Important Notes

**Theme cloning:** The original theme is never modified. A new theme is created with the suffix you specify. If you omit `--variant`, the suffix defaults to `-custom` (e.g., `Qogir-Light` becomes `Qogir-Light-custom`).

**PNG assets:** PNG/raster images (GTK2 checkboxes, switches) are not recolored. Only CSS and SVG files are processed. Some elements may retain original colors if they rely on PNG assets.

## Autostart (random color on each boot)

Open **Startup Applications** in Cinnamon menu, click **Add**, and enter:

- **Name**: `AnyThemeColorShifter`
- **Command**: `/home/YOUR_USERNAME/.local/bin/themecolorshift.py --random --theme-app Orchis-Light --variant auto`

To also shift the Desktop (Cinnamon shell), add another entry:

- **Name**: `AnyThemeColorShifter-Desktop`
- **Command**: `/home/YOUR_USERNAME/.local/bin/themecolorshift.py --random --theme-desktop cinnamon --variant auto`

## How It Works

1. Locates the source theme (`~/.local/share/themes/`, then `/usr/share/themes/`, then `/usr/share/cinnamon/theme/`)
2. Detects the accent color via `@define-color selected_bg_color` in CSS
3. Scans all CSS and SVG files for hue-related derivatives
4. Shifts all derivatives to the new target color using multiplicative HSV scaling
5. Clones the theme, substitutes colors in CSS/SVG/gtkrc/metadata files
6. Applies via gsettings and forces CSS reload by toggling themes briefly

## Repository Structure

```text
AnyThemeColorShifter-for-Cinnamon/
├── themecolorshift.py
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT License
