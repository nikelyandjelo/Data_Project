from django.shortcuts import render, redirect
from .models import Income, Expense, Category
from .forms import IncomeForm, ExpenseForm
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os 
import numpy as np

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

def plot_histogram(data, field):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.hist(data[field], bins=10)
    ax.set_xlabel(field.capitalize())
    ax.set_ylabel('Frequency')
    ax.set_title(f'{field.capitalize()} Histogram')

    return fig

def graph_income(request):
    incomes = Income.objects.all()
    fieldnames = ['date', 'amount', 'currency', 'category_id'] 
    csv_filename = convert_to_csv(incomes, fieldnames)

    df = pd.read_csv(csv_filename)

    fig, ax = plt.subplots(figsize = (13,6))

    df['date'] = pd.to_datetime(df['date'])
    df.sort_values (by='date', inplace=True)
    ax.plot(df['date'], df['amount'])

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income Graph')

    graph_filename = os.path.join('static', 'income_graph.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize = (6,6))

    df['amount'] = df['amount'].astype(float)
    grouped_data = df.groupby('category_id')['amount'].sum()

    category_ids = grouped_data.index.tolist()
    amounts = grouped_data.tolist()

    categories = Category.objects.filter(id__in=category_ids)
    labels = [str(category) for category in categories]

    ax1.pie(amounts, labels=labels, autopct='%1.1f%%')
    ax1.axis("equal")

    graph_filename2 = os.path.join('static', 'income_equal.png')
    plt.savefig(graph_filename2)
    plt.close(fig)

    context = {
            'csv_filename': csv_filename, 
            'graph_filename': graph_filename,
            'graph_filename2': graph_filename2
        }
    return render(request, 'graph_income.html', context)


def graph_expense(request):
    expenses = Expense.objects.all()
    fieldnames = ['date', 'amount', 'currency', 'payment_method','category_id']
    csv_filename = convert_to_csv(expenses, fieldnames)

    df = pd.read_csv(csv_filename)

    field_to_analyze = 'category_id'
    fig = plot_histogram(df, field_to_analyze)
    graph_filename = os.path.join('static', f'expense_{field_to_analyze}_histogram.png')
    fig.savefig(graph_filename)
    plt.close(fig)

    field_to_analyze = 'amount'
    fig = plot_histogram(df, field_to_analyze)
    graph_filename1 = os.path.join('static', 'expense_histogram.png')
    plt.savefig(graph_filename1)
    plt.tight_layout()
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
        'graph_filename1': graph_filename1,
        'graph_filename2': graph_filename2
    }
    return render(request, 'graph_expense.html', context)


def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def income_list(request):
    incomes = Income.objects.all()
    categories = Category.objects.filter(income__in=incomes).distinct()
    if request.method == 'POST' and 'delete' in request.POST:
        income_id =request.POST.get('delete')
        income = Income.objects.get(id=income_id)
        income.delete()
        return redirect('income_list')
    context = {
        'incomes': incomes,
        'categories': categories,
    }
    return render(request, 'income_list.html',context)

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