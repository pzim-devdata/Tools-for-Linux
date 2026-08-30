#!/usr/bin/env python3
"""
themecolorshift.py — AnyThemeColorShifter

Dynamic accent color shifter for Cinnamon desktop themes.
Clones a source theme, detects its accent color and all HSV derivatives,
shifts them to a new target color, and applies the modified theme instantly.

Features:
 - Dynamic derivative discovery (scans CSS + SVG, no hardcoded color lists)
 - Multiplicative HSV scaling (preserves relative brightness ratios)
 - Separate Desktop/Applications sources
 - System theme auto-copy from /usr/share/themes/ or /usr/share/cinnamon/theme/
 - Interactive color picker (--pick, via zenity with tkinter fallback)
 - Random color generation (--random)
 - Instant CSS reload via toggle-refresh
 - SVG asset recoloring

Usage:
 # Shift only Applications (GTK)
 python themecolorshift.py --random --theme-app Orchis-Light --variant proton_mix

 # Shift only Desktop (Cinnamon)
 python themecolorshift.py --pick --theme-desktop cinnamon --variant custom_desk

 # Shift both from different sources
 python themecolorshift.py "#6d4aff" --theme-app Orchis-Light --theme-desktop CBlack --variant proton_mix

 # Single source for Desktop + Applications
 python themecolorshift.py --random --theme-source Qogir-Light

 # Preview substitutions (--dry-run)
 python themecolorshift.py "#6d4aff" --theme-source Qogir-Light --dry-run

 # Skip theme reload (--no-refresh)
 python themecolorshift.py --random --theme-app Orchis-Light --no-refresh
"""

import sys
import re
import shutil
import colorsys
import argparse
import subprocess
from pathlib import Path
from collections import Counter

# ── Configuration ───────────────────────────────────────────────────
# Adjust these paths for your system if needed.

HOME = Path.home()
THEMES_DIR = HOME / ".local" / "share" / "themes"
SYSTEM_CINNAMON_THEME = Path("/usr/share/cinnamon/theme")
SYSTEM_THEMES = Path("/usr/share/themes")
SYSTEM_COPY_PREFIX = "_system_" # prefix for temporary system theme copies

# gsettings schemas
GS_CINNAMON = "org.cinnamon.theme"
GS_GTK = "org.cinnamon.desktop.interface"
GS_WM = "org.cinnamon.desktop.wm.preferences"

# ── Color conversion utilities ─────────────────────────────────────

def hex_to_rgb(h):
 """Convert '#rrggbb' to (r, g, b) tuple of ints 0-255."""
 h = h.lstrip("#")
 return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
 """Convert (r, g, b) tuple to '#rrggbb' lowercase string."""
 return "#{:02x}{:02x}{:02x}".format(*rgb)

def hex_to_hsv(h):
 """Convert '#rrggbb' to (h, s, v) tuple of floats 0.0-1.0."""
 r, g, b = [c / 255.0 for c in hex_to_rgb(h)]
 return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_hex(h, s, v):
 """Convert (h, s, v) floats to '#rrggbb' lowercase string."""
 r, g, b = colorsys.hsv_to_rgb(h, s, v)
 return rgb_to_hex(tuple(int(round(c * 255)) for c in (r, g, b)))

# ── Color picker ────────────────────────────────────────────────────

def parse_zenity_output(raw):
 """Parse all possible output formats from zenity --color-selection.
 Handles #rrggbb, rgb(R,G,B), rgba(R,G,B,A)."""
 raw = raw.strip()
 if not raw:
 return None
 if raw.startswith("#"):
 return raw.lower()
 if raw.startswith("rgb"):
 nums = re.findall(r'[\d.]+', raw)
 if len(nums) >= 3:
 rgb = tuple(int(float(nums[i])) for i in range(3))
 return rgb_to_hex(rgb)
 # Last resort: extract 3 numbers from any format
 nums = re.findall(r'[\d.]+', raw)
 if len(nums) >= 3:
 rgb = tuple(int(float(nums[i])) for i in range(3))
 return rgb_to_hex(rgb)
 return None

