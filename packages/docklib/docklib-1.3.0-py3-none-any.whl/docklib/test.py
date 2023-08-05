from docklib import Dock

# Load the current Dock
dock = Dock()

# List of desired apps
apps = [
    "/System/Applications/Launchpad.app",
    "/Applications/Google Chrome.app",
    "/Applications/Slack.app",
    "/Applications/Managed Software Center.app",
    "/System/Applications/System Preferences.app",
]

# Create a new list to contain the apps' items
persistent_apps = []

# Add each item to the list
for app in apps:
    persistent_apps.append(dock.makeDockAppEntry(app))

# Save the Dock
dock.save()

# app_changes = {
#     "add": [
#         "/Applications/Managed Software Center.app",
#     ],
#     "remove": [
#         "Calendar",
#         "Contacts",
#         "Reminders",
#         "FaceTime",
#     ],
#     "replace": [
#         ("Safari", "/Applications/Microsoft Edge.app"),
#         ("Mail", "/Applications/Microsoft Outlook.app"),
#         ("Pages", "/Applications/Microsoft Word.app"),
#         ("Numbers", "/Applications/Microsoft Excel.app"),
#         ("Keynote", "/Applications/Microsoft PowerPoint.app"),
#         ("Messages", "/Applications/Microsoft Teams.app"),
#         ("Notes", "/Applications/Microsoft OneNote.app"),
#     ],
# }
# for app in app_changes["add"]:
#     item = dock.makeDockAppEntry(app)
#     dock.items["persistent-apps"].append(item)
# for app in app_changes["remove"]:
#     dock.removeDockEntry(app)
# for app in app_changes["replace"]:
#     dock.replaceDockEntry(app[0], app[1])
# dock.save()
