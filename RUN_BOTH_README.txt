How to run frontend and backend at the same time
================================================

Option 1 – Use the script (easiest)
-----------------------------------
Double-click:  run-both.bat

This opens two terminal windows:
  • One runs the backend (uvicorn on port 8000)
  • One runs the frontend (http.server on port 8080)

Then open in your browser:  http://localhost:8080

If your backend is not in the folder  ..\backend  (sibling of frontend),
edit run-both.bat and change the line:
  set BACKEND_DIR=%~dp0..\backend
to your backend folder path.


Option 2 – Two terminals by hand
---------------------------------
Terminal 1 (backend):
  cd c:\code\healthsync\healthsync-demo\backend
  python -m uvicorn main:app --host 0.0.0.0 --port 8000

Terminal 2 (frontend):
  cd c:\code\healthsync\healthsync-demo\frontend
  python -m http.server 8080

Then open:  http://localhost:8080


Port 8000 already in use?
-------------------------
If the backend says "Only one usage of each socket address... (10048)":
  • Another backend (or app) is already using port 8000.
  • Double-click  free-port-8000.bat  to stop the process on port 8000, then run run-both.bat again.
  • Or close the other terminal where the backend was running, then run run-both.bat again.

To stop
-------
Close each terminal window, or press Ctrl+C in each.
