python copy_run_map.py
copy /y C:\Users\hppc\Desktop\GitHub\standalone_wildfireprediction\sa_map.html C:\Users\hppc\Desktop\GitHub\standalone_wildfireprediction\map\greekfireprediction.github.io\index.html
cd map\greekfireprediction.github.io
call git status && git add . && git commit -m "Update map" && git push
PAUSE