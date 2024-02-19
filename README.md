# Wish calendar on kivy
To run from IDE:
1. Install dependencies::
```
     pip install -r requirements.txt
```
2. Run main.py

To make .exe file:
1. Install dependencies:
```
    pip install -r requirements.txt
```

2. Correctly set up main.spec file:
```
    main.spec.exemple --> main.spec
```

3. Run PyInstaller:
```
    pyinstaller main.spec  
```

4. When the file is built, the .exe file will be in the **dist** directory.