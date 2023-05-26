from django.shortcuts import render, redirect
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os 

def convert_to_csv(incomes):
    filename = 'income_data.csv' 
    fieldnames = ['Date', 'Amount', 'Currency'] 

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader() 

        for income in incomes:
            writer.writerow({
                'Date': income.date,
                'Amount': income.amount,
                'Currency': income.currency
            })

    return filename

def graph_income(request):
    incomes = Income.objects.all()
    csv_filename = convert_to_csv(incomes)

    df = pd.read_csv(csv_filename)

    fig, ax = plt.subplots()
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values (by='Date', inplace=True)
    ax.plot(df['Date'], df['Amount'])

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income Graph')

    graph_filename = os.path.join('static', 'income_graph.png')
    plt.savefig(graph_filename)

    plt.close(fig)

    context = {'csv_filename': csv_filename, 'graph_filename': graph_filename}
    return render(request, 'graph_income.html', context)

def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})