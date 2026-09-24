from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .forms import UsersForm, LoginForm, ServiceForm, ServicesForm, ServiceProviderProfileForm, UserProfileForm
from .models import Users, ServiceProvider, Service, MenuItem, ServiceDocument, Favorite, Booking


# ================================
#       HOME / BASIC VIEWS
# ================================
def home_view(request):
    recent_services = Service.objects.filter(is_approved=True).select_related('provider')[:6]
    return render(request, "home.html", {"recent_services": recent_services})


def forget_view(request):
    return render(request, "forget.html")


def service_view(request):
    search_query = request.GET.get('search', '')
    city_query = request.GET.get('city', '')
    
    services = Service.objects.filter(is_approved=True).select_related('provider').prefetch_related('menu')
    
    if search_query:
        services = services.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(type__icontains=search_query)
        )
    
    if city_query:
        services = services.filter(address__icontains=city_query)
    
    services_list = []

    # Preload favorites for logged-in user (for heart state on UI)
    favorite_ids = set()
    user_id = request.session.get("user_id")
    if user_id:
        favorite_ids = set(
            Favorite.objects.filter(user_id=user_id, service__in=services)
            .values_list("service_id", flat=True)
        )

    def build_time_slots(open_time, close_time, step_minutes=30):
        """
        Build a list of time slot strings (HH:MM) between open_time and close_time.
        If either is missing, return an empty list and let the template fall back.
        """
        if not open_time or not close_time:
            return []

        slots = []
        # Use arbitrary date; we only care about time portion
        current = datetime.combine(timezone.now().date(), open_time)
        end = datetime.combine(timezone.now().date(), close_time)

        # Avoid infinite loop if close_time <= open_time
        if end <= current:
            return []

        while current < end:
            slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=step_minutes)
        return slots

    for service in services:
        menu_items = [{"name": item.name, "price": item.price} for item in service.menu.all()]
        time_slots = build_time_slots(service.open_time, service.close_time)

        services_list.append({
            "service": service,
            "menu": menu_items,
            "image_url": service.image.url if service.image else None,
            "is_favorite": service.id in favorite_ids,
            "time_slots": time_slots,
        })
    
    return render(request, "service.html", {
        "services": services_list,
        "search_query": search_query,
        "city_query": city_query,
        "favorite_ids": favorite_ids,
    })


# ================================
#        REGISTER VIEW
# ================================
def register_view(request):
    if request.method == "POST":
        form = UsersForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            user = Users.objects.create(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                password=data["password"],
                adress=data["adress"],
                gender=data["gender"],
                status=data["status"],
                photo=data["photo"],
            )

            # SESSION
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            request.session["user_status"] = user.status

            # PROVIDER CREATE PROFILE
            if user.status == "provider":
                provider = ServiceProvider.objects.create(
                    name=user.name,
                    email=user.email,
                    phone=user.phone,
                    password=user.password,
                    address=user.adress,
                )
                request.session["provider_id"] = provider.id
                messages.success(request, "Service Provider Registered Successfully!")
                return redirect("service_provider")

            # NORMAL USER
            messages.success(request, "User Registered Successfully!")
            return redirect("services")

    else:
        form = UsersForm()

    return render(request, "register.html", {"form": form})


