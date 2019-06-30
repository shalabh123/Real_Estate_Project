from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id)
            if has_contacted:
                messages.error(request, 'Yo have already made an entry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing = listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        #Send_mail
        send_mail(
            'Property_Listing_Entry'
            'There has been an entry for'+ listing + '.Sign into admin panel for more info',
            'ashucrazy77@gmail.com',
            [realtor_email,],
            fail_silently=False 
        )
        messages.success(request, 'Your request has been submitted, A realtor will contact you')
        return redirect('/listings/'+listing_id)