# 🌐 Sitemap & Robots.txt Generator

A modern, fast, GUI-powered tool that generates **sitemap.xml** and **robots.txt** for both **local website folders** and **online websites**.
Built with **CustomTkinter**, **BeautifulSoup**, and **Python’s XML tools**.

---

## ✨ Features

### ✅ **Local Sitemap Generator**

Scans your website folder and builds a clean, structured sitemap:

* Detects `.html` / `.htm` files
* Auto-generates URL paths
* Supports folder and file exclusions
* Adds priority + lastmod fields

---

### 🌍 **Online Sitemap Crawler**

Crawls any website (same domain only), fully automated:

* Respects maximum crawl depth
* Only collects HTML pages
* Smart URL normalization
* Prevents duplicate pages

---

### 🤖 **Automatic robots.txt**

Generates a clean `robots.txt` including:

* Allowed pages
* Disallowed folders
* Disallowed files
* Auto-inserts sitemap URL

---

### 🎨 **Modern GUI**

Powered by **CustomTkinter**:

* Dark theme
* Modern controls
* Clean layout
* Fast, non-blocking thread handling

---

## 📦 Requirements

```
customtkinter
requests
beautifulsoup4
```

Python built-ins (no need to install):
`os`, `xml.etree`, `tkinter`, `datetime`, `threading`, `urllib.parse`

---

## 📥 Installation

### 1. Download / Clone

```sh
git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
cd REPO-NAME
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

---

## ▶️ How to Run

```sh
python main.py
```

The GUI will open automatically.

---

## 🖼️ Screenshots (optional)

<img width="801" height="784" alt="image" src="https://github.com/user-attachments/assets/91f8f4a6-8746-4073-aae0-0adf13cd89cf" />
<img width="786" height="780" alt="image" src="https://github.com/user-attachments/assets/a681d0fa-6900-4cf6-ae84-6036d78931e2" />


---

## 🛠️ How It Works

### Local Mode

1. Select your website folder
2. Enter your base URL
3. Optionally exclude folders / files
4. Generate → outputs:

   * `sitemap.xml`
   * `robots.txt`

### Online Mode

1. Enter website URL
2. Choose crawl depth
3. Generate → outputs:

   * `sitemap.xml`
   * `robots.txt`

---

## 📂 Output Files

### **sitemap.xml**

* Structured
* Human-readable
* Auto-prioritized

### **robots.txt**

* User-agent rules
* Disallowed items
* Automatic sitemap link

---

## 💡 Notes

* Fully safe to use for GitHub-hosted websites
* Works offline for local folders
* Works online with any accessible website

---

## 🐛 Issues / Contributions

Feel free to open issues or PRs!

---

## ⭐ Support

If this project helped you, please give it a star ⭐ on GitHub!