def pick_color_zenity(default="#6d4aff"):
 """Open zenity color picker. Returns hex string or None (cancelled/absent)."""
 try:
 r = subprocess.run(
 ["zenity", "--color-selection",
 f"--color={default}",
 "--title=Choose accent color"],
 capture_output=True, text=True, check=True
 )
 return parse_zenity_output(r.stdout)
 except FileNotFoundError:
 return None # zenity not installed
 except subprocess.CalledProcessError:
 return None # user cancelled (ESC / Cancel button)

def pick_color_tkinter(default="#6d4aff"):
 """Fallback color picker via tkinter.colorchooser."""
 try:
 import tkinter as tk
 from tkinter import colorchooser
 root = tk.Tk()
 root.withdraw()
 result = colorchooser.askcolor(color=default,
 title="Choose accent color")
 root.destroy()
 if result and result[1]:
 return result[1].lower()
 except Exception:
 pass
 return None

def pick_color(default="#6d4aff"):
 """Try zenity first (more native on Cinnamon/X11), fall back to tkinter."""
 color = pick_color_zenity(default)
 if color is not None:
 return color
 # zenity returned None: either absent or cancelled
 if not shutil.which("zenity"):
 print("[!] zenity not found, trying tkinter...")
 color = pick_color_tkinter(default)
 if color:
 return color
 print("[!] No color picker available")
 else:
 # zenity exists but returned None = user cancelled
 print("[!] Selection cancelled")
 return None

def random_color():
 """Generate a random pleasant accent color (high saturation, high value)."""
 import random
 # Curated hue options (excludes muddy brown/green tones)
 hue_options = [0.0, 0.08, 0.15, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5,
 0.55, 0.6, 0.7, 0.75, 0.8, 0.9]
 h = random.choice(hue_options)
 s = random.uniform(0.6, 0.95)
 v = random.uniform(0.7, 1.0)
 return hsv_to_hex(h, s, v)

# ── Neutral colors (excluded from accent detection) ────────────────

NEUTRAL_HEX = {
 "#ffffff", "#fffffe", "#fefefe", "#fdfdfe", "#fafbfc", "#f7f7f7",
 "#f0f3f6", "#f2f2f2", "#f6f6fb", "#fcfcfc", "#fafafc",
 "#000000", "#282a33", "#21232b", "#32343d", "#333641", "#434655",
 "#3e4250", "#51535b", "#464750", "#424656", "#4d5265", "#2c2f39",
 "#464853", "#4a4c59", "#23242a", "#6b6d75", "#85878e", "#5b5f68",
 "#9093a2", "#a3a4a9", "#b2b3b8", "#c4c5c9", "#d3dae3", "#7c7e86",
 "#7c8088", "#898d94", "#e6e6e6", "#e0e0e0", "#e3e4e5", "#d1dae3",
 "#dae2e9", "#eaeef2", "#e1e7ed", "#edf1f4", "#d3e1eb", "#e4edf3",
 "#f6f9fb", "#575a60", "#3f4145", "#a6a6a6", "#d1d3da", "#90949e",
 "#b6b8c0", "#7a7f8b", "#777983", "#e5d6ca",
 "#888888", "#888", "#666666", "#666", "#aaaaaa", "#aaa",
 "#eeeeee", "#eee", "#cccccc", "#ccc", "#444444", "#444",
 "#222222", "#222", "#111111", "#111",
 "#fc4138", "#f04a50", "#f27835", "#f08437", "#f46067", "#d05258",
 "#f68086", "#fd8d88", "#f7ae86", "#ff4d4d", "#ee3239", "#f26267",
 "#f4797e", "#f75d37",
 "#6dcfa7",
 "#9f9792", "#7b736e", "#574f4a", "#463e39", "#342c27",
 "#be916d", "#785336", "#e3cf9c", "#b08952",
 "#83b6ec", "#337fdc", "#cfe1f5", "#7ad9f1", "#0f9ac8", "#caeaf2",
 "#8de6b1", "#29ae74", "#cef8d8", "#b5e98a", "#6ab85b", "#e6f9d7",
 "#f8e359", "#d29d09", "#f9f4e1", "#ffcb62", "#d68400", "#ffead1",
 "#ffa95a", "#ed5b00", "#ffe5c5", "#f78773", "#e62d42", "#f8d2ce",
 "#e973ab", "#e33b6a", "#fac7de", "#cb78d4", "#9945b5", "#e7c2e8",
 "#9e91e8", "#7a59ca", "#d5d2f5", "#c0bfbc", "#6e6d71", "#d8d7d3",
}