# ================================
#          LOGIN VIEW
# ================================
def login_view(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            try:
                user = Users.objects.get(email=email, password=password)
            except Users.DoesNotExist:
                messages.error(request, "Invalid Email or Password")
                return render(request, "login.html", {"form": form})
            
            # SAVE SESSION
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            request.session["user_status"] = user.status
            request.session["email"] = user.email
            request.session["pass"] = user.password
            
            # ADMIN LOGIN
            if "admin" in user.email.lower():
                return redirect("admin_dashboard")
            
            # PROVIDER LOGIN
            if user.status == "provider":
            
                provider = ServiceProvider.objects.filter(email=user.email).first()
                if not provider:
                    provider = ServiceProvider.objects.create(
                        name=user.name,
                        email=user.email,
                        phone=user.phone,
                        password=user.password,
                        address=user.adress,
                    )
                
                request.session["provider_id"] = provider.id
                return redirect("service_provider")
            
            # NORMAL USER LOGIN -> go to user dashboard
            return redirect("user_dashboard")
    
    return render(request, "login.html", {"form": form})


# ================================
#          LOGOUT VIEW
# ================================
def logout_view(request):
    request.session.flush()
    # After logout, go back to home page
    return redirect("home")


# ================================
#          USER DASHBOARD
# ================================
def user_dashboard_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(Users, id=user_id)
    if user.status != "user":
        # Providers/admins should not use user dashboard
        return redirect("service_provider")

    favorites = Favorite.objects.filter(user=user).select_related("service", "service__provider")
    bookings = Booking.objects.filter(user=user).select_related("service", "service__provider")

    # Services list for inline booking section in dashboard
    services = Service.objects.filter(is_approved=True).select_related("provider").prefetch_related("menu")

    favorite_ids = set(
        Favorite.objects.filter(user=user, service__in=services)
        .values_list("service_id", flat=True)
    )

    def build_time_slots(open_time, close_time, step_minutes=30):
        if not open_time or not close_time:
            return []
        slots = []
        current = datetime.combine(timezone.now().date(), open_time)
        end = datetime.combine(timezone.now().date(), close_time)
        if end <= current:
            return []
        while current < end:
            slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=step_minutes)
        return slots

    booking_services = []
    for service in services:
        menu_items = [{"name": item.name, "price": item.price} for item in service.menu.all()]
        time_slots = build_time_slots(service.open_time, service.close_time)
        booking_services.append({
            "service": service,
            "menu": menu_items,
            "image_url": service.image.url if service.image else None,
            "is_favorite": service.id in favorite_ids,
            "time_slots": time_slots,
        })

    profile_form = UserProfileForm(instance=user)

    return render(request, "user_dashboard.html", {
        "user": user,
        "favorites": favorites,
        "bookings": bookings,
        "booking_services": booking_services,
        "profile_form": profile_form,
    })


# ================================
#   UPDATE USER PROFILE (DASHBOARD)
# ================================
def update_user_profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(Users, id=user_id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            # Show a simple combined error message
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f"{field}: {err}")

    return redirect("user_dashboard")


