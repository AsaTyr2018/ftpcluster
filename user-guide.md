# FTPCluster User Guide

The portal uses a comfortable dark theme and lets you fetch files from multiple servers with a single login.

---

## Sign In

1. Open `http://<server>:8080` in your browser.
2. Enter your username and password.

---

## Finding Your Files

- After login the dashboard lists the servers you may access.
- Click a server name to browse its virtual folder.
- Every file is available via a URL pattern:
```
/ftp/<username>/<server_alias>/path/to/file
```
Example:
```
/ftp/user1/serverA/docs/readme.txt
```
Download files with your browser or a tool like `curl`.

---

## Need Help?

If a server is missing or you encounter permission errors, contact your administrator.
