# SMB Brute Force Script (Batch)

Simple Windows **Batch script** for testing SMB credentials using a password wordlist.
The script attempts to authenticate to a remote machine by iterating through passwords and stops when a valid one is found.

---

## ⚙️ How It Works

1. Prompts the user for:

   * Target IP address
   * Username
   * Password wordlist

2. Reads passwords from the wordlist one by one.

3. Attempts authentication using:

```
net use \\IP /user:USERNAME PASSWORD
```

4. If authentication succeeds:

   * Displays the valid password
   * Disconnects the SMB session
   * Stops the script.

---

## 📋 Requirements

* Windows system
* `net use` command available
* Password wordlist file

---

## 🚀 Usage

Run the script:

```
script.bat
```

Then enter:

```
Enter IP Address:
Enter Username:
Enter Password List:
```

Example:

```
Enter IP Address: 192.168.1.10
Enter Username: admin
Enter Password List: passwords.txt
```

---

## 📂 Example Wordlist

```
123456
password
admin
letmein
qwerty
```

---

## ⚠️ Disclaimer

For **educational purposes and authorized security testing only**.
Do not use on systems without permission.
