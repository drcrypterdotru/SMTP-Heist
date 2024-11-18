# ⚡ SMTP Heist (SMTP Cracker) | GUI PyQt6 🤖

**SMTP Heist Advanced with Custom SMTPHost + Find SMTPHost:** Built with PyQt6 UI, Tracking SMTP Cracked Results (Good/Bad), Report to Telegram, Advanced Custom SMTPHost + Ports with Custom HTML Letter Preview.

## 📷 Screenshots

🌐 **Dashboard (Reported)**  
![Dashboard](https://github.com/drcrypterdotru/SMTP-Heist/blob/main/Screenshot/demo_0.png)

🌐 **Realtime Update**  
![Realtime Update](https://github.com/drcrypterdotru/SMTP-Heist/blob/main/Screenshot/demo_1.png)

🌐 **Settings/Config**  
![Settings/Config](https://github.com/drcrypterdotru/SMTP-Heist/blob/main/Screenshot/demo_2.png)

---
<details>
SMTP Heist is an Open Source tool useful for those trying to crack/pentest SMTP for a Single Host, Multi Host, or Multi Port services. You can modify settings in the UI under the **Settings/Config** tab.

Two main things to discover the host with your email combo:
1. **Target Hostname** of the SMTP Service. - Enter the host of your choice, for example, `smtp.gmail.com`.
2. **Input SMTP Host** 
You can also add more domains and configurations to the **Config.ini** under the line:  
`smtp_subdomain = smtp, smtpout, webmail` [Add More](https://github.com/drcrypterdotru/SMTP-Heist/Sub_SMTP.txt) .

**Support File => Load `*.txt`**  
Your combo file (`list_combo.txt`) must contain the following format:
- `HOST|PORT|EMAIL|PASSWORD` or
- `EMAIL|PASSWORD`.

If your combo list contains `email:password`, replace `:` with `|`. Invalid or empty combos will be skipped automatically.

</details>

## ⚙️ Features

| SMTP Heist v1.0          |
|--------------------------|
| 🔄 Track Report with Good/Failed - Task/Remaining - Progress        |
| ⚙️ Config SMTP Host with 2 Methods + Set your own mail sent Success Result          |
| 🔍 Advanced Discovery Target without Skip |
| 📜 Report Result to Telegram |


## 🚒 Installation

1. Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/drcrypterdotru/SMTP-Heist
cd SMTP-Heist
```
Install the required dependencies:
```bash
python -m pip install -r requirements.txt
# Or
python3 -m pip install -r requirements.txt
```

🚀 How to Run
After installation, launch the application by running:
```bash
python3 Main.py
```

### Run from EXE (No Installation Needed)

You can download and run the **executable** from the [Releases section](https://github.com/drcrypterdotru/SMTP-Heist/releases). No Python installation is required, just **one click** to run. 🎉

---

<div style="text-align: center;">

## Video Usage 
[![Video Usage](https://i.ibb.co/bm2FtCC/SMTP-Heist-Time-0-00-27-06.png)](https://www.youtube.com/watch?v=JezDTo5S_ks)

## More Tools on Forums

Explore our community and connect with us on visit our website for more Tools and Resources!

[![Website](https://drcrypter.ru/data/assets/logo/logo1.png)](https://drcrypter.ru)

---

## 🤝 Contributing

We welcome contributions! Feel free to fork this repository, make enhancements, and open pull requests. Please check the [issues](#) page for ongoing tasks or bug reports.
yi

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

> ⚠️ **Disclaimer**: This tool is for educational purposes only. 🏫 The creator and contributors are not responsible for any misuse or damages caused. Use responsibly, and only on systems you own or have permission for. ✅

---

### 🎉 Enjoy Using SMTP Heist v1.0! 

If you encounter any issues or have questions, feel free to reach out or open an issue on GitHub.
