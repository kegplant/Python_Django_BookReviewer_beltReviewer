from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from models import Users, Books, Reviews
import bcrypt
from django.contrib.messages import error
    
# the index function is called when root is visited
def isLoggedIn(request):
    try:
        request.session['user_id']
        return True
    except:
        return False
def index(request):
    context={
        'status':isLoggedIn(request)
    }
    #return HttpResponse(response)
    return render(request,'logIn_registration/index.html',context)

def register(request):
    #validate
    errors=Users.objects.registration_validator(request.POST)
    if errors:
        for tag,message in errors.items():
            error(request,message,extra_tags=tag)
        return redirect('/')
    else:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        hash1=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        user=Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=hash1)
        request.session['user_id']=user.id
        return redirect('/'+str(user.id)+'/success')
def logIn(request):
    #if wrong: credential / existance, flash message
    errors=Users.objects.logIn_validator(request.POST)
    if errors:
        for tag,message in errors.items():
            error(request,message,extra_tags=tag)
        return redirect('/')
    else:
        user=Users.objects.filter(email=request.POST['email'])[0]
        if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
            request.session['user_id']=user.id
            return redirect('/'+str(user.id)+'/success')
        #flash vague message//wrong password   
def process(request):
    if request.method=='POST':
        if request.POST['type']=='register':            
            return register(request)
        if request.POST['type']=='log in':            
            return logIn(request)
    return redirect('/')

def success(request,id):
    if not isLoggedIn(request):
        return redirect('/')
    user=Users.objects.get(id=id)
    context={
        'user': user,
    }
    return redirect('/books')#render(request,'logIn_registration/success.html',context)

def books(request):#but for stars, \/
    if not isLoggedIn(request):
        return redirect('/')
    context={
        'books':Books.objects.all(),
        'stars':'*'*3,
        'noStars':'^'*2,
        'name':Users.objects.get(id=request.session['user_id']).last_name,
        'reviews':Reviews.objects.all().order_by('-id')[:3]
    }
    return render(request,'logIn_registration/books.html',context)
def books_add(request):#finished
    if not isLoggedIn(request):
        return redirect('/')
    context={
        'user_id':request.session['user_id']
    }
    return render(request,'logIn_registration/books_add.html',context)
def review_create(request):
    if request.method=='POST':
        #validate
        print request.POST['rating']
        print 'here'
        print request.POST['review']
        print int(request.POST['user_id'])
        int(request.POST['book_id'])
        Reviews.objects.createReview(request.POST)
        # user=Users.objects.get(id=int(request.POST['user_id']))
        # book=Books.objects.get(id=int(request.POST['book_id']))
        # Reviews.objects.create(user=user,book=book,rating=int(request.POST['rating']),review=request.POST['review'])
        book=Books.objects.get(id=request.POST['book_id'])
        return redirect('/books/'+str(book.id))
    return redirect('/books')
def books_create(request):  #besides validation & review, \/
    if request.method=='POST':
        #validate in views
        #create book \/
        book=Books.objects.createBook(request.POST)
        user=Users.objects.get(id=int(request.POST['user_id']))
        Reviews.objects.create(user=user,book=book,rating=int(request.POST['rating']),review=request.POST['review'])
        #also create review
        return redirect('/books/'+str(book.id))
    return redirect('/')
def books_show(request,book_id):#but for validation, \/
    if not isLoggedIn(request):
        return redirect('/')
    #check if book_id in range
    context={
        'book':Books.objects.get(id=book_id),
        'user':Users.objects.get(id=request.session['user_id'])
    }
    return render(request,'logIn_registration/books_show.html',context)
def review_destroy(request,review_id):
    if not isLoggedIn(request):
        return redirect('/')
    #validate
    print review_id
    review=Reviews.objects.get(id=review_id)
    print review_id
    book_id=review.book.id
    review.delete()
    print book_id
    return redirect('/books/'+str(book_id))   
def users(request,id): #\/
    if not isLoggedIn(request):
        return redirect('/')
    #validate id in range, pass user to context
    context={
        'user':Users.objects.get(id=id)
    }
    return render(request,'logIn_registration/users.html',context)





def clear(request):
    Users.objects.all().delete()
    return redirect('/')
def logOut(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')