# Admin Service Approval Guide

## How to Approve Services as Admin

### Step 1: Create/Login as Admin User

**Option A: Register New Admin Account**
1. Go to: `http://127.0.0.1:8000/register/`
2. Fill in the registration form
3. **Important**: Use an email that contains the word "admin" (e.g., `admin@example.com`, `adminuser@gmail.com`, `myadmin@test.com`)
4. Set status as "User" (admin access is determined by email, not status)
5. Complete registration

**Option B: Login with Existing Admin Account**
1. Go to: `http://127.0.0.1:8000/login/`
2. Enter your admin email and password
3. You will be automatically redirected to the Admin Dashboard

### Step 2: Access Admin Dashboard

After logging in with an admin email, you will be automatically redirected to:
- **URL**: `http://127.0.0.1:8000/admin-dashboard/`

Or you can manually navigate to this URL after logging in.

### Step 3: Review Pending Services

The Admin Dashboard displays:

1. **Statistics Cards**:
   - **Pending Services**: Number of services waiting for approval
   - **Approved Services**: Total number of approved services

2. **Pending Services List**:
   Each pending service card shows:
   - Service Name
   - Service Type (Tiffin, Laundry, Water Supplier, Cook)
   - Provider Name
   - Address
   - Phone Number
   - Price (if set)
   - **Uploaded Documents** (clickable links to view/download):
     - Tiffin Service: Food License, Working Place Document
     - Laundry Service: Shop License, GST Registration
     - Water Supplier: Driving License, NOC Document
     - Cook: Food License

### Step 4: Approve or Reject Services

For each pending service, you have two options:

**✅ Approve Service:**
1. Click the green **"Approve"** button
2. Confirm the action in the popup
3. The service will be marked as approved
4. The service will now appear on the public Services page
5. The page will automatically refresh

**❌ Reject Service:**
1. Click the red **"Reject"** button
2. Confirm the action in the popup
3. The service will be permanently deleted
4. The page will automatically refresh

### Step 5: Verify Approval

After approving a service:
1. Go to: `http://127.0.0.1:8000/services/`
2. The approved service should now be visible to all users
3. Users can search and view the service details

## Important Notes

### Admin Access Requirements
- Admin access is determined by having "admin" in the email address (case-insensitive)
- Example admin emails: `admin@test.com`, `myadmin@gmail.com`, `ADMIN@example.com`
- The user status field doesn't matter for admin access

### Service Approval Workflow
1. **Service Provider** adds a new service → Service is created with `is_approved=False`
2. **Admin** reviews the service and documents → Admin clicks "Approve"
3. **Service** becomes visible to all users → `is_approved=True`
4. **Users** can now see and search for the service

### Document Review
Before approving, make sure to:
- Review all uploaded documents
- Verify document authenticity (click links to view)
- Check that required documents are present based on service type
- Ensure service information is complete and accurate

## Troubleshooting

### Can't Access Admin Dashboard?
- **Check**: Your email must contain "admin" (case-insensitive)
- **Solution**: Register a new account with "admin" in the email, or update an existing user's email

### No Pending Services Showing?
- **Check**: Service providers need to add services first
- **Solution**: Ask a service provider to add a service, then it will appear in pending list

### Services Not Appearing After Approval?
- **Check**: Refresh the services page
- **Check**: Make sure you clicked "Approve" and confirmed
- **Solution**: Check the browser console for any JavaScript errors

## Quick Reference

| Action | URL | Method |
|--------|-----|--------|
| Login | `/login/` | GET/POST |
| Admin Dashboard | `/admin-dashboard/` | GET |
| Approve Service | `/approve-service/<id>/` | POST |
| View Services | `/services/` | GET |

## Example Admin Workflow

```
1. Login with admin@example.com
   ↓
2. Redirected to /admin-dashboard/
   ↓
3. See 5 pending services
   ↓
4. Review first service:
   - Check documents (Food License, Working Place Doc)
   - Verify service details
   - Click "Approve"
   ↓
5. Service approved! (4 pending remaining)
   ↓
6. Repeat for other services
   ↓
7. All services approved → 0 pending, 5 approved
```

---

**Need Help?** Check the main `IMPLEMENTATION_SUMMARY.md` file for more details.



