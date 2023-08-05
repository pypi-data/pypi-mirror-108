#!/usr/local/munki/munki-python

import os
import plistlib
import shutil
import subprocess
import sys

dock_plist_path = os.path.expanduser("~/Library/Preferences/com.apple.dock.plist")
if not os.path.isfile(dock_plist_path):
    sys.exit("No dock preferences file exists.")

print("Saving backup of dock preferences...")
shutil.copy(dock_plist_path, dock_plist_path.replace(".plist", ".backup.plist"))

with open(dock_plist_path, "rb") as openfile:
    dock_plist = plistlib.load(openfile)

translation_map = (
    # Dock preference keys to migrate from/to
    ("static-apps", "persistent-apps"),
    ("static-others", "persistent-others"),
)

changed = False
for t in translation_map:
    if not dock_plist.get(t[0]):
        print("No %s in dock preferences." % t[0])
        continue

    if not dock_plist.get(t[1]):
        dock_plist[t[1]] = []
    for idx, t_item in enumerate(dock_plist[t[0]]):
        print("Moving to %s: %s" % (t[1], t_item))
        dock_plist[t[1]].insert(idx, t_item)

    print("Deleting %s from dock preferences..." % t[0])
    del dock_plist[t[0]]
    changed = True

if not changed:
    print("No changes were made. Exiting.")
    sys.exit(0)

print("Writing changes to dock preferences...")
with open(dock_plist_path, "wb") as openfile:
    openfile.write(plistlib.dumps(dock_plist))

print("Relaunching Dock...")
subprocess.run(["killall", "cfprefsd", "Dock"], check=True)
