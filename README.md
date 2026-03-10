# PDF Unlocker — Free REST API

Strips owner-password restrictions from PDFs without needing the password.  
Built for use with Power Automate + Adobe "Create Tagged PDF" connector.

---

## Deploy to Render.com (Free)

### 1. Push to GitHub
1. Create a new **public** repository on GitHub
2. Upload all files from this folder into the repo

### 2. Deploy on Render
1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repo
4. Set the following:
   - **Name:** pdf-unlocker (or anything you like)
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Click **"Create Web Service"**
6. Wait ~2 minutes for deployment
7. Copy your public URL e.g. `https://pdf-unlocker.onrender.com`

---

## API Usage

### Health Check
```
GET https://your-app.onrender.com/
```

### Unlock PDF
```
POST https://your-app.onrender.com/unlock
Content-Type: application/json

{
  "pdf_base64": "<base64 encoded PDF content>"
}
```

**Response:**
```json
{
  "success": true,
  "pdf_base64": "<base64 encoded unlocked PDF>"
}
```

---

## Power Automate Flow Setup

```
1. HTTP action          → scrape the original PDF from URL
2. HTTP action (POST)   → call /unlock on your Render app
3. Adobe               → "Create Tagged PDF"
4. SharePoint          → Create file
```

### Step 2 — HTTP action settings:
- **Method:** POST
- **URL:** `https://your-app.onrender.com/unlock`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "pdf_base64": "@{body('HTTP')?['$content']}"
}
```

### Step 3 — Adobe "Create Tagged PDF":
- **File Content:**
```
base64ToBinary(body('HTTP_2')?['pdf_base64'])
```

---

## Important Note on Render Free Tier
The free tier **spins down after 15 minutes of inactivity**.  
The first request after inactivity may take ~30 seconds to wake up.  
Subsequent requests are fast. This is fine for Power Automate flows.
