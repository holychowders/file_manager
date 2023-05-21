# File Manager

**Semi-abandoned project to create a minimalistic file manager with tags and better-than-average organization capabilities**

---

Stack: python, tkinter, sqlite
</br>
Tools: [pre-commit](.pre-commit-config.yaml), [GitHub Actions](.github/workflows/pre-commit.yaml)
</br>
Support: Windows, Linux, untested on Mac (probably works)

## Details

### UI and Behavior on `main`

![Image of GUI on `main` branch](screenshots/main_gui.png)

The UI on the `main` branch currently allows adding, deleting, and live-searching tags in the underlying database. Upon typing in the `Search/Edit` field of the `Tags` section, the tags list below it will update with current matches. If there are matching tags, the user can select any of them. If the user's search is an exact match, pressing the `+/-` button hides the tag from the user interface. If there is no exact match, pressing the `+/-` button creates a new tag. There's currently no way to actually delete a tag from the database from the UI. `Clear Selections` clears the search box and deselects all tags.

When tags are selected, the `Files` section updates to list files that contain matches for all of the tags selected. Files that do not include every selected tag are filtered out.

Clicking a listed file result from the `Files` section (paths hardcoded) opens it using the system's default opener. Middle clicking on a file result "selects" it and updates the `Selected File` section to include information about that file.

The UI resizes fairly gracefully. There's also a (not totally dark) dark mode.

The UI is obviously very clunky and not very minimal -- lots of unecessary lines and boxes are present. You'll also notice that it has lots of flickering on interaction, as interaction causes the entire UI to be re-constructed. Because it was written in a tightly-coupled way that was very difficult to change, a rewrite of this GUI was initiated on the `rewrite_gui` branch as opposed to simply updating the original.

### UI and Behavior on `rewrite_gui`

![Image of GUI on `rewrite_gui` branch](screenshots/rewrite_gui.png)

This rewrite of the UI was started because of the obnoxious flickering on interaction on the original (as stated in [above](#ui-and-behavior-on-main)). The in-progress rework can be used by passing `gui2` as an argument to the normal run command: `python file_manager/main.py gui2`.

This UI can search and select tags and search files. That's about it.
