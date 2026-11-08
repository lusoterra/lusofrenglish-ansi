#!/usr/bin/env python3
import argparse, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "lusofrenglish")

SYSTEM_SYMBOLS = "/usr/share/X11/xkb/symbols/lusofrenglish"
SYSTEM_LST = "/usr/share/X11/xkb/rules/evdev.lst"
SYSTEM_XML = "/usr/share/X11/xkb/rules/evdev.xml"

USER_BASE = os.path.expanduser("~/.config/xkb")
USER_SYMBOLS = os.path.join(USER_BASE, "symbols", "lusofrenglish")
USER_RULES = os.path.join(USER_BASE, "rules")
USER_LST = os.path.join(USER_RULES, "evdev.lst")
USER_EVDEV = os.path.join(USER_RULES, "evdev")
USER_XML = os.path.join(USER_RULES, "evdev.xml")

EVDEV_XML_BLOCK = """  <layout>
    <configItem>
      <name>lusofrenglish</name>
      <shortDescription>PT-FR-EN</shortDescription>
      <description>English (Luso-FrEnglish, AltGr dead keys)</description>
      <countryList><iso3166Id>us</iso3166Id></countryList>
      <languageList><iso639Id>eng</iso639Id><iso639Id>por</iso639Id><iso639Id>fra</iso639Id></languageList>
    </configItem>
  </layout>
"""


def run(cmd):
    subprocess.run(cmd, check=True)


def install_system():
    run(["sudo", "cp", SRC, SYSTEM_SYMBOLS])
    # evdev.lst
    if os.path.exists(SYSTEM_LST):
        text = open(SYSTEM_LST).read()
        if "lusofrenglish" not in text.splitlines().__str__():
            pass
        if not any(l.startswith("lusofrenglish") for l in text.splitlines()):
            # append after ! layout
            text = text.replace("! layout\n", "! layout\nlusofrenglish   English (Luso-FrEnglish, AltGr dead keys)\n", 1)
            # write via sudo tee
            p = subprocess.Popen(["sudo", "tee", SYSTEM_LST], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
            p.communicate(text)
            if p.returncode:
                raise SystemExit("failed to update evdev.lst")
    # evdev.xml
    if os.path.exists(SYSTEM_XML):
        text = open(SYSTEM_XML).read()
        if "lusofrenglish" not in text:
            text = text.replace("</layoutList>", EVDEV_XML_BLOCK + "</layoutList>", 1)
            p = subprocess.Popen(["sudo", "tee", SYSTEM_XML], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
            p.communicate(text)
            if p.returncode:
                raise SystemExit("failed to update evdev.xml")


def uninstall_system():
    run(["sudo", "rm", "-f", SYSTEM_SYMBOLS])
    if os.path.exists(SYSTEM_LST):
        text = open(SYSTEM_LST).read()
        lines = [l for l in text.splitlines() if not l.startswith("lusofrenglish")]
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        p = subprocess.Popen(["sudo", "tee", SYSTEM_LST], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        p.communicate(text)
    if os.path.exists(SYSTEM_XML):
        text = open(SYSTEM_XML).read()
        text = re.sub(r"\s*<layout>\s*<configItem>\s*<name>lusofrenglish</name>.*?</configItem>\s*</layout>\s*", "\n", text, count=1, flags=re.S)
        p = subprocess.Popen(["sudo", "tee", SYSTEM_XML], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        p.communicate(text)


def install_user():
    os.makedirs(os.path.dirname(USER_SYMBOLS), exist_ok=True)
    os.makedirs(USER_RULES, exist_ok=True)
    shutil.copyfile(SRC, USER_SYMBOLS)
    # evdev rules: copy system then add mapping
    if not os.path.exists(USER_EVDEV):
        shutil.copyfile("/usr/share/X11/xkb/rules/evdev", USER_EVDEV)
    text = open(USER_EVDEV).read()
    if "lusofrenglish" not in text:
        text = text.replace("  *			 us_intl		=	pc+us(alt-intl)\n",
                            "  *			 us_intl		=	pc+us(alt-intl)\n  *			 lusofrenglish	=	pc+lusofrenglish\n")
        open(USER_EVDEV, "w").write(text)
    # evdev.xml
    open(USER_XML, "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE xkbConfigRegistry SYSTEM "xkb.dtd">\n'
        '<xkbConfigRegistry version="1.1">\n'
        '  <layoutList>\n' + EVDEV_XML_BLOCK + '  </layoutList>\n'
        '</xkbConfigRegistry>\n'
    )
    print("Installed for current user in ~/.config/xkb")
    print("Log out and back in (Wayland) or run: setxkbmap -layout lusofrenglish")


def uninstall_user():
    for p in (USER_SYMBOLS,):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
    # remove mapping line
    if os.path.exists(USER_EVDEV):
        text = open(USER_EVDEV).read()
        text = text.replace("  *			 lusofrenglish	=	pc+lusofrenglish\n", "")
        open(USER_EVDEV, "w").write(text)
    for p in (USER_XML,):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
    print("Removed user-level layout.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["install", "uninstall"], nargs="?", default="install")
    ap.add_argument("--system", action="store_true", help="install system-wide (needs sudo)")
    args = ap.parse_args()

    user = not args.system
    if user:
        if args.action == "install":
            install_user()
        else:
            uninstall_user()
    else:
        if args.action == "install":
            install_system()
        else:
            uninstall_system()


if __name__ == "__main__":
    main()