# ================================
#          BOOK SERVICE
# ================================
def book_service(request, service_id):
    if not request.session.get("user_id"):
        return redirect("login")

    user = get_object_or_404(Users, id=request.session.get("user_id"))
    if user.status != "user":
        # Only normal users can book
        return HttpResponse("Only users can book services.", status=403)

    service = get_object_or_404(Service, id=service_id, is_approved=True)

    if request.method == "POST":
        date_str = request.POST.get("service_date", "").strip()
        time_slot = request.POST.get("time_slot", "").strip()
        quantity_str = request.POST.get("quantity", "").strip() or "1"
        note = request.POST.get("note", "").strip()

        errors = []
        service_date = None

        if not date_str:
            errors.append("Please select a service date.")
        else:
            try:
                service_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
                if service_date < timezone.now().date():
                    errors.append("Service date cannot be in the past.")
            except ValueError:
                errors.append("Invalid date format.")

        if not time_slot:
            errors.append("Please select a time slot.")

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                errors.append("Quantity must be at least 1.")
        except ValueError:
            errors.append("Invalid quantity.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return redirect("services")

        Booking.objects.create(
            user=user,
            service=service,
            service_date=service_date,
            time_slot=time_slot,
            quantity=quantity,
            note=note or "",
        )
        messages.success(request, "Service booked successfully!")
        return redirect("user_dashboard")

    return redirect("services")


# ================================
#    USER CANCEL BOOKING
# ================================
def cancel_booking(request, booking_id):
    if not request.session.get("user_id"):
        return redirect("login")

    booking = get_object_or_404(Booking, id=booking_id, user_id=request.session["user_id"])

    if booking.status not in ["pending", "accepted"]:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect("user_dashboard")

    booking.status = "cancelled"
    booking.save(update_fields=["status", "updated_at"])
    messages.success(request, "Booking cancelled successfully.")
    return redirect("user_dashboard")


# ================================
#  SERVICE PROVIDER DASHBOARD VIEW
# ================================
def service_provider_view(request):

    if not request.session.get("user_id"):
        return redirect("login")

    if request.session.get("user_status") != "provider":
        return HttpResponse("You are not service provider")

    provider = get_object_or_404(ServiceProvider, id=request.session.get("provider_id"))

    user = Users.objects.filter(email=provider.email).first()

    services = Service.objects.filter(provider=provider).prefetch_related('menu')

    # ============================
    # Provider statistics (services)
    # ============================
    total_services = services.count()
    approved_services = services.filter(is_approved=True).count()
    pending_services = services.filter(is_approved=False).count()

    # ============================
    # Provider statistics (bookings)
    # ============================
    provider_bookings = Booking.objects.filter(service__provider=provider).select_related("service", "user")
    total_bookings = provider_bookings.count()
    pending_bookings = provider_bookings.filter(status="pending").count()
    accepted_bookings = provider_bookings.filter(status="accepted").count()
    completed_bookings = provider_bookings.filter(status="completed").count()

    # Count services by type for chart (only non-empty types)
    services_by_type_qs = (
        services.exclude(type__isnull=True)
        .exclude(type__exact="")
        .values("type")
        .annotate(total=Count("id"))
    )

    # Map type codes to human labels using model choices
    type_display_map = dict(Service.SERVICE_TYPES) if hasattr(Service, "SERVICE_TYPES") else {}
    chart_labels = []
    chart_values = []
    for row in services_by_type_qs:
        code = row["type"]
        label = type_display_map.get(code, code or "Unknown")
        chart_labels.append(label)
        chart_values.append(row["total"])

    services_data = []
    for service in services:
        menu_items = [{"name": item.name, "price": item.price} for item in service.menu.all()]
        services_data.append({
            "id": service.id,
            "name": service.name,
            "type": service.type,
            "description": service.description or "",
            "address": service.address or "",
            "phone": service.phone or "",
            "open_time": service.open_time.strftime("%H:%M") if service.open_time else "",
            "close_time": service.close_time.strftime("%H:%M") if service.close_time else "",
            "image": {"url": service.image.url} if service.image else None,
            "menu": menu_items
        })

    return render(request, "service_provider.html", {
        "provider": provider,
        "user": user,
        "services": services,
        "services_json": json.dumps(services_data),
        "addservice": ServiceForm(),
        "total_services": total_services,
        "approved_services": approved_services,
        "pending_services": pending_services,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "accepted_bookings": accepted_bookings,
        "completed_bookings": completed_bookings,
        "provider_bookings": provider_bookings,
        "chart_labels": json.dumps(chart_labels),
        "chart_values": json.dumps(chart_values),
    })


# ================================
#       ADD SERVICE
# ================================
def add_service(request):
    if not request.session.get("provider_id"):
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            service = form.save(commit=False)

            provider = get_object_or_404(ServiceProvider, id=request.session.get("provider_id"))
            service.provider = provider
            service.save()

            # MENU ITEMS
            names = request.POST.getlist("menu_name")
            prices = request.POST.getlist("menu_price")

            for n, p in zip(names, prices):
                if n.strip():
                    MenuItem.objects.create(service=service, name=n.strip(), price=p.strip())

            # DOCUMENT HANDLING
            doc_map = {
                'tiffin': ['food_license', 'working_place'],
                'laundry': ['shop_license', 'gst_registration'],
                'water': ['driving_license', 'noc_document'],
                'cook': ['food_license'],
            }

            for doc_type in doc_map.get(service.type, []):
                file_obj = request.FILES.get(f'document_{doc_type}')
                if file_obj:
                    ServiceDocument.objects.create(
                        service=service,
                        document_type=doc_type,
                        document_file=file_obj
                    )

            return JsonResponse({"success": True, "message": "Service added successfully"})

        # Form invalid -> return JSON with errors for AJAX frontend
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return redirect("service_provider")


# ================================
#       EDIT SERVICE
# ================================
def edit_service(request, id):
    if not request.session.get("provider_id"):
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    service = get_object_or_404(Service, id=id)

    if service.provider.id != request.session.get("provider_id"):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            form.save()

            # DELETE OLD MENU
            MenuItem.objects.filter(service=service).delete()

            # ADD NEW MENU
            names = request.POST.getlist("menu_name")
            prices = request.POST.getlist("menu_price")

            for n, p in zip(names, prices):
                if n.strip():
                    MenuItem.objects.create(service=service, name=n.strip(), price=p.strip())

            return JsonResponse({"success": True, "message": "Service updated successfully"})

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # GET → return JSON data
    menu_items = [{"name": item.name, "price": item.price} for item in service.menu.all()]
    return JsonResponse({
        "success": True,
        "service": {
            "id": service.id,
            "name": service.name,
            "type": service.type,
            "price": str(service.price) if service.price else "",
            "description": service.description,
            "address": service.address,
            "phone": service.phone,
            "open_time": service.open_time.strftime("%H:%M") if service.open_time else "",
            "close_time": service.close_time.strftime("%H:%M") if service.close_time else "",
            "image_url": service.image.url if service.image else "",
            "menu": menu_items
        }
    })


# ================================
#       DELETE SERVICE
# ================================
def delete_service(request, id):
    if not request.session.get("provider_id"):
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    service = get_object_or_404(Service, id=id)

    if service.provider.id != request.session.get("provider_id"):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

    service.delete()
    return JsonResponse({"success": True, "message": "Service deleted successfully"})


# ================================
#  UPDATE SERVICE PROVIDER PROFILE
# ================================
def update_provider_profile(request):
    if not request.session.get("provider_id"):
        return redirect("login")

    provider = get_object_or_404(ServiceProvider, id=request.session.get("provider_id"))

    if request.method == "POST":
        form = ServiceProviderProfileForm(request.POST, instance=provider)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Profile updated successfully"})

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return redirect("service_provider")



# ================================
#        ADMIN DASHBOARD
# ================================
def admin_dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(Users, id=user_id)

    if "admin" not in user.email.lower():
        return HttpResponse("Access Denied. Admin only.", status=403)

    search_query = request.GET.get("q", "").strip()

    pending_services = Service.objects.filter(is_approved=False)
    approved_count = Service.objects.filter(is_approved=True).count()

    user_list = Users.objects.all()
    provider_list = ServiceProvider.objects.all()
    bookings = Booking.objects.select_related("service", "user").order_by("-created_at")

    if search_query:
        # Filter users by name only
        user_list = user_list.filter(
            models.Q(name__icontains=search_query)
        )

        # Filter providers by name only
        provider_list = provider_list.filter(
            models.Q(name__icontains=search_query)
        )

        # Filter pending services by service name OR provider name
        pending_services = pending_services.filter(
            models.Q(name__icontains=search_query) |
            models.Q(provider__name__icontains=search_query)
        )

        # Filter bookings by user name OR service name
        bookings = bookings.filter(
            models.Q(user__name__icontains=search_query) |
            models.Q(service__name__icontains=search_query)
        )

    # Limit bookings list to latest 20 after filtering
    bookings = bookings[:20]

    return render(request, "admin_dashboard.html", {
        "pending_services": pending_services,
        "approved_count": approved_count,
        "pending_count": pending_services.count(),
        "user_count": user_list.count(),
        "provider_count": provider_list.count(),
        "total_bookings": Booking.objects.count(),
        "user_list": user_list,
        "provider_list": provider_list,
        "bookings": bookings,
        "search_query": search_query,
    })


# ================================
#   PROVIDER BOOKING STATUS UPDATE
# ================================
def update_booking_status(request, booking_id):
    if not request.session.get("provider_id"):
        return redirect("login")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        service__provider_id=request.session["provider_id"],
    )

    if request.method != "POST":
        return redirect("service_provider")

    action = request.POST.get("action")

    if action == "accept" and booking.status == "pending":
        booking.status = "accepted"
    elif action == "reject" and booking.status in ["pending", "accepted"]:
        booking.status = "rejected"
    elif action == "complete" and booking.status in ["accepted"]:
        booking.status = "completed"
    else:
        messages.error(request, "Invalid status change.")
        return redirect("service_provider")

    booking.save(update_fields=["status", "updated_at"])
    messages.success(request, "Booking status updated.")
    return redirect("service_provider")


# ================================
#     APPROVE / REJECT SERVICE
# ================================
def approve_service(request, id):
    if not request.session.get("user_id"):
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    user = get_object_or_404(Users, id=request.session.get("user_id"))
    if "admin" not in user.email.lower():
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

    service = get_object_or_404(Service, id=id)
    action = request.POST.get("action", "approve")

    if action == "approve":
        service.is_approved = True
        service.save()
        return JsonResponse({"success": True, "message": "Service approved"})

    if action == "reject":
        service.delete()
        return JsonResponse({"success": True, "message": "Service rejected & deleted"})

    return JsonResponse({"success": False, "error": "Invalid action"})


# ================================
#     ADD / REMOVE FAVORITE
# ================================
def toggle_favorite(request, service_id):
    if not request.session.get("user_id"):
        return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)

    user = get_object_or_404(Users, id=request.session.get("user_id"))
    service = get_object_or_404(Service, id=service_id)

    from .models import Favorite
    favorite, created = Favorite.objects.get_or_create(user=user, service=service)

    if not created:
        favorite.delete()
        return JsonResponse({"success": True, "is_favorite": False, "message": "Removed from favorites"})

    return JsonResponse({"success": True, "is_favorite": True, "message": "Added to favorites"})