# ── Accent color detection ─────────────────────────────────────────

def detect_accent_color(theme_dir):
 """
 Detect the dominant accent color of a theme.
 Priority: @define-color selected_bg_color > most frequent non-neutral hex.
 """
 css_files = list(theme_dir.rglob("*.css"))
 if not css_files:
 return None

 for css in css_files:
 try:
 content = css.read_text(encoding="utf-8", errors="ignore")
 except Exception:
 continue
 for pattern in (
 r'@define-color\s+selected_bg_color\s+(#[0-9a-fA-F]{6})',
 r'@define-color\s+theme_selected_bg_color\s+(#[0-9a-fA-F]{6})',
 r'@define-color\s+accent_bg_color\s+(#[0-9a-fA-F]{6})',
 ):
 m = re.search(pattern, content)
 if m:
 return m.group(1).lower()

 counter = Counter()
 for css in css_files:
 try:
 content = css.read_text(encoding="utf-8", errors="ignore")
 except Exception:
 continue
 for match in re.finditer(r'#([0-9a-fA-F]{6})\b', content):
 color = f"#{match.group(1).lower()}"
 if color not in NEUTRAL_HEX:
 counter[color] += 1
 if counter:
 return counter.most_common(1)[0][0]
 return None

# ── Dynamic derivative discovery ───────────────────────────────────

def is_derivative(h, s, v, acc_h, hue_tolerance=0.08, min_v=0.2, max_v=0.99):
 """
 Determine if an HSV color is a derivative of the accent color.

 Criteria:
 - Hue within ±hue_tolerance (0.08 ≈ 29 degrees) of the accent hue
 - Value (brightness) >= min_v (excludes dark grays/blacks)
 - Saturation adaptive:
 - s > 0.20 → clearly tinted, accept
 - s > 0.10 AND v > 0.80 → light tint (pastel), accept
 - otherwise → reject (likely noise)
 """
 if v < min_v or v > max_v:
 return False
 if s < 0.10:
 return False
 # Circular hue distance
 dh = abs(h - acc_h)
 if dh > 0.5:
 dh = 1.0 - dh
 if dh > hue_tolerance:
 return False
 # Adaptive saturation threshold
 if s > 0.20:
 return True
 if s > 0.10 and v > 0.80:
 return True
 return False

def discover_derivatives(theme_dir, accent_hex, hue_tolerance=0.08):
 """
 Scan all CSS and SVG files in the theme directory.
 Find every color whose hue is close to the accent.
 Returns a set of lowercase hex strings.
 """
 acc_h, acc_s, acc_v = hex_to_hsv(accent_hex)
 found = set()
 found.add(accent_hex.lower())

 files = list(theme_dir.rglob("*.css")) + list(theme_dir.rglob("*.svg"))
 for f in files:
 try:
 content = f.read_text(encoding="utf-8", errors="ignore")
 except Exception:
 continue
 for match in re.finditer(r'#([0-9a-fA-F]{6})\b', content):
 color = f"#{match.group(1).lower()}"
 if color in NEUTRAL_HEX or color in found:
 continue
 h, s, v = hex_to_hsv(color)
 if is_derivative(h, s, v, acc_h, hue_tolerance):
 found.add(color)
 return found

