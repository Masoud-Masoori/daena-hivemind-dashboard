import webbrowser

def launch_mobile_dashboard():
    url = "http://localhost:5173/mobile"
    print("Launching mobile dashboard controller...")
    webbrowser.open(url)

if __name__ == "__main__":
    launch_mobile_dashboard()
