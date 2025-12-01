import os
import xml.etree.ElementTree as ET
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ------------------------------
# Modern Sitemap & Robots Generator
# ------------------------------

def generate_local_sitemap(website_folder, base_url, excluded_folders, excluded_files, output_folder):
    urls = []

    for root, _, files in os.walk(website_folder):
        rel_root = os.path.relpath(root, website_folder).replace("\\", "/")

        if any(excl.strip().lower() in rel_root.lower() for excl in excluded_folders if excl.strip()):
            continue

        for file in files:
            if not file.endswith((".html", ".htm")):
                continue
            if any(file.lower() == excl.strip().lower() for excl in excluded_files if excl.strip()):
                continue

            rel_path = os.path.join(rel_root, file).replace("\\", "/")
            if rel_path == ".":
                rel_path = file

            url_path = rel_path.replace("index.html", "").replace(".html", "")
            if not url_path.startswith("/"):
                url_path = "/" + url_path

            urls.append(f"{base_url.rstrip('/')}{url_path}")

    urls = sorted(set(urls))
    return save_sitemap(urls, output_folder)


def generate_online_sitemap(start_url, max_depth, output_folder):
    visited = set()
    urls = []

    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)
        try:
            response = requests.get(url, timeout=6)
            if "text/html" not in response.headers.get("Content-Type", ""):
                return
            soup = BeautifulSoup(response.text, "html.parser")
            urls.append(url)
            for a in soup.find_all("a", href=True):
                next_url = urljoin(url, a["href"])
                if urlparse(next_url).netloc == urlparse(start_url).netloc:
                    crawl(next_url.split("#")[0], depth + 1)
        except Exception:
            pass

    crawl(start_url.rstrip("/"), 0)
    return save_sitemap(sorted(set(urls)), output_folder)


def save_sitemap(urls, output_folder):
    urlset = ET.Element("urlset", {
        "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xmlns:xhtml": "http://www.w3.org/1999/xhtml"
    })

    for url in urls:
        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = url
        ET.SubElement(url_el, "priority").text = str(round(max(0.4, 1.0 - url.count("/") * 0.1), 1))
        ET.SubElement(url_el, "lastmod").text = datetime.now().strftime("%Y-%m-%d")

    sitemap_path = os.path.join(output_folder, "sitemap.xml")

    indent_xml(urlset)
    tree = ET.ElementTree(urlset)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    return sitemap_path


