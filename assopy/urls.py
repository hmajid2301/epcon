


from django.conf import settings as dsettings
from django.conf.urls import url, include
from django.contrib.auth.views import (
    login,
    logout,
    password_change,
    password_change_done,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)

from assopy.forms import LoginForm, SetPasswordForm
from assopy import views


urlpatterns = [
    url(r'^login/$',
        login,
        kwargs={'authentication_form': LoginForm},
        name="login"),

    url(r'^logout/$', logout, name="logout"),

    # Password change
    url(r'^password_change/$', password_change, name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        name='password_change_done'),

    # Password reset, using default django views.
    url(r'^password_reset/$', password_reset, name='password_reset'),

    url(r'^password_reset/done/$', password_reset_done,
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[\w-]+)/(?P<token>[\w]{1,13}-[\w]{1,20})/$',
        password_reset_confirm,
        kwargs={'set_password_form': SetPasswordForm},
        name='password_reset_confirm'),

    url(r'^reset/done/$', password_reset_complete,
        name='password_reset_complete'),


    # New account
    url(r'^new-account/$', views.new_account,
        name='assopy-new-account'),
    url(r'^new-account/feedback$', views.new_account_feedback,
        name='assopy-new-account-feedback'),

    # Manage user profile
    url(r'^profile/$', views.profile, name='assopy-profile'),
    url(r'^profile/identities$', views.profile_identities, name='assopy-profile-identities'),
    url(r'^billing/$', views.billing, name='assopy-billing'),
    url(r'^checkout/$', views.checkout, name='assopy-checkout'),
    url(r'^tickets/$', views.tickets, name='assopy-tickets'),

    url(r'^geocode/$', views.geocode, name='assopy-geocode'),

    url(r'orders/(?P<order_id>\d+)/(?P<item_id>\d+)/voucher$', views.voucher, name='assopy-orderitem-voucher'),
    url(r'orders/(?P<order_id>\d+)/(?P<item_id>\d+)/refund$', views.refund, name='assopy-orderitem-refund'),
    url(r'orders/(?P<assopy_id>.+)/completed$', views.order_complete, name='assopy-order-complete'),
    url(r'^paypal/redirect/(?P<code>.+)/$', views.paypal_billing, name='assopy-paypal-redirect'),
    url(r'^paypal/cc/redirect/(?P<code>.+)/$', views.paypal_cc_billing, name='assopy-cc-paypal-redirect'),

    url(r'paypal_return/(?P<code>.+)/$', views.paypal_feedback_ok, name='assopy-paypal-feedback-ok'),
    url(r'^paypal/cancel/(?P<code>.+)/$', views.paypal_cancel, name='assopy-paypal-feedback-cancel'),
    url(r'bank_return/(?P<code>.+)/$', views.bank_feedback_ok, name='assopy-bank-feedback-ok'),

    url(
        r'orders/(?P<order_code>.+)/invoices/(?P<code>.+).html$',
        views.invoice,
        name='assopy-invoice-html',
        kwargs={'mode': 'html'},
    ),
    url(
        r'orders/(?P<order_code>.+)/invoices/(?P<code>.+).pdf$',
        views.invoice,
        name='assopy-invoice-pdf',
        kwargs={'mode': 'pdf'},
    ),

    url(
        r'orders/(?P<order_code>.+)/credit-note/(?P<code>.+).html$',
        views.credit_note,
        name='assopy-credit_note-html',
        kwargs={'mode': 'html'},
    ),
    url(
        r'orders/(?P<order_code>.+)/credit-note/(?P<code>.+).pdf$',
        views.credit_note,
        name='assopy-credit_note-pdf',
        kwargs={'mode': 'pdf'},
    ),
]

if 'paypal.standard.ipn' in dsettings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^paypal/standard-ipn/', include('paypal.standard.ipn.urls')),
    ]

if 'assopy.stripe' in dsettings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^stripe/', include('assopy.stripe.urls')),
    ]
