# Tracker

The CSV you carry between sessions so a new conversation, on any model, can pick up where the last one stopped.

Download `tracker_template.csv`, fill it as you go, and re-upload it at the start of each session. [COLUMNS.md](COLUMNS.md) defines every field.

Keep your filled copy outside this repository. The `.gitignore` is set so a file named `tracker_mine.csv` or `tracker_filled.csv` is never committed by accident.

When you are ready to write a complaint or arbitration submission, `scripts/export_chronology.py` turns a filled-in tracker into a plain-text, date-sorted chronology you can paste into the form.
