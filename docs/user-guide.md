# FTPCluster User Guide

FTPCluster lets you reach multiple FTP servers with a single login. After signing in you will see only the servers assigned to you.

---

## Sign In

1. Open `http://<server>:8080` in your browser.
2. Enter your username and password.

---

## Accessing Files

- The dashboard lists all servers you can reach.
- Click a server name to browse its virtual folder.
- Every file follows the pattern:

```
/ftp/<username>/<server_alias>/path/to/file
```

Example:

```
/ftp/user1/serverA/docs/readme.txt
```

Use your browser or a tool like `curl` to download files.

---

## Need Help?

If a server is missing or you see permission errors, please contact your administrator.
