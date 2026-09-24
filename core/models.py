from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# =====================================================
# SERVICE PROVIDER MODEL
# =====================================================
class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ]
    )
    password = models.CharField(
        max_length=16,
        validators=[MinLengthValidator(6, message="Password must be at least 6 characters.")]
    )
    address = models.TextField()

    def __str__(self):
        return self.name


# =====================================================
# SERVICE MODEL  (MAIN SERVICES IN SYSTEM)
# =====================================================
class Service(models.Model):

    SERVICE_TYPES = [
        ('tiffin', 'Tiffin Service'),
        ('laundry', 'Laundry'),
        ('water', 'Water Supplier'),
        ('cook', 'Cook'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SERVICE_TYPES, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Base service price", default=None)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to="service_images/", blank=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add related_name to avoid clashes
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name="provided_services",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


# =====================================================
# MENU ITEM FOR SERVICE
# =====================================================
class MenuItem(models.Model):
    service = models.ForeignKey(Service, related_name="menu", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} – {self.price}"


# =====================================================
# USERS MODEL
# =====================================================
class Users(models.Model):
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ]
    )
    password = models.CharField(
        max_length=16,
        validators=[MinLengthValidator(6, message="Password must be at least 6 characters.")]
    )
    adress = models.TextField()

    STATUS_CHOICES = [
        ('provider', 'Provider'),
        ('user', 'User'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")

    def __str__(self):
        return self.name


# =====================================================
# MASTER LIST OF SERVICE CATEGORIES (NO CONFLICT NOW)
# =====================================================
class Services(models.Model):
    service_name = models.CharField(max_length=40, unique=True)

    # FIX: add related_name to avoid conflict with Service.provider
    providers = models.ManyToManyField(
        ServiceProvider,
        blank=True,
        related_name="categories"
    )

    def __str__(self):
        return self.service_name


# =====================================================
# SERVICE DOCUMENTS MODEL
# =====================================================
class ServiceDocument(models.Model):
    DOCUMENT_TYPES = [
        ('food_license', 'Food License'),
        ('working_place', 'Working Place Document'),
        ('shop_license', 'Shop License'),
        ('gst_registration', 'GST Registration'),
        ('driving_license', 'Driving License'),
        ('noc_document', 'NOC Document'),
    ]
    
    service = models.ForeignKey(Service, related_name="documents", on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to="service_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service.name} - {self.get_document_type_display()}"


# =====================================================
# USER FAVORITES MODEL
# =====================================================
class Favorite(models.Model):
    user = models.ForeignKey(Users, related_name="favorites", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="favorited_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'service']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.service.name}"


# =====================================================
# SERVICE BOOKING MODEL
# =====================================================
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(Users, related_name="bookings", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="bookings", on_delete=models.CASCADE)

    service_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)

    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name} → {self.service.name} ({self.get_status_display()})"
