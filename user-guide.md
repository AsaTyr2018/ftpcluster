# User Guide

This document is aimed at regular users without admin rights and explains how to use FTPCluster.

## Login

1. Open the application's login page (`/`).
2. Enter your username and password.
3. After a successful login you will be redirected to the dashboard.

## Dashboard and server access

- The dashboard shows all servers you have access to.
- Navigate to a server folder to fetch files through the integrated proxy.
- File URLs follow the pattern:
  ```
  /ftp/<username>/<server_alias>/path/to/file
  ```
  Example:
  ```
  /ftp/user1/server2/data/report.csv
  ```
- Download files using a normal browser download or a command line tool such as `curl`.

If you experience access problems, contact an administrator so the appropriate permissions can be set.
