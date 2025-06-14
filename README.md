# getthis

ME

    sudo apt-get update && sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

    python3 -m venv venv --system-site-packages

    source venv/bin/activate

    pip install -r requirements.txt

WINDOWS

    Install Python from python.org (ensure "Add to PATH" is checked).

    Install WebView2 from Microsoft's site if needed.

- terminal

    python -m venv venv

    .\venv\Scripts\activate

    pip install -r requirements.txt


RUN

    (source venv/bin/activate or .\venv\Scripts\activate).

    python -m shop_app.main

Run the Admin

    python -m admin_app.admin_main




### source

```
.
├── README.md
├── admin_app
│   ├── __init__.py
│   ├── admin_api.py
│   ├── admin_app.py
│   ├── admin_main.py
│   ├── admin_payload.py
│   └── admin_views.py
├── assets
│   ├── css
│   │   └── style.css
│   ├── fonts
│   │   └── RocaOne.ttf
│   └── images
│       ├── 9.jpg
│       ├── lanyard.png
│       ├── pup_logo.png
│       └── tshirt.png
├── requirements.txt
├── shared
│   ├── __init__.py
│   ├── builder.py
│   └── database.py
└── shop_app
    ├── __init__.py
    ├── api.py
    ├── app.py
    ├── content_payload.py
    ├── layout_payload.py
    ├── main.py
    └── payload.py

7 directories, 24 files
```


