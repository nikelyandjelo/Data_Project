from django.shortcuts import render, redirect
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os 
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def convert_to_csv(data, fieldnames):
    filename = 'data.csv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            writer.writerow({
                fieldname: getattr(item, fieldname) for fieldname in fieldnames
            })

    return filename

def graph_income(request):
    incomes = Income.objects.all()
    fieldnames = ['date', 'amount', 'currency'] 
    csv_filename = convert_to_csv(incomes, fieldnames)

    df = pd.read_csv(csv_filename)

    fig, ax = plt.subplots()
    fig.set_size_inches(13,6)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values (by='date', inplace=True)
    ax.plot(df['date'], df['amount'])

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income Graph')

    graph_filename = os.path.join('static', 'income_graph.png')
    plt.savefig(graph_filename)

    plt.close(fig)

    context = {'csv_filename': csv_filename, 'graph_filename': graph_filename}
    return render(request, 'graph_income.html', context)

def graph_expense(request):
    expenses = Expense.objects.all()
    fieldnames = ['date', 'amount', 'currency', 'payment_method']
    csv_filename = convert_to_csv(expenses, fieldnames)

    df = pd.read_csv(csv_filename)

    fig, ax1 = plt.subplots(figsize=(6, 6)) 

    ax1.hist(df['amount'], bins=10)
    ax1.set_xlabel('Amount')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Expense Histogram')

    graph_filename = os.path.join('static', 'expense_histogram.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    fig, ax2 = plt.subplots(figsize=(6, 6))
    payment_counts = df['payment_method'].value_counts()
    ax2.bar(payment_counts.index, payment_counts.values)
    ax2.set_xlabel('Payment Method')
    ax2.set_ylabel('Count')
    ax2.set_title('Expense Bar Chart by Payment Method')

    graph_filename2 = os.path.join('static', 'expense_bar_chart.png')
    plt.savefig(graph_filename2)

    plt.tight_layout()
    plt.close(fig)

    context = {
        'csv_filename': csv_filename,
        'graph_filename': graph_filename,
        'graph_filename2': graph_filename2
    }
    return render(request, 'graph_expense.html', context)


def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def income_list(request):
    incomes = Income.objects.all()
    if request.method == 'POST' and 'delete' in request.POST:
        income_id =request.POST.get('delete')
        income = Income.objects.get(id=income_id)
        income.delete()
        return redirect('income_list')
    return render(request, 'income_list.html', {'incomes': incomes})

def expense_list(request):
    expenses = Expense.objects.all()
    if request.method == 'POST' and 'delete' in request.POST:
        expense_id =request.POST.get('delete')
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return redirect('expense_list')
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