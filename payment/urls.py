from django.urls import path, include
from .views import PaymentConfig, StripeWebHook, CreateCheckoutSession, GetUserActiveSubscriptionDetail

urlpatterns = [
    path("payment/payment_config/", PaymentConfig.as_view()),
    path("payment/webhook/", StripeWebHook.as_view()),
    path("payment/create_checkout_session/", CreateCheckoutSession.as_view()),
    path("payment/getuseractivesubscriptiondetails/", GetUserActiveSubscriptionDetail.as_view()),
]
