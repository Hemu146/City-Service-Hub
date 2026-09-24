# 📋 Step-by-Step Guide: Admin Dashboard & Service Approval

## 🚀 STEP 1: Login as Admin

### Option A: Use Pre-Created Admin Account
1. Open your browser
2. Go to: **http://127.0.0.1:8000/login/**
3. Enter these credentials:
   - **Email:** `admin@cityservicehub.com`
   - **Password:** `admin123`
4. Click **"Login"** button

### Option B: Create New Admin Account
1. Go to: **http://127.0.0.1:8000/register/**
2. Fill the form:
   - **Name:** Admin User
   - **Email:** `admin@test.com` (MUST contain "admin")
   - **Phone:** 1234567890
   - **Password:** your password
   - **Confirm Password:** same password
   - **Address:** Any address
   - **Status:** User (doesn't matter)
   - **Gender:** Any
   - **Photo:** Upload any image
3. Click **"Register"**
4. You'll be automatically redirected to Admin Dashboard

---

## 🎯 STEP 2: Access Admin Dashboard

After logging in with an admin email, you will be **automatically redirected** to:

**URL:** `http://127.0.0.1:8000/admin-dashboard/`

**OR** you can manually navigate to this URL after login.

---

## 📊 STEP 3: View Admin Dashboard

You will see:

### Top Section - Statistics:
```
┌─────────────────────┐  ┌─────────────────────┐
│ Pending Services    │  │ Approved Services   │
│        5            │  │        12           │
└─────────────────────┘  └─────────────────────┘
```

### Main Section - Pending Services List:
Each service card shows:
- ✅ Service Name
- ✅ Service Type (Tiffin, Laundry, Water Supplier, Cook)
- ✅ Provider Name
- ✅ Address
- ✅ Phone Number
- ✅ Price (if set)
- ✅ **Documents** (clickable links to view):
  - Food License
  - Working Place Document
  - etc.
- ✅ **Two Buttons:**
  - 🟢 **"Approve"** button (Green)
  - 🔴 **"Reject"** button (Red)

---

## ✅ STEP 4: Approve a Service

### Detailed Steps:

1. **Review the Service:**
   - Read all service details
   - Check the provider information
   - Verify address and contact details

2. **Review Documents:**
   - Click on document links to view/download
   - Verify all required documents are uploaded
   - Check document authenticity

3. **Click "Approve" Button:**
   - Find the green **"Approve"** button on the service card
   - Click it

4. **Confirm Approval:**
   - A popup will appear: "Approve this service?"
   - Click **"OK"** to confirm

5. **Success:**
   - You'll see: "Service approved!"
   - The page will automatically refresh
   - The service will disappear from pending list
   - Approved count will increase

6. **Verify:**
   - Go to: `http://127.0.0.1:8000/services/`
   - The approved service should now be visible to all users

---

## ❌ STEP 5: Reject a Service (Optional)

If a service doesn't meet requirements:

1. **Click "Reject" Button:**
   - Find the red **"Reject"** button on the service card
   - Click it

2. **Confirm Rejection:**
   - A popup will appear: "Reject and delete this service?"
   - Click **"OK"** to confirm

3. **Service Deleted:**
   - The service will be permanently deleted
   - Page will refresh automatically

---

## 🔍 Visual Flow Diagram

```
┌─────────────────────────────────────────────────┐
│  1. Login with admin email                      │
│     admin@cityservicehub.com / admin123         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  2. Auto-redirect to Admin Dashboard            │
│     /admin-dashboard/                           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  3. View Pending Services                       │
│     - See statistics                            │
│     - Review service cards                      │
│     - Check documents                           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  4. Click "Approve" Button                      │
│     (Green button on service card)              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  5. Confirm in Popup                            │
│     "Approve this service?" → OK                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  6. Service Approved! ✅                        │
│     - Page refreshes                            │
│     - Service appears on public page            │
└─────────────────────────────────────────────────┘
```

---

## 🎬 Quick Demo Steps

**Test the complete flow:**

1. **Login:**
   ```
   URL: http://127.0.0.1:8000/login/
   Email: admin@cityservicehub.com
   Password: admin123
   ```

2. **You'll see Admin Dashboard:**
   ```
   URL: http://127.0.0.1:8000/admin-dashboard/
   ```

3. **Find a pending service card**

4. **Click the green "Approve" button**

5. **Click "OK" in the confirmation popup**

6. **Done!** Service is now approved and visible to users

---

## 🔐 Important Notes

- **Admin Access:** Email must contain "admin" (case-insensitive)
- **Auto-Redirect:** Admins are automatically redirected after login
- **No Pending Services?** Ask a service provider to add a service first
- **Documents:** Always review documents before approving
- **Approved Services:** Appear on `/services/` page for all users

---

## 🆘 Troubleshooting

**Can't see Admin Dashboard?**
- Check: Email contains "admin"
- Solution: Login with `admin@cityservicehub.com`

**No pending services?**
- Service providers need to add services first
- Services are created with `is_approved=False` by default

**Approve button not working?**
- Check browser console for errors
- Make sure you're logged in
- Refresh the page

---

## 📞 Quick Reference

| Action | URL | Button |
|--------|-----|--------|
| Login | `/login/` | Login button |
| Admin Dashboard | `/admin-dashboard/` | Auto-redirect |
| Approve Service | Click "Approve" | Green button |
| View Approved | `/services/` | Browse page |

---

**Ready to approve services? Login now and start reviewing!** 🚀



