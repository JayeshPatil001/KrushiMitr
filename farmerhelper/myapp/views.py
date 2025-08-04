from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout
from .models import Crop,Expense,Harvest
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import os
import google.generativeai as genai
from dotenv import load_dotenv
from .forms import HarvestForm,CropForm, ExpenseForm


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
username =None

def generate_info(question):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
  
    prompt = (
    "You are an agricultural expert helping a farmer understand a concept.\n"
    "Provide a clear, beginner-friendly explanation in Marathi language using Devanagari script about the following topic:\n"
    f"\"{question}\".\n"
    "Avoid technical jargon. Use simple words and real-world examples relevant to farming.\n"
    "The explanation should be detailed, practical, and easy to follow.\n"
    "Keep the tone respectful and supportive, as if you're guiding someone new to the topic.\n"
)


    response = model.generate_content(prompt)
    return response.text



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})  

def user_register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('login')
          
    else:
        form=UserCreationForm()
        return render(request,'register.html',{'form':form})
    

@login_required
def home(request):
    user=request.user
    total_crops = Crop.objects.filter(user=user).count()

    total_sales = Harvest.objects.filter(user=user).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    profit = total_sales - total_expenses

    context = {
        'total_crops': total_crops,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
    }
    return render(request, 'home.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def user_inquiry(request):
    if request.method=="POST":
        question=request.POST.get("question")
        response=generate_info(question)
        return render(request,'response.html',{'question':question, 'response':response})
    return render(request,'response.html')

@login_required
def add_harvest(request):
    if request.method == 'POST':
        form = HarvestForm(request.POST)
        if form.is_valid():
            harvest = form.save(commit=False)  
            harvest.user = request.user        
            harvest.save()                     
            return redirect('home')
    else:
        form = HarvestForm()

    return render(request, 'harvest.html', {'form': form})


@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user
            crop.save()
            return redirect('home')
    else:
        form = CropForm()
    return render(request, 'crop.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expense.html', {'form': form})


@login_required
def history(request):
    return render(request,'history.html')


@login_required
def harvest_history(request):
    user = request.user
    harvests = Harvest.objects.filter(user=user)  

    if request.method == 'GET' and 'filter_type' in request.GET:
        filter_type = request.GET.get('filter_type')

        if filter_type == 'crop':
            crop_name = request.GET.get('crop_name')
            if crop_name:
                finalresult = harvests.filter(crop__name__icontains=crop_name)
                return render(request,'harvest_result.html',{'harvest':harvests})

        elif filter_type == 'buyer':
            buyer = request.GET.get('buyer_name')
            if buyer:
                finalresult = harvests.filter(buyer__icontains=buyer)
                return render(request,'harvest_result.html',{'harvest':harvests})

        elif filter_type == 'date':
            date = request.GET.get('harvest_date')
            if date:
                finalresult = harvests.filter(date_of_harvest=date)
                return render(request,'harvest_result.html',{'harvest':finalresult})

    return render(request, 'harvest_history.html')


@login_required
def expense_history(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)  

    if request.method == 'GET' and 'filter_type' in request.GET:
        filter_type = request.GET.get('filter_type')

        if filter_type == 'crop':
            crop_name = request.GET.get('crop_name')
            if crop_name:
                finalresult = expenses.filter(crop__name__icontains=crop_name)
                return render(request, 'expense_result.html', {'expenses': finalresult})

        elif filter_type == 'date':
            date = request.GET.get('date')
            if date:
                finalresult = expenses.filter(date=date)
                return render(request, 'expense_result.html', {'expenses': finalresult})

    return render(request, 'expense_history.html')