# ── Replacement palette construction ───────────────────────────────

def build_replacements(source_colors, source_accent, target_accent):
 """
 Build replacement map using multiplicative HSV scaling.

 For each source color:
 ratio_s = s_source / s_accent_source
 ratio_v = v_source / v_accent_source
 new_s = clamp(ratio_s * s_target, 0, 1)
 new_v = clamp(ratio_v * v_target, 0, 1)
 new_h = h_target (always use target hue)

 Returns:
 - hex_repl: dict {old_hex: new_hex} (includes both lower and upper case)
 - rgba_map: list of (src_r, src_g, src_b, tgt_r, tgt_g, tgt_b) tuples
 """
 tgt = target_accent.lower()
 src = source_accent.lower()
 t_h, t_s, t_v = hex_to_hsv(tgt)
 s_h, s_s, s_v = hex_to_hsv(src)

 hex_repl = {}
 rgba_map = []

 for sc in source_colors:
 sc = sc.lower()
 d_h, d_s, d_v = hex_to_hsv(sc)

 # Multiplicative ratios (guard against division by zero)
 ratio_s = d_s / s_s if s_s > 0.01 else 1.0
 ratio_v = d_v / s_v if s_v > 0.01 else 1.0

 new_s = max(0.0, min(1.0, ratio_s * t_s))
 new_v = max(0.0, min(1.0, ratio_v * t_v))
 tc = hsv_to_hex(t_h, new_s, new_v)

 # Store both lowercase and uppercase variants
 hex_repl[sc] = tc
 hex_repl[sc.upper()] = tc.upper()

 # Build rgba component map for regex substitution
 sr, sg, sb = hex_to_rgb(sc)
 tr, tg, tb = hex_to_rgb(tc)
 rgba_map.append((sr, sg, sb, tr, tg, tb))

 return hex_repl, rgba_map

# ── File substitution ───────────────────────────────────────────────

def replace_in_text(content, hex_repl, rgba_map):
 """Replace hex colors and rgba() values in a text string."""
 # 1. Replace hex values (sorted by length descending to avoid substring issues)
 for old in sorted(hex_repl.keys(), key=len, reverse=True):
 content = content.replace(old, hex_repl[old])
 # 2. Replace rgba(r, g, b, alpha) → rgba(tr, tg, tb, alpha)
 for sr, sg, sb, tr, tg, tb in rgba_map:
 content = re.sub(
 rf'rgba\(\s*{sr}\s*,\s*{sg}\s*,\s*{sb}\s*,',
 f'rgba({tr}, {tg}, {tb},',
 content
 )
 return content

def process_file(filepath, hex_repl, rgba_map):
 """Process a single file. Returns True if modified."""
 if not filepath.is_file():
 return False
 try:
 content = filepath.read_text(encoding="utf-8", errors="ignore")
 except Exception:
 return False
 new_content = replace_in_text(content, hex_repl, rgba_map)
 if new_content != content:
 filepath.write_text(new_content, encoding="utf-8")
 return True
 return False

def process_theme_dir(theme_dir, hex_repl, rgba_map):
 """Recursively process all relevant files in a theme directory."""
 modified = []
 # CSS, SVG, GTK2 config files
 for pattern in ("*.css", "*.svg", "gtkrc", "*.rc"):
 for f in theme_dir.rglob(pattern):
 if process_file(f, hex_repl, rgba_map):
 modified.append(str(f.relative_to(theme_dir)))
 # Theme metadata
 idx = theme_dir / "index.theme"
 if idx.is_file():
 content = idx.read_text(encoding="utf-8")
 new = replace_in_text(content, hex_repl, rgba_map)
 if new != content:
 idx.write_text(new, encoding="utf-8")
 modified.append("index.theme")
 meta = theme_dir / "metadata.json"
 if process_file(meta, hex_repl, rgba_map):
 modified.append("metadata.json")
 # Plank dock theme (if present)
 dock = theme_dir / "plank" / "dock.theme"
 if process_file(dock, hex_repl, rgba_map):
 modified.append("plank/dock.theme")
 return modified

