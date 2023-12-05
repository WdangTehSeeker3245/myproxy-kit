import tkinter as tk
from tkinter import ttk
import requests

def get_ip_info():
    try:
        # Get IP information from ipinfo.io
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Extract relevant information
        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        location = data.get("loc", "N/A")
        isp = data.get("org", "N/A")  # ISP information

        # Display the information in the GUI
        ip_label.config(text=f"IP: {ip}")
        city_label.config(text=f"City: {city}")
        region_label.config(text=f"Region: {region}")
        country_label.config(text=f"Country: {country}")
        isp_label.config(text=f"ISP: {isp}")
        location_label.config(text=f"Location: {location}")
    except requests.RequestException as e:
        # Handle errors (e.g., no internet connection)
        # ip_label.config(text=f"Error: {str(e)}")
        ip_label.config(text=f"Error")

# Create the main window
root = tk.Tk()
root.title("IP Check App")  # Set the title of the window
root.geometry("400x500")

# Create a big label for the title
title_label = ttk.Label(root, text="IP Check App", font=("Helvetica", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(50, 0))

# Create labels to display information
ip_label = ttk.Label(root, text="IP: N/A")
city_label = ttk.Label(root, text="City: N/A")
region_label = ttk.Label(root, text="Region: N/A")
country_label = ttk.Label(root, text="Country: N/A")
isp_label = ttk.Label(root, text="ISP: N/A")  # ISP label
location_label = ttk.Label(root, text="Location: N/A")

# Create a button to refresh information
refresh_button = ttk.Button(root, text="Refresh", command=get_ip_info)

# Arrange widgets in the grid
ip_label.grid(row=1, column=0, sticky="w", padx=80, pady=(100,0))
city_label.grid(row=2, column=0, sticky="w", padx=80)
region_label.grid(row=3, column=0, sticky="w", padx=80)
country_label.grid(row=4, column=0, sticky="w", padx=80)
isp_label.grid(row=5, column=0, sticky="w", padx=80)  # Add ISP label to the grid
location_label.grid(row=6, column=0, sticky="w", padx=80)
refresh_button.grid(row=7, column=0, sticky="n", padx=80,pady=30)

# Initial request to display information
get_ip_info()

# Run the Tkinter event loop
root.mainloop()
