from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from userData.forms import UserForm, UserDetailsInfoForm
from django.contrib.auth import authenticate, login, logout, get_user
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userProfile.models import UserRides, UserProfile
from userData.models import *
from django.utils import timezone
import requests
from datetime import datetime as dt
from django.core.mail import send_mail
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

def sendSMS(mobile,message):
	import requests
	
	url = "https://www.fast2sms.com/dev/bulk"

	payload = "sender_id=FSTSMS&message=" + str(message) + "&language=english&route=p&numbers=" + str(mobile)

	headers = {
	'authorization': "GJDP4jol0eRvyAZU5bFnENL9H83sdr1TI7qzkVBMiSQpKuhwcfrq34RA1MftjQLzOJZI9dhUXbHkg0Pw",
	'Content-Type': "application/x-www-form-urlencoded",
	'Cache-Control': "no-cache",
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	return response.json()

def hashCode(text):
	import hashlib
	return str(hashlib.md5(text.encode()).hexdigest())

@login_required
def confirmTransaction(request,sender,receiver,amount):
	if request.method == "POST":
		username = request.user.get_username()
		password = request.POST['Password']
		data = WalletMapping.objects.get(name=username).password
		if hashCode(password) == data:
			public = WalletMapping.objects.get(name=username).public
			private = WalletMapping.objects.get(name=username).private
			
			history = WalletHistory.objects.create(sender=sender)
			history.sid = 1
			history.receiver = receiver
			history.amount = amount
			history.date = str(dt.now())
			history.save()

			messages.info(request, 'Transaction successful!')
			return HttpResponseRedirect('/faq')
		else:
			messages.info(request, 'Invalid Password!')
			return HttpResponseRedirect('/wallet')
	return render(request, 'confirmTransaction.html')

def landingPage(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']

		send_mail(
			subject,
			message,
			email,
			['masihulla17@gmail.com'],
			fail_silently=False,
		)
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def services(request):
	return render(request, 'services.html')

def forgotPassword(request,username,hash_):
	if len(hash_) < 25:
		raise Http404("Page doesn\'t exists!!")
		
	if request.method == 'POST':
		auth = request.POST['authentication']
		if auth != "mpin":
			p1 = request.POST['p1']
			p2 = request.POST['p2']
			if p1!=p2:
				return render(request, 'forgotpassword.html', {'message2':'Passwords didn\'t match!!'})		
			elif p1=='' or p2=='':
				return render(request, 'forgotpassword.html', {'message2':'Password can\'t be empty!!'})		
			else:
				user = User.objects.get(username=username)
				user.set_password(p1)
				user.save()
				messages.info(request, 'Password has been changed successfully! Login now.')
				return HttpResponseRedirect('/userData/login/')
		else:
			m1 = request.POST['m1']
			m2 = request.POST['m2']
			if m1!=m2:
				return render(request, 'forgotpassword.html', {'message2':'mPins didn\'t match!!'})		
			elif m1=='' or m2=='':
				return render(request, 'forgotpassword.html', {'message2':'mPin can\'t be empty!!'})		
			else:
				user = UserDetailsInfo.objects.get(username=username)
				user.mPin = m1
				user.save()
				messages.info(request, 'mPin has been changed successfully! Login now.')
				return HttpResponseRedirect('/userData/login/')
	return render(request, 'forgotpassword.html')

@login_required
def closeContacts(request):
	username = request.user.get_username()
	try:
		cc = CloseContacts.objects.get(username=username)
	except CloseContacts.DoesNotExist:
		cc = None

	if request.method == 'POST':
		if cc == None:
			cc = CloseContacts.objects.create(username=username)
		cc.cc1 = request.POST['cc1']
		cc.cc2 = request.POST['cc2']
		cc.cc3 = request.POST['cc3']
		cc.cc4 = request.POST['cc4']
		cc.cc5 = request.POST['cc5']
		cc.save()
		return redirect('/dashboard/')	
	return render(request, 'close_contacts.html', {'cc':cc})

def welcomeAnimation(request):
	return render(request, 'welcomeAnimation.html')

@login_required
def scheduleRide(request):
	if request.method == 'POST':
		s = request.POST['source']	
		e = request.POST['destination']
		t = request.POST['time']
		print(request.POST)
		schedule = Scheduled_Rides.objects.create(username=request.user.get_username(), source = s, destination = e, dateTime=t)
		schedule.save()

	schedules = Scheduled_Rides.objects.filter(username=request.user.get_username())
	return render(request, "scheduled_rides.html", {"schedules" : schedules})

@login_required
def bargaining(request,price):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	mapping = {"-5":-5,"-10":-10,"-50":-50,"5":5,"10":10,"50":50}
	priceBargain = UserRides.objects.filter(driverId=price, isDone = False)[0]
	bargain = priceBargain.bargain.split(",")[0]
	bargain = int(bargain.split(" ")[1])
	if request.method == "POST":
		keys = list(request.POST.keys())
		if isDriver:
			priceBargain.bargain = priceBargain.bargain + "0 " + mapping[keys[1]] + ","
		else:
			priceBargain.bargain = priceBargain.bargain + "1 " + mapping[keys[1]] + ","
		priceBargain.save()
		return redirect('/bargain/' + str(price) + "/")
	return render(request, 'bargaining.html',{'isDriver':isDriver,'price':bargain, "driverId" : price, "customer" : priceBargain.username})

@csrf_exempt
def setBargain(request):
	if request.method == "POST":
		data = request.POST
		price = data['price']
		isDriver = data['isDriver']
		driverId = data['driverId']
		priceBargain = UserRides.objects.filter(driverId=driverId, isDone = False)[0]
		if isDriver == "True":
			priceBargain.bargain = priceBargain.bargain + "0 " + price + ","
		else:
			priceBargain.bargain = priceBargain.bargain + "1 " + price + ","
		priceBargain.save()
	return HttpResponse("OK")

@csrf_exempt
def getBargain(request):
	if request.method == "POST":
		data = request.POST
		pricy = data['price']
		isDriver = data['isDriver']
		driverId = data['driverId']
		priceBargain = UserRides.objects.filter(driverId=driverId, isDone = False)[0]
		pricesUpdated = []
		p = priceBargain.bargain.split(",")
		if len(p) > 10:
			pricesUpdated.append("Done")
			pricesUpdated.append(str(p[-2].split(" ")[1]))
		else:
			p = p[-2].split(" ")[1]
			pricesUpdated.append(p)
			if isDriver == "True":
				bargain = priceBargain.bargain.split(",")
				for price in reversed(bargain):
					price = price.split(" ")
					if price[0] != '' and price[1] == pricy:
						break
					elif price[0] == "1" and price[1] != pricy:
						pricesUpdated.append(int(price[1]))
			else:
				bargain = priceBargain.bargain.split(",")
				for price in reversed(bargain):
					price = price.split(" ")
					if price[0] != '' and price[1] == pricy:
						break
					elif price[0] == "0" and  price[1] != pricy:
						pricesUpdated.append(int(price[1]))		
	return HttpResponse(json.dumps(pricesUpdated[::-1]), content_type='application/json')

@csrf_exempt
def agreeRide(request):
	if request.method == "POST":
		data = request.POST
		price = data['price']
		isDriver = data['isDriver']
		driverId = data['driverId']
		priceBargain = UserRides.objects.filter(driverId=driverId, isDone = False)[0]
		if isDriver == "True":
			priceBargain.driverAgreed = True
		else:
			priceBargain.customerAgreed = True
		priceBargain.amount = int(price)
		priceBargain.save()
	return HttpResponse("OK")

@csrf_exempt
def disagreeRide(request):
	if request.method == "POST":
		data = request.POST
		price = data['price']
		isDriver = data['isDriver']
		driverId = data['driverId']
		priceBargain = UserRides.objects.filter(driverId=driverId, isDone = False)[0]
		if isDriver == "True":
			priceBargain.driverAgreed = False
		else:
			priceBargain.customerAgreed = False
		priceBargain.save()
		if (not priceBargain.driverAgreed and not priceBargain.customerAgreed):
			priceBargain.delete()
	return HttpResponse("OK")

@csrf_exempt
def checkAgreeRide(request):
	if request.method == "POST":
		data = request.POST
		driverId = data['driverId']
		priceBargain = UserRides.objects.filter(driverId=driverId, isDone = False)[0]
		if priceBargain.driverAgreed and priceBargain.customerAgreed :
			return HttpResponse("True")
		else:
			return HttpResponse("False")

@login_required
def dashboard(request):
	username = request.user.get_username()
	try:
		numRides = len(UserRides.objects.filter(username=username))
		cc = CloseContacts.objects.get(username=username)
		count = -2
		for field in cc._meta.fields:
			if field.value_from_object(cc) != '':
				count += 1
	except UserRides.DoesNotExist:
		numRides = 0
	except CloseContacts.DoesNotExist:
		count = 0
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	return render(request, 'dashboard.html', {'Totalrides' : numRides,'walletBalance':100,'closeContacts':count, "isDriver" : isDriver})

@login_required
def user(request):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver

	try:
		details = UserProfile.objects.get(Username=username)
	except UserProfile.DoesNotExist:
		details = None
		return render(request, 'user.html',{'isDriver':isDriver})

	if request.method == "POST":
		details.Username = request.POST['PhoneNumber']
		details.EmailAddress = request.POST['EmailAddress']
		details.FirstName = request.POST['FirstName']
		details.LastName = request.POST['LastName']
		details.Address = request.POST['Address']
		details.City = request.POST['City']
		details.Country = request.POST['Country']
		details.PostalCode = request.POST['PostalCode']
		if len(request.FILES) != 0:
			details.ProfilePic = request.FILES['ProfilePic']
		details.save()
		details = UserProfile.objects.get(Username=username)

	if details.ProfilePic == None or details.ProfilePic == '':
		return render(request, 'user.html',{'PhoneNumber':details.Username,'EmailAddress':details.EmailAddress,'FirstName':details.FirstName,'LastName':details.LastName,'Address':details.Address,'City':details.City,'Country':details.Country,'PostalCode':details.PostalCode,'ProfilePic':None,'isDriver':isDriver})	
	else:
		return render(request, 'user.html',{'PhoneNumber':details.Username,'EmailAddress':details.EmailAddress,'FirstName':details.FirstName,'LastName':details.LastName,'Address':details.Address,'City':details.City,'Country':details.Country,'PostalCode':details.PostalCode,'ProfilePic':details.ProfilePic.url,'isDriver':isDriver})

	

@login_required
def wallet(request):
	username = request.user.get_username()
	try:
		data = WalletHistory.objects.filter(Q(sender=username) | Q(receiver=username))
		data = data.order_by('-date')
	except WalletHistory.DoesNotExist:
		data = None
	if request.method == "POST":
		sender = request.POST['PhoneNumber']
		receiver = request.POST['Receiver']
		amount = request.POST['Amount']
		if amount !='' and receiver != '':
			return redirect('/confirmTransaction/' + str(sender) + "/" + str(receiver) + "/" + str(amount) + "/" )
		else:
			messages.info(request, 'Fill in the empty details!')
			return HttpResponseRedirect('/wallet')
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	return render(request, 'wallet.html', {'PhoneNumber':username,'data':data, "isDriver" : isDriver})

@login_required
def pay(request, driver, amount):
	username = request.user.get_username()
	try:
		data = WalletHistory.objects.filter(Q(sender=username) | Q(receiver=username))
		data = data.order_by('-date')
	except WalletHistory.DoesNotExist:
		data = None
	if request.method == "POST":
		sender = request.POST['PhoneNumber']
		receiver = request.POST['Receiver']
		amount = request.POST['Amount']
		if amount !='' and receiver != '':
			return redirect('/confirmTransaction/' + str(sender) + "/" + str(receiver) + "/" + str(amount) + "/" )
		else:
			messages.info(request, 'Fill in the empty details!')
			return HttpResponseRedirect('/wallet')
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	return render(request, 'wallet.html', {'PhoneNumber':username,'data':data, "isDriver" : isDriver, "Receiver" : driver, "Amount" : amount})

@login_required
def security(request):
	return render(request, 'user.html')

@login_required
def addingStops(request, source, destination):
	if request.method == "POST":
		ride = UserRides.objects.get(username=request.user.get_username(), source=source, destination=destination)
		try:
			stop1 = request.POST['stop1']
			if stop1 != "":
				ride.stops = ride.stops + stop1 +","
		except MultiValueDictKeyError:
			pass
		try:
			stop2 = request.POST['stop2']
			if stop2 != "":
				ride.stops = ride.stops + stop2 +","
		except MultiValueDictKeyError:
			pass
		try:
			stop3 = request.POST['stop3']
			if stop3 != "":
				ride.stops = ride.stops + stop3 +","
		except MultiValueDictKeyError:
			pass
		ride.save()
		return HttpResponseRedirect('/chooseDriver/')
	return render(request, 'addingStops.html')

@login_required
def locateMe(request):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	message = ''
	if request.method == "POST":
		closeContacts = CloseContacts.objects.get(username=request.user.username)
		if closeContacts.cc1 != '' :
			response = sendSMS(int(closeContacts.cc1),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc2 != '' :
			response = sendSMS(int(closeContacts.cc2),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc3 != '' :
			response = sendSMS(int(closeContacts.cc3),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc4 != '' :
			response = sendSMS(int(closeContacts.cc4),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc5 != '' :
			response = sendSMS(int(closeContacts.cc5),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		message = "SOS Initialized successfully."
	return render(request, 'locateMe.html', {"isDriver" : isDriver, "message" : message})

@login_required
def notifications(request):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	return render(request, 'user.html',{'isDriver':isDriver})
	
@login_required
def faq(request):
	if request.method== 'POST':
		message = request.POST['message']
		return render(request, 'faq.html', {'message':message,'name':UserProfile.objects.get(Username=request.user.get_username()).FirstName})
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	return render(request, 'faq.html', {"isDriver" : isDriver})

@login_required
def upgrade(request):
	return render(request, 'user.html')

@login_required
def chooseDriver(request):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver

	booking = UserRides.objects.filter(username=request.user.get_username(), isDone=False)[0]
	if booking.driverId != '':
		driver = UserProfile.objects.get(Username=booking.driverId)
		return render(request, 'chooseDriver.html', {"isDriver" : isDriver, 'driver' : driver})
	return render(request, 'chooseDriver.html', {"isDriver" : isDriver})

@login_required
def rideOn(request, driver, customer):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	driverProfile = UserProfile.objects.get(Username=driver)
	customerProfile = UserProfile.objects.get(Username=customer)
	booking = UserRides.objects.filter(username=customer, isDone=False)[0]
	stops = booking.stops.split(",")
	message = ''
	if request.method == "POST":
		closeContacts = CloseContacts.objects.get(username=request.user.username)
		if closeContacts.cc1 != '' :
			response = sendSMS(int(closeContacts.cc1),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc2 != '' :
			response = sendSMS(int(closeContacts.cc2),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc3 != '' :
			response = sendSMS(int(closeContacts.cc3),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc4 != '' :
			response = sendSMS(int(closeContacts.cc4),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		if closeContacts.cc5 != '' :
			response = sendSMS(int(closeContacts.cc5),"\nYour dear one has raised an SOS emergency.\nCheck his live location")
		message = "SOS Initialized successfully."
	return render(request, 'rideOn.html', {"isDriver" : isDriver, "driver" : driverProfile, "customer" : customerProfile, "driverId" : booking.driverId, "amount" : booking.amount, "message" : message, "booking" : booking, "stops" : stops})

@login_required
def chooseRide(request):
	if request.method == 'POST':
		p = request.POST['pickup']
		d = request.POST['destination']
		dLat = request.POST['destLat']
		dLng = request.POST['destLng']
		pLat = request.POST['plat']
		pLng = request.POST['plng']

		if p=="Your Location":
			p = "LiveLocation"

		booking = UserRides.objects.create(username=request.user.get_username(), source=p,destination=d,dateTime=dt.now())
		booking.save()

		return HttpResponseRedirect('/addingStops/{}/{}/'.format(p,d))

	else:
		username = request.user.get_username()
		isDriver = UserDetailsInfo.objects.get(username=username).isDriver
		return render(request, 'chooseRide.html', {'pickup' : 'Your Location', "isDriver" : isDriver})

@login_required
def checkRides(request):
	username = request.user.get_username()
	isDriver = UserDetailsInfo.objects.get(username=username).isDriver
	if request.method == "POST":
		amount = request.POST['amount']
		rides = UserRides.objects.filter(isDone=False)[0]
		rides.driverId = request.user.get_username()
		rides.bargain = "0 " + amount + ","
		rides.save()
		return HttpResponseRedirect('/bargain/{}/'.format(request.user.get_username()))
	rides = UserRides.objects.filter(isDone=False)
	return render(request, 'checkRides.html', {"isDriver" : isDriver, 'rides' : rides})

def hashCode(text):
	import hashlib
	return str(hashlib.md5(text.encode()).hexdigest())

def otpAuthentication(request,hash_,pk,msg,pas):
	user = User.objects.get(username=pk)
	if request.method=="POST":
		userOtp = request.POST['otp']
		
		if len(userOtp)!=6:
			return render(request, 'otpAuthentication.html', {'message':'Otp should be of length 6!!'})
		
		userOtp = hashCode(str(userOtp))
		if hash_!=userOtp:
			return render(request, 'otpAuthentication.html', {'message':'Otp didn\'t match!!'})
		else:
			user.is_active=True
			user.save()

			mapi = WalletMapping.objects.create(name=pk)
			mapi.password = pas
			mapi.save()

			if msg=="register":
				messages.info(request, 'Your Registration has been successful! Login now.')
				return HttpResponseRedirect('/userData/login/')
			elif msg=="forgot":
				return redirect('/forgotPassword/' + str(pk) + "/"+ str(hash_) + "/")
	
	return render(request, 'otpAuthentication.html', {'message1':'Otp sent to mobile successfully!!'})