# ── Theme sourcing and cloning ─────────────────────────────────────

def ensure_theme_available(source_name):
 """
 Locate a theme and make it available in ~/.local/share/themes/.

 Search order:
 1. Already present in ~/.local/share/themes/<name>/ → use directly
 2. Exists in /usr/share/themes/<name>/ → copy to temporary _system_<name>/
 3. Default Cinnamon theme at /usr/share/cinnamon/theme/ → copy to
 _system_<name>/cinnamon/ (creates proper theme structure)

 Returns: (Path, is_temporary) or (None, False) if not found.
 The caller is responsible for cleaning up temporary copies.
 """
 local_dir = THEMES_DIR / source_name
 if local_dir.is_dir():
 return (local_dir, False)

 THEMES_DIR.mkdir(parents=True, exist_ok=True)

 # Temporary name to avoid conflicts with system themes
 temp_name = f"{SYSTEM_COPY_PREFIX}{source_name}"
 temp_dir = THEMES_DIR / temp_name
 if temp_dir.exists():
 shutil.rmtree(temp_dir)

 # 1. Standard system theme
 usr_theme = SYSTEM_THEMES / source_name
 if usr_theme.is_dir():
 print(f" [INFO] Copying from /usr/share/themes/{source_name}")
 shutil.copytree(usr_theme, temp_dir)
 return (temp_dir, True)

 # 2. Default Cinnamon theme (flat structure, needs cinnamon/ subdir)
 if source_name == "cinnamon" and SYSTEM_CINNAMON_THEME.is_dir():
 print(f" [INFO] Copying default Cinnamon theme")
 cinnamon_subdir = temp_dir / "cinnamon"
 shutil.copytree(SYSTEM_CINNAMON_THEME, cinnamon_subdir)
 # Create minimal index.theme
 idx = temp_dir / "index.theme"
 idx.write_text(
 "[X-Cinnamon]\n"
 "Name=cinnamon\n"
 "Type=X-Cinnamon-Theme\n",
 encoding="utf-8"
 )
 return (temp_dir, True)

 return (None, False)

def clone_theme(source_dir, source_name, target_name):
 """Clone a theme directory and update its name in metadata files."""
 target_dir = THEMES_DIR / target_name
 if not source_dir.is_dir():
 print(f"[!] Source theme not found: {source_dir}")
 return None
 if target_dir.exists():
 shutil.rmtree(target_dir)
 shutil.copytree(source_dir, target_dir)

 # Update Name= in index.theme
 idx = target_dir / "index.theme"
 if idx.is_file():
 c = idx.read_text(encoding="utf-8")
 c = re.sub(r'^Name\s*=.*$', f"Name={target_name}", c, flags=re.MULTILINE)
 idx.write_text(c, encoding="utf-8")

 # Update "name" in metadata.json
 meta = target_dir / "metadata.json"
 if meta.is_file():
 c = meta.read_text(encoding="utf-8")
 c = re.sub(r'"name"\s*:\s*"[^"]*"', f'"name": "{target_name}"', c)
 meta.write_text(c, encoding="utf-8")

 return target_dir

# ── gsettings utilities ─────────────────────────────────────────────

def gs_get(schema, key):
 """Get a gsettings value. Returns empty string on failure."""
 try:
 r = subprocess.run(["gsettings", "get", schema, key],
 capture_output=True, text=True, check=True)
 return r.stdout.strip().strip("'")
 except subprocess.CalledProcessError:
 return ""

