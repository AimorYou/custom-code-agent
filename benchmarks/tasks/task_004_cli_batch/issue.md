# Support processing entire directories

Right now `fileproc` only works with a single file at a time, which makes it pretty tedious when you have a directory full of reports to process. It would be really helpful to have a `--batch` flag that accepts a directory path and processes everything in it.

Something like:

```bash
fileproc --batch ./reports/
```

The output should be a mapping of each file to its processed result.

One other thing I noticed while trying to work around this manually — I wrote a small script that used `list_supported_files()` to grab `.txt` and `.csv` files from a folder, but it seemed to pick up everything in the directory including `.log` and `.tmp` files. Not sure if that's intentional or a separate issue, but it caused `process_file` to choke on formats it doesn't understand.

Would be great to get the batch flag added and that file listing thing sorted out. Happy to test once there's a branch to look at.
