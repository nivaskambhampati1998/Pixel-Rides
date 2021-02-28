from django.shortcuts import render, redirect
from userData.forms import UserForm, UserDetailsInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userData.models import UserDetailsInfo
from userProfile.models import UserProfile

def hashCode(text):
	import hashlib
	return str(hashlib.md5(text.encode()).hexdigest())

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

def sendOtp(request):
	if request.method == 'POST':
		from random import randint
		import hashlib
		otp = str(randint(100000,999999))
		hash_ = hashCode(otp)
		pk = str(request.POST['username'])
		if User.objects.filter(username=pk).exists():
			response = sendSMS(int(pk),"\nYour Otp is : " + str(otp) + ".\nThank you for using on PixelRides :) .")
			if response["return"]:
				msg = "forgot"
				pas = "changePassword"
				return redirect('/verifyOtp/' + str(hash_)+"/" + str(pk)+"/" + str(msg)+"/"+ str(pas) + "/")
			else:
				return render(request,'userData/enterNumber.html')
		else:
			return render(request, 'userData/enterNumber.html', {'message':'You have not registered. Please register.'})		
	return render(request, 'userData/enterNumber.html')


def registration(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserDetailsInfoForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			if request.POST['password']!=request.POST['retype_password']:
				user_form = UserForm()
				profile_form = UserDetailsInfoForm()
				return render(request,'userData/registration.html',
						              {'user_form':user_form,
						               'profile_form':profile_form,
						               'registered':registered,
						               'message':'Passwords didn\'t match!!'})
			if request.POST['mPin']!=request.POST['retype_mPin']:
				user_form = UserForm()
				profile_form = UserDetailsInfoForm()
				return render(request,'userData/registration.html',
						              {'user_form':user_form,
						               'profile_form':profile_form,
						               'registered':registered,
						               'message':'mPins didn\'t match!!'})
			if len(request.POST['mPin'])!=4:
				user_form = UserForm()
				profile_form = UserDetailsInfoForm()
				return render(request,'userData/registration.html',
						              {'user_form':user_form,
						               'profile_form':profile_form,
						               'registered':registered,
						               'message':'mPin length should be 4!!'})
			
			user = user_form.save()
			user.set_password(user.password)
			user.is_active = False
			user.save()
			profile = profile_form.save(commit=False)
			profile.username = request.POST['username']
			profile.save()
			registered = True

			details = UserProfile.objects.create(Username=request.POST['username'])
			details.EmailAddress = request.POST['email']
			details.FirstName = request.POST['first_name']
			details.save()

			from random import randint
			import hashlib
			otp = str(randint(100000,999999))
			hash_ = hashCode(otp)
			pk = str(request.POST['username'])
			response = sendSMS(int(pk),"\nYour Otp is : " + str(otp) + ".\nThank you for registering on PixelRides :) .")
			if response["return"]:
				msg = "register"
				pas = hashCode(request.POST['password'])
				return redirect('/verifyOtp/' + str(hash_)+"/" + str(pk)+"/" + str(msg)+"/"+ str(pas) + "/")
			else:
				user_form = UserForm()
				profile_form = UserDetailsInfoForm()
				return render(request,'userData/registration.html',
						              {'user_form':user_form,
						               'profile_form':profile_form,
						               'registered':registered,
						               'message':response["message"]})
		else:
			user = User.objects.get(username=request.POST['username'])
			if user.is_active == False:
				from random import randint
				import hashlib
				otp = str(randint(100000,999999))
				hash_ = hashCode(otp)
				pk = str(request.POST['username'])
				response = sendSMS(int(pk),"\nYour Otp is : " + str(otp) + ".\nThank you for registering on PixelRides :) .")
				if response["return"]:
					msg = "register"
					pas = hashCode(request.POST['password'])
					return redirect('/verifyOtp/' + str(hash_)+"/" + str(pk)+"/" + str(msg)+"/"+ str(pas) + "/")
				else:
					user_form = UserForm()
					profile_form = UserDetailsInfoForm()
					return render(request,'userData/registration.html',
							              {'user_form':user_form,
							               'profile_form':profile_form,
							               'registered':registered,
							               'message':response["message"]})

			error = str(user_form.errors).split('<li>')[2].split('</li>')[0]
			if 'username' in error:
				error = error.replace('username','mobile number')
			user_form = UserForm()
			profile_form = UserDetailsInfoForm()
			return render(request,'userData/registration.html',
					              {'message':error,
					               'user_form':user_form,
					               'profile_form':profile_form,
					               'registered':registered})
	else:
		user_form = UserForm()
		profile_form = UserDetailsInfoForm()
		return render(request,'userData/registration.html',
				              {'user_form':user_form,
				               'profile_form':profile_form,
				               'registered':registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST['mobile']
		mode = request.POST['authentication']
		mpin = request.POST['mpin']
		password = request.POST['password']

		if mode!='password':
			try:
				user = UserDetailsInfo.objects.get(username=username)
				if str(user.mPin) == str(mpin):
					user = User.objects.get(username=username)
					user.backend = 'django.contrib.auth.backends.ModelBackend'
					login(request, user)
					return HttpResponseRedirect(reverse('dashboard'))
				else:
					return render(request, 'userData/login.html', {'message2':'Wrong Username or mPin!!'})
			except UserDetailsInfo.DoesNotExist:
				return render(request, 'userData/login.html', {'message2':'User doesn\'t exist!! Please Register.'})

		user = User.objects.get(username=username)
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				return render(request, 'userData/login.html', {'message2':'Your account is not verified!!'})
		else:
			return render(request, 'userData/login.html', {'message2':'Wrong Username or Password!!'})
	else:
		return render(request, 'userData/login.html', {'message2':''})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))