def indent_xml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def generate_robots(base_url, excluded_folders, excluded_files, output_folder):
    robots_path = os.path.join(output_folder, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\n")

        if excluded_folders:
            f.write("# Disallowed folders\n")
            for folder in excluded_folders:
                folder = folder.strip()
                if folder:
                    if not folder.startswith("/"):
                        folder = "/" + folder
                    if not folder.endswith("/"):
                        folder += "/"
                    f.write(f"Disallow: {folder}\n")

        if excluded_files:
            f.write("\n# Disallowed files\n")
            for file in excluded_files:
                file = file.strip()
                if file:
                    if not file.startswith("/"):
                        file = "/" + file
                    f.write(f"Disallow: {file}\n")

        f.write(f"\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n")

    return robots_path


# ------------------------------
# UI Class
# ------------------------------
class ModernSitemapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sitemap & Robots Generator")
        self.geometry("750x720")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.mode_var = ctk.StringVar(value="local")

        # --- Layout Container ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Header ---
        ctk.CTkLabel(self.main_frame, text="Sitemap & Robots.txt Generator", font=("Segoe UI Semibold", 22)).pack(pady=(10, 5))
        ctk.CTkLabel(self.main_frame, text="Generate readable sitemaps for local or online websites.", text_color="gray").pack(pady=(0, 15))

        # --- Mode Selector ---
        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.pack(pady=5)
        ctk.CTkRadioButton(self.mode_frame, text="Local Folder", variable=self.mode_var, value="local", command=self.update_mode).pack(side="left", padx=20)
        ctk.CTkRadioButton(self.mode_frame, text="Online Website", variable=self.mode_var, value="online", command=self.update_mode).pack(side="left", padx=20)

        # --- Dynamic Options Container ---
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.pack(pady=(15, 10), fill="x")

        # --- Local Frame ---
        self.local_frame = ctk.CTkFrame(self.options_frame)
        self.path_entry = ctk.CTkEntry(self.local_frame, width=500, placeholder_text="Select your website folder...")
        self.path_entry.grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(self.local_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1, pady=5)
        ctk.CTkLabel(self.local_frame, text="Base URL (e.g. https://example.com):").grid(row=1, column=0, columnspan=2, pady=(10, 5))
        self.base_url_entry = ctk.CTkEntry(self.local_frame, width=500)
        self.base_url_entry.insert(0, "https://example.com")
        self.base_url_entry.grid(row=2, column=0, columnspan=2)

        # --- Online Frame ---
        self.online_frame = ctk.CTkFrame(self.options_frame)
        ctk.CTkLabel(self.online_frame, text="Website URL (e.g. https://example.com):").pack(pady=(5, 5))
        self.site_url_entry = ctk.CTkEntry(self.online_frame, width=500)
        self.site_url_entry.pack(pady=5)
        ctk.CTkLabel(self.online_frame, text="Max Crawl Depth:").pack(pady=(10, 5))
        self.depth_slider = ctk.CTkSlider(self.online_frame, from_=1, to=4, number_of_steps=3, width=300)
        self.depth_slider.set(2)
        self.depth_slider.pack(pady=(0, 10))

        # --- Exclusions ---
        ctk.CTkLabel(self.main_frame, text="Exclude Folders (comma-separated):").pack(pady=(10, 5))
        self.excl_folders_entry = ctk.CTkEntry(self.main_frame, width=500)
        self.excl_folders_entry.insert(0, "admin, Components, downloads, discord-api, OLD, unreleased")
        self.excl_folders_entry.pack()

        ctk.CTkLabel(self.main_frame, text="Exclude Files (comma-separated):").pack(pady=(20, 5))
        self.excl_files_entry = ctk.CTkEntry(self.main_frame, width=500)
        self.excl_files_entry.insert(0, "404.html, thankyou.html, README.md")
        self.excl_files_entry.pack()

        # --- Generate Button ---
        ctk.CTkButton(self.main_frame, text="Generate Sitemap & Robots.txt", width=250, height=45, command=self.start_generation).pack(pady=30)

        # --- Loading / Status Label ---
        self.loading_label = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 13))
        self.loading_label.pack()

        # --- Footer ---
        ctk.CTkLabel(self.main_frame, text="Open-source | Local or Online | Safe for GitHub", text_color="gray", font=("Segoe UI", 11)).pack(side="bottom", pady=10)

        # Initialize mode visibility
        self.update_mode()

    def update_mode(self):
        for widget in self.options_frame.winfo_children():
            widget.pack_forget()
        if self.mode_var.get() == "local":
            self.local_frame.pack(pady=5)
        else:
            self.online_frame.pack(pady=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def start_generation(self):
        threading.Thread(target=self.generate, daemon=True).start()
        self.loading_label.configure(text="⏳ Generating, please wait...", text_color="orange")

    def generate(self):
        try:
            mode = self.mode_var.get()
            excluded_folders = [f.strip() for f in self.excl_folders_entry.get().split(",")]
            excluded_files = [f.strip() for f in self.excl_files_entry.get().split(",")]
            output_folder = os.getcwd()

            if mode == "local":
                folder = self.path_entry.get().strip()
                base_url = self.base_url_entry.get().strip()
                if not os.path.isdir(folder):
                    messagebox.showerror("Error", "Please select a valid local folder.")
                    return
                sitemap_path = generate_local_sitemap(folder, base_url, excluded_folders, excluded_files, output_folder)
                robots_path = generate_robots(base_url, excluded_folders, excluded_files, output_folder)
            else:
                site_url = self.site_url_entry.get().strip()
                if not site_url.startswith("http"):
                    messagebox.showerror("Error", "Enter a valid site URL (https://...).")
                    return
                sitemap_path = generate_online_sitemap(site_url, int(self.depth_slider.get()), output_folder)
                robots_path = generate_robots(site_url, [], [], output_folder)

            self.loading_label.configure(
                text=f"✅ Done! Files created in:\n{output_folder}\n\n• sitemap.xml\n• robots.txt",
                text_color="lightgreen"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
            self.loading_label.configure(text="", text_color="white")


if __name__ == "__main__":
    app = ModernSitemapApp()
    app.mainloop()