from django.shortcuts import render, redirect
from .graph import plot_histogram, line_graph, plot_pie_chart, chart_bar
from .models import Income, Expense, Category
from .forms import IncomeForm, ExpenseForm, process_category
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os 


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
    fieldnames = ['date', 'amount', 'currency', 'category_id'] 
    csv_filename = convert_to_csv(incomes, fieldnames)

    df = pd.read_csv(csv_filename)
    #line
    fig = line_graph(df, 'date', 'amount')
   
    graph_filename = os.path.join('static', 'income_graph.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    #pie chart
    df['amount'] = df['amount'].astype(float)
    grouped_data = df.groupby('category_id')['amount'].sum()
    category_ids = grouped_data.index.tolist()
    amounts = grouped_data.tolist()

    categories = Category.objects.filter(id__in=category_ids)
    labels = [str(category) for category in categories]

    fig = plot_pie_chart(amounts, labels)
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

    #hist for category
    fig = plot_histogram(df,'category_id') 
    graph_filename = os.path.join('static', f'expense_category_histogram.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    #hist for amount
    fig = plot_histogram(df, 'amount')
    graph_filename1 = os.path.join('static', f'expense_amount_histogram.png')
    plt.savefig(graph_filename1)
    plt.tight_layout()
    plt.close(fig)

    #chart_bar for payment
    payment_counts = df['payment_method'].value_counts()
    fig = chart_bar(payment_counts)
    graph_filename2 = os.path.join('static', 'expense_bar_chart.png')
    plt.savefig(graph_filename2)
    plt.tight_layout()
    plt.close(fig)

    #pie chart
    df['amount'] = df['amount'].astype(float)
    grouped_data = df.groupby('category_id')['amount'].sum()
    category_ids = grouped_data.index.tolist()
    amounts = grouped_data.tolist()

    categories = Category.objects.filter(id__in=category_ids)
    labels = [str(category) for category in categories]

    fig = plot_pie_chart(amounts, labels)
    graph_filename3 = os.path.join('static', 'expense_equal.png')
    plt.savefig(graph_filename3)
    plt.close(fig)

    context = {
        'csv_filename': csv_filename,
        'graph_filename': graph_filename,
        'graph_filename1': graph_filename1,
        'graph_filename2': graph_filename2,
        'graph_filename3': graph_filename3
    }
    return render(request, 'graph_expense.html', context)


def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def income_list(request):
    incomes = Income.objects.filter(user=request.user)
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
    categories = Category.objects.filter(expense__in=expenses).distinct()
    if request.method == 'POST' and 'delete' in request.POST:
        expense_id =request.POST.get('delete')
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return redirect('expense_list')
    context = {
        'expenses': expenses,
        'categories': categories,
    }
    return render(request, 'expense_list.html', context)

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            custom_category = form.cleaned_data['custom_category']
            category = process_category(category_name, custom_category, request.user)
            form.instance.user = request.user
            form.instance.category = category
            form.instance.custom_category = custom_category
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            custom_category = form.cleaned_data['custom_category']
            category = process_category(category_name, custom_category, request.user)
            form.instance.user = request.user
            form.instance.category = category
            form.instance.custom_category = custom_category
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})