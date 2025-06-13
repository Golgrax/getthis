# getthis

ME

    sudo apt-get update && sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

    python3 -m venv venv --system-site-packages

    source venv/bin/activate

    pip install -r requirements.txt

WINDOWS

    Install Python from python.org (ensure "Add to PATH" is checked).

    Install WebView2 from Microsoft's site if needed.

    cmdprompt

    python -m venv venv

    .\venv\Scripts\activate

    pip install -r requirements.txt

BUILD


    python build_payload.py

    python admin_build_payload.py

RUN

    (source venv/bin/activate or .\venv\Scripts\activate).

    python -m shop_app.main

Run the Admin

    python -m admin_app.admin_main