def gs_set(schema, key, value):
 """Set a gsettings value with console output."""
 try:
 subprocess.run(["gsettings", "set", schema, key, value], check=True)
 print(f" [OK] {schema} {key} = '{value}'")
 return True
 except subprocess.CalledProcessError as e:
 print(f" [!] Failed {schema} {key}: {e}")
 return False

def gs_set_quiet(schema, key, value):
 """Set a gsettings value silently (used during refresh toggle)."""
 try:
 subprocess.run(["gsettings", "set", schema, key, value], check=True)
 return True
 except subprocess.CalledProcessError:
 return False

# ── Theme refresh (force CSS reload) ────────────────────────────────

def refresh_themes(desk_name, app_name, wm_name,
 do_desktop=True, do_app=True):
 """
 Force theme CSS reload by toggling to an alternate theme and back.

 do_desktop and do_app allow refreshing only what was modified.
 If both share the same name, a single grouped toggle is performed.
 """
 import time
 import random

 # List available themes (local + system)
 available = set()
 if THEMES_DIR.is_dir():
 for d in THEMES_DIR.iterdir():
 if d.is_dir() and not d.name.startswith(SYSTEM_COPY_PREFIX):
 available.add(d.name)
 if SYSTEM_THEMES.is_dir():
 for d in SYSTEM_THEMES.iterdir():
 if d.is_dir():
 available.add(d.name)

 # Grouped refresh (same theme for desktop + apps)
 if do_desktop and do_app and desk_name == app_name:
 candidates = available - {desk_name, wm_name}
 if not candidates:
 print(" [!] No alternate theme available for grouped refresh")
 return
 alt = random.choice(sorted(candidates))
 print(f" [*] Grouped refresh: switching to '{alt}' and back")
 gs_set_quiet(GS_CINNAMON, "name", alt)
 gs_set_quiet(GS_GTK, "gtk-theme", alt)
 gs_set_quiet(GS_WM, "theme", alt)
 time.sleep(0.5)
 gs_set_quiet(GS_CINNAMON, "name", desk_name)
 gs_set_quiet(GS_GTK, "gtk-theme", app_name)
 gs_set_quiet(GS_WM, "theme", wm_name)
 print(" [OK] Desktop + Applications reloaded")
 return

 # Separate refresh
 if do_app:
 candidates = available - {app_name}
 if candidates:
 alt = random.choice(sorted(candidates))
 print(f" [*] Applications refresh: switching to '{alt}' and back")
 gs_set_quiet(GS_GTK, "gtk-theme", alt)
 time.sleep(0.3)
 gs_set_quiet(GS_GTK, "gtk-theme", app_name)
 print(" [OK] Applications reloaded")
 else:
 print(" [!] No alternate theme for Applications")

 if do_desktop:
 candidates = available - {desk_name, wm_name}
 if candidates:
 alt = random.choice(sorted(candidates))
 print(f" [*] Desktop refresh: switching to '{alt}' and back")
 gs_set_quiet(GS_CINNAMON, "name", alt)
 gs_set_quiet(GS_WM, "theme", alt)
 time.sleep(0.3)
 gs_set_quiet(GS_CINNAMON, "name", desk_name)
 gs_set_quiet(GS_WM, "theme", wm_name)
 print(" [OK] Desktop reloaded")
 else:
 print(" [!] No alternate theme for Desktop")

# ── Per-theme processing pipeline ───────────────────────────────────

