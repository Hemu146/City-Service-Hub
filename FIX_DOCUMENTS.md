# Fix: Admin Can't See Documents

## ✅ What I Fixed

1. **Added Media File Configuration** in `settings.py`:
   - `MEDIA_URL = '/media/'`
   - `MEDIA_ROOT = BASE_DIR / 'media'`

2. **Added Media URL Serving** in `urls.py`:
   - Configured Django to serve media files during development

3. **Improved Document Display** in admin dashboard:
   - Better styled document buttons
   - Shows upload date
   - Clearer visual indicators

## 🔄 IMPORTANT: Restart Your Server

**You MUST restart the Django server for these changes to work!**

1. **Stop the current server:**
   - Press `Ctrl + C` in the terminal where the server is running

2. **Start the server again:**
   ```bash
   cd cityservicehub_project
   python3 manage.py runserver
   ```

3. **Now documents will be accessible!**

## 📋 How to View Documents in Admin Dashboard

### Step-by-Step:

1. **Login as Admin:**
   - Go to: `http://127.0.0.1:8000/login/`
   - Email: `admin@cityservicehub.com`
   - Password: `admin123`

2. **Access Admin Dashboard:**
   - You'll be redirected to: `http://127.0.0.1:8000/admin-dashboard/`

3. **View Documents:**
   - Find a pending service card
   - Look for the "Documents:" section
   - You'll see buttons like:
     ```
     📄 Food License
     📄 Working Place Document
     ```
   - **Click on any document button** to view/download

4. **Document Links:**
   - Documents open in a new tab
   - You can view PDFs, images, etc.
   - Download by right-clicking and "Save As"

## 🎯 What You'll See

```
┌─────────────────────────────────────┐
│ Service Name: Tiffin Service        │
│ Type: Tiffin Service                │
│ Provider: John Doe                  │
│                                     │
│ Documents:                          │
│ ┌─────────────────────────────┐   │
│ │ 📄 Food License            │ ← Click here
│ │ Uploaded: Dec 14, 2025     │   │
│ └─────────────────────────────┘   │
│ ┌─────────────────────────────┐   │
│ │ 📄 Working Place Document  │ ← Click here
│ │ Uploaded: Dec 14, 2025     │   │
│ └─────────────────────────────┘   │
│                                     │
│ [Approve] [Reject]                 │
└─────────────────────────────────────┘
```

## 🔍 Troubleshooting

**Still can't see documents?**

1. **Check server is restarted:**
   - Make sure you restarted after the changes

2. **Check document exists:**
   - Verify files are in `service_documents/` folder
   - Check if service has documents uploaded

3. **Check browser console:**
   - Press F12 → Console tab
   - Look for any 404 errors

4. **Verify URL:**
   - Document URLs should start with `/media/service_documents/`
   - Example: `/media/service_documents/food_license.pdf`

## ✅ After Restart

Once you restart the server:
- ✅ Document links will work
- ✅ Clicking documents will open them
- ✅ You can view/download all uploaded files
- ✅ Better styled document buttons

**Restart your server now and try again!** 🚀



