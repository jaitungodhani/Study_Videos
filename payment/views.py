import datetime

import stripe
from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.response import Response

from account.models import User
from utils.response_handler import ResponseMsg

from .models import StripeCustomer
from .serializers import CreateCheckoutSessionSerializer

# Create your views here.


class PaymentConfig(views.APIView):
    def get(self, request):
        data = {
            "PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            "STUDENT_MONTHLY_PLAN_ID": settings.STUDENT_MONTHLY_PLAN_ID,
            "STUDENT_YEARLY_PLAN_ID": settings.STUDENT_YEARLY_PLAN_ID,
            "FACULTY_MONTHLY_PLAN_ID": settings.FACULTY_MONTHLY_PLAN_ID,
            "FACULTY_YEARLY_PLAN_ID": settings.FACULTY_YEARLY_PLAN_ID,
        }
        response = ResponseMsg(data=data, error=False, message="Payment Config Get Successfully!!")
        return Response(response.response)


class StripeWebHook(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            raise Exception(str(e))
            # Invalid payload

        except stripe.error.SignatureVerificationError as e:
            raise Exception(str(e))
            # Invalid signature

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            # Fetch all the required data from session
            client_reference_id = session.get("customer_email")
            stripe_customer_id = session.get("customer")
            stripe_subscription_id = session.get("subscription")

            # Get the user and create a new StripeCustomer
            user = User.objects.get(email=client_reference_id)

            if user.is_facultyuser:
                user.groups.set("")
                user.groups.add(get_object_or_404(Group, name__iexact="Subscribed Faculty"))
            if user.is_studentuser:
                user.groups.set("")
                user.groups.add(get_object_or_404(Group, name__iexact="Subscribed Student"))

            StripeCustomer.objects.create(
                user=user,
                stripeCustomerId=stripe_customer_id,
                stripeSubscriptionId=stripe_subscription_id,
            )
            print(user.username + " just subscribed.")
        response = ResponseMsg(data={}, error=False, message="Successfully!!")
        return Response(response.response)


class CreateCheckoutSession(views.APIView):
    @swagger_auto_schema(request_body=CreateCheckoutSessionSerializer)
    def post(self, request):
        serializer = CreateCheckoutSessionSerializer(request.data)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        sub_obj = StripeCustomer.objects.filter(user=request.user).first()
        print(sub_obj)
        if sub_obj:
            sub_status = stripe.Subscription.retrieve(
                sub_obj.stripeSubscriptionId,
            )

            if sub_status.status == "active":
                r = ResponseMsg(data={}, error=False, message="Subscription is already exist !!!!")
                return Response(r.response)

            else:
                customer_id = sub_obj.stripeCustomerId
                try:
                    checkout_session = stripe.checkout.Session.create(
                        # customer_email=request.user.email,
                        customer=customer_id,
                        line_items=[
                            {
                                "price": serializer.validated_data["lookup_key"],
                                "quantity": 1,
                            },
                        ],
                        mode="subscription",
                        success_url=serializer.validated_data["success_url"],
                        cancel_url=serializer.validated_data["cancel_url"],
                    )
                    r = ResponseMsg(data={"url": checkout_session.url}, error=False, message="Subscription status !!!!")
                    return Response(r.response)

                except Exception as e:
                    print(e)
                    r = ResponseMsg(data={}, error=True, msg=str(e))
                    return Response(r.response)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                line_items=[
                    {
                        "price": request.data.get("lookup_key"),
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url=request.data.get("success_url"),
                cancel_url=request.data.get("cancel_url"),
            )
            r = ResponseMsg(data={"url": checkout_session.url}, error=False, message="Subscription status !!!!")
            return Response(r.response)

        except Exception as e:
            print(e)
            r = ResponseMsg(data={}, error=True, message=str(e))
            return Response(r.response)


class GetUserActiveSubscriptionDetail(views.APIView):
    def get(self, request):
        try:
            subscripion_obj = StripeCustomer.objects.get(user=request.user)
        except StripeCustomer.DoesNotExist:
            r = ResponseMsg(data={}, error=False, message="No Any Active Subscription found four this User !!!!")
            return Response(r.response)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        data = {
            "subscription_details": {
                "id": None,
                "start_date": None,
                "end_date": None,
                "status": None,
                "plan_name": None,
            },
            "payment_info": {
                "id": None,
                "last4": None,
                "type": None,
                "country": None,
                "funding": None,
                "exp_month": None,
                "exp_year": None,
            },
        }

        subscription_data = stripe.Subscription.retrieve(subscripion_obj.stripeSubscriptionId)

        payment_info = stripe.PaymentMethod.list(
            customer=subscripion_obj.stripeCustomerId,
            type="card",
        )

        data["subscription_details"] = subscription_data
        data["payment_info"] = payment_info

        r = ResponseMsg(data=data, error=False, message="Subscription Details Get !!!!")
        return Response(r.response)
