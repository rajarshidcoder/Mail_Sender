## 📧 Personalized Email Sender  

A Python-based tool to send personalized emails to recipients listed in a CSV file. This script automates email dispatch, allowing for custom messages tailored to each recipient.  

### ✨ Features  
- Reads recipient details from a CSV file  
- Sends personalized emails using SMTP  
- Supports plain text and HTML email formats  
- Secure authentication using environment variables  

### 🛠️ Installation  

1️⃣ **Clone the repository:**  
```bash
git clone https://github.com/rajarshidcoder/Mail_Sender.git
cd Mail_Sender
```   

3️⃣ **Set up environment variables for email credentials:**  
```bash
EMAIL="your-email@example.com"
PASS="your-email-password"
```  

4️⃣ **Run the application:**  

   🔹 **Navigate to the `server` directory:**  
   ```bash
   cd server
   ```  

   🔹 **Create a virtual environment (same for all OS):**  
   ```bash
   python -m venv .venv
   ```  

   🔹 **Activate the virtual environment:**  

   - **For Windows (Command Prompt - cmd):**  
     ```cmd
     .venv\Scripts\activate
     ```  

   - **For Windows (PowerShell):**  
     ```powershell
     .venv\Scripts\Activate.ps1
     ```  

   - **For Windows (Git Bash):**  
     ```bash
     source .venv/Scripts/activate
     ```  

   - **For macOS/Linux (Terminal):**  
     ```bash
     source .venv/bin/activate
     ```  

   🔹 **Install required dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```  

   🔹 **Start the application:**  
   ```bash
   py app.py
   ```  

   🔹 **Open your browser and go to:**  
   ```
   http://localhost:5000
   ```  