def shift_one_theme(source_name, target_accent, variant_suffix, dry_run=False):
 """
 Full pipeline for one theme:
 locate → detect accent → discover derivatives → build replacements
 → clone → substitute → return result.

 Returns: (target_name, target_dir, hex_repl, rgba_map) or None.
 """
 source_dir, is_temp = ensure_theme_available(source_name)
 if not source_dir or not source_dir.is_dir():
 print(f"[!] Theme source not found: {source_name}")
 return None

 try:
 accent = detect_accent_color(source_dir)
 if not accent:
 print(f"[!] Accent not detected for '{source_name}'")
 return None

 source_colors = discover_derivatives(source_dir, accent)
 print(f" Source: {source_name} (accent {accent}, {len(source_colors)} derivatives)")

 hex_repl, rgba_map = build_replacements(source_colors, accent, target_accent)
 target_name = f"{source_name}{variant_suffix}"
 print(f" Target: {target_name} (accent {target_accent})")
 print(f" {len(hex_repl)} hex substitutions, {len(rgba_map)} rgba patterns")

 if dry_run:
 print(" --- Substitutions ---")
 seen = set()
 for old in sorted(hex_repl.keys()):
 if old.startswith("#") and len(old) == 7 and old.lower() not in seen:
 seen.add(old.lower())
 print(f" {old} -> {hex_repl[old]}")
 return (target_name, None, hex_repl, rgba_map)

 target_dir = clone_theme(source_dir, source_name, target_name)
 if not target_dir:
 return None

 modified = process_theme_dir(target_dir, hex_repl, rgba_map)
 print(f" {len(modified)} file(s) modified")
 for f in modified[:15]:
 print(f" - {f}")
 if len(modified) > 15:
 print(f" ... and {len(modified) - 15} more")

 return (target_name, target_dir, hex_repl, rgba_map)

 finally:
 # Clean up temporary system theme copy
 if is_temp and source_dir.exists():
 shutil.rmtree(source_dir)
 print(f" [INFO] Temporary copy removed: {source_dir.name}")

# ── Main entry point ────────────────────────────────────────────────

def normalize_variant(v):
 """Ensure variant starts with '-'."""
 if not v:
 return "-custom"
 return v if v.startswith("-") else f"-{v}"

def main():
 parser = argparse.ArgumentParser(
 description="AnyThemeColorShifter — Change accent color of any Cinnamon/GTK theme."
 )
 parser.add_argument("color", nargs='?', default=None,
 help='Target color as hex (e.g. "#6d4aff"). '
 'Omitted if --pick or --random is used.')
 parser.add_argument("--pick", action="store_true",
 help="Open interactive color picker (zenity)")
 parser.add_argument("--random", action="store_true",
 help="Generate a random pleasant accent color")

 # Theme source group (mutually exclusive but optional)
 src = parser.add_mutually_exclusive_group(required=False)
 src.add_argument("--theme-source",
 help="Single theme for both Desktop and Applications")
 src.add_argument("--theme-app",
 help="Source theme for Applications (GTK) only")

 parser.add_argument("--theme-desktop", default=None,
 help="Source theme for Desktop (Cinnamon). "
 "If omitted with --theme-app, Desktop stays unchanged.")
 parser.add_argument("--variant", default="-custom",
 help="Suffix for the derived theme name (default: -custom)")
 parser.add_argument("--dry-run", action="store_true",
 help="Print substitutions without applying")
 parser.add_argument("--no-refresh", action="store_true",
 help="Skip theme toggle-refresh (for headless/SSH)")
 args = parser.parse_args()

 # Validate: at least one theme must be specified
 if not args.theme_source and not args.theme_app and not args.theme_desktop:
 print("[!] Specify at least one theme: --theme-source, --theme-app, or --theme-desktop")
 sys.exit(1)

 # Resolve target color
 if args.random:
 target = random_color()
 print(f"[*] Generated color: {target}\n")
 elif args.pick:
 target = pick_color()
 if not target:
 sys.exit(1)
 print(f"[*] Selected color: {target}\n")
 elif args.color:
 target = args.color.lower()
 if not re.match(r'^#[0-9a-fA-F]{6}$', target):
 print("[!] Invalid format. Expected: #RRGGBB")
 sys.exit(1)
 else:
 print("[!] Specify a hex color, --pick, or --random")
 sys.exit(1)

 variant = normalize_variant(args.variant)

 # Determine which themes to process
 if args.theme_source:
 app_source = args.theme_source
 desktop_source = args.theme_source
 has_desktop = True
 has_app = True
 elif args.theme_app:
 app_source = args.theme_app
 desktop_source = args.theme_desktop
 has_app = True
 has_desktop = desktop_source is not None
 elif args.theme_desktop:
 app_source = None
 desktop_source = args.theme_desktop
 has_app = False
 has_desktop = True
 else:
 print("[!] Invalid configuration")
 sys.exit(1)

 same_source = has_desktop and has_app and (app_source == desktop_source)

 THEMES_DIR.mkdir(parents=True, exist_ok=True)

 print(f"=== AnyThemeColorShifter: {target} ===\n")

 # Process Applications (GTK)
 if has_app:
 print("[Applications / GTK]")
 app_result = shift_one_theme(app_source, target, variant, args.dry_run)
 else:
 print("[Applications / GTK]")
 print(" (skipped: --theme-app/--theme-source not specified)")
 app_name = gs_get(GS_GTK, "gtk-theme")
 if app_name:
 print(f" Current theme preserved: {app_name}")
 app_result = (app_name, None, {}, [])

 # Process Desktop (Cinnamon)
 if has_desktop:
 print("\n[Desktop / Cinnamon]")
 if same_source:
 print(" (same source: reused)")
 desk_result = app_result
 else:
 desk_result = shift_one_theme(desktop_source, target, variant, args.dry_run)
 else:
 print("\n[Desktop / Cinnamon]")
 print(" (skipped: --theme-desktop not specified)")
 current_desk = gs_get(GS_CINNAMON, "name")
 if current_desk:
 print(f" Current theme preserved: {current_desk}")
 desk_result = None

 if args.dry_run:
 print("\n[*] Dry-run complete.")
 return

 # Validate results
 if has_app and not app_result:
 print("\n[!] Applications failed. Aborting.")
 sys.exit(1)
 if not has_app and not desk_result:
 print("\n[!] No theme modified. Aborting.")
 sys.exit(1)

 # Apply via gsettings
 print(f"\n[Applying gsettings]")

 if has_app:
 app_name = app_result[0]
 gs_set(GS_GTK, "gtk-theme", app_name)
 else:
 print(" [SKIP] Applications theme not modified")

 if same_source:
 gs_set(GS_CINNAMON, "name", app_name)
 gs_set(GS_WM, "theme", app_name)
 elif has_desktop and desk_result:
 desk_name = desk_result[0]
 gs_set(GS_CINNAMON, "name", desk_name)
 gs_set(GS_WM, "theme", desk_name)
 else:
 print(" [SKIP] Desktop theme not modified")

 # Refresh: force CSS reload
 if not args.no_refresh:
 if same_source:
 final_desk = app_result[0] if has_app else None
 final_wm = final_desk
 refresh_themes(final_desk, final_desk, final_wm,
 do_desktop=True, do_app=True)
 elif has_app and has_desktop and desk_result:
 final_desk = desk_result[0]
 final_wm = final_desk
 refresh_themes(final_desk, app_result[0], final_wm,
 do_desktop=True, do_app=True)
 elif has_app:
 final_desk = gs_get(GS_CINNAMON, "name") or app_result[0]
 final_wm = gs_get(GS_WM, "name") or final_desk
 refresh_themes(final_desk, app_result[0], final_wm,
 do_desktop=False, do_app=True)
 elif has_desktop:
 final_app = gs_get(GS_GTK, "gtk-theme") or ""
 final_desk = desk_result[0]
 final_wm = final_desk
 refresh_themes(final_desk, final_app, final_wm,
 do_desktop=True, do_app=False)

 # Summary
 print(f"\n[OK]")
 if has_app:
 print(f" Applications='{app_name}',", end="")
 if has_desktop and desk_result:
 print(f" Desktop='{desk_result[0]}',", end="")
 print(f" Accent={target}")
 if not args.no_refresh:
 print(" Theme(s) reloaded live.")
 else:
 print(" Restart apps to see changes.")

if __name__ == "__main__":
 main()