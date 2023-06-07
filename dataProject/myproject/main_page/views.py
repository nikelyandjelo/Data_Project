from io import StringIO
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, ExpenseForm
from .graph import plot_histogram, line_graph, pie_chart, chart_bar, compare
from .models import Income, Expense, Category


def convert_to_csv(data, fieldnames):
    filename = 'data.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            writer.writerow({
                fieldname: getattr(item, fieldname) for fieldname in fieldnames
            })

    return filename


def convert_set_to_csv(queryset, fieldnames):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for obj in queryset:
        row = {field: getattr(obj, field) for field in fieldnames}
        writer.writerow(row)

    return output.getvalue()


def process_category(category_name, custom_category, user):
    category = None

    if custom_category:
        category, _ = Category.objects.get_or_create(
            name=custom_category, user=user)
    elif category_name:
        category, _ = Category.objects.get_or_create(
            name=category_name, user=user)

    return category


@login_required
def graph_income(request):
    incomes = Income.objects.filter(user=request.user)
    fieldnames = ['date', 'amount', 'currency', 'category_id']
    csv_filename = convert_to_csv(incomes, fieldnames)

    df = pd.read_csv(csv_filename)

    # line
    fig = line_graph(df, 'date', 'amount')

    graph_filename = os.path.join('static', 'income_graph.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    # pie chart
    grouped_data = df.groupby('category_id')['amount'].sum()
    category_ids = grouped_data.index.tolist()
    amounts = grouped_data.tolist()

    categories = Category.objects.filter(id__in=category_ids)
    labels = [str(category) for category in categories]

    fig = pie_chart(amounts, labels)
    graph_filename2 = os.path.join('static', 'income_equal.png')
    plt.savefig(graph_filename2)
    plt.close(fig)

    # chart_bar for currency
    currency_counts = df['currency'].value_counts()
    fig = chart_bar(currency_counts)
    graph_filename3 = os.path.join('static', 'income_bar_chart.png')
    plt.savefig(graph_filename3)
    plt.close(fig)

    context = {
        'csv_filename': csv_filename,
        'graph_filename': graph_filename,
        'graph_filename2': graph_filename2,
        'graph_filename3': graph_filename3
    }
    return render(request, 'graph_income.html', context)


@login_required
def graph_expense(request):
    expenses = Expense.objects.filter(user=request.user)
    fieldnames = ['date', 'amount', 'currency',
                  'payment_method', 'category_id']
    csv_filename = convert_to_csv(expenses, fieldnames)

    df = pd.read_csv(csv_filename)

    # line
    fig = line_graph(df, 'date', 'amount')

    graph_filename = os.path.join('static', 'expense_graph.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    # hist for amount
    fig = plot_histogram(df, 'amount')
    graph_filename1 = os.path.join('static', 'expense_amount_histogram.png')
    plt.savefig(graph_filename1)
    plt.tight_layout()
    plt.close(fig)

    # chart_bar for payment
    payment_counts = df['payment_method'].value_counts()
    fig = chart_bar(payment_counts)
    graph_filename2 = os.path.join('static', 'expense_bar_chart.png')
    plt.savefig(graph_filename2)
    plt.tight_layout()
    plt.close(fig)

    # pie chart
    grouped_data = df.groupby('category_id')['amount'].sum()
    category_ids = grouped_data.index.tolist()
    amounts = grouped_data.tolist()

    categories = Category.objects.filter(id__in=category_ids)
    labels = [str(category) for category in categories]

    fig = pie_chart(amounts, labels)
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


@login_required
def compare_income_expense(request):
    incomes = Income.objects.filter(user=request.user)
    fieldnames = ['date', 'amount', 'currency', 'category_id']
    csv_data1 = convert_set_to_csv(incomes, fieldnames)

    expenses = Expense.objects.filter(user=request.user)
    fieldnames = ['date', 'amount', 'currency',
                  'payment_method', 'category_id']
    csv_data2 = convert_set_to_csv(expenses, fieldnames)

    df1 = pd.read_csv(StringIO(csv_data1))
    df2 = pd.read_csv(StringIO(csv_data2))
    income_sum = df1['amount'].sum()
    expense_sum = df2['amount'].sum()
    # print(income_sum)
    # print(expense_sum)
    data = {'Type': ['Income', 'Expense'], 'Amount': [income_sum, expense_sum]}
    df = pd.DataFrame(data)

    # compareBarChart
    fig = compare(data=df, x='Type', y='Amount')
    graph_filename = os.path.join('static', 'compare.png')
    plt.savefig(graph_filename)
    plt.close(fig)

    context = {'graph_filename': graph_filename}

    return render(request, 'compare.html', context)


@login_required
def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    categories = Category.objects.filter(income__in=incomes).distinct()

    if request.method == 'POST' and 'delete' in request.POST:
        income_id = request.POST.get('delete')
        income = Income.objects.get(id=income_id)
        income.delete()
        category_id = request.POST.get('delete')
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect('income_list')

    context = {
        'incomes': incomes,
        'categories': categories,
    }
    return render(request, 'income_list.html', context)


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.filter(expense__in=expenses).distinct()

    if request.method == 'POST' and 'delete' in request.POST:
        expense_id = request.POST.get('delete')
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        category_id = request.POST.get('delete')
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect('expense_list')

    context = {
        'expenses': expenses,
        'categories': categories,
    }
    return render(request, 'expense_list.html', context)


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            custom_category = form.cleaned_data['custom_category']
            category = process_category(
                category_name, custom_category, request.user)
            form.instance.user = request.user
            form.instance.category = category
            form.instance.custom_category = custom_category
            form.save()
            return redirect('income_list')

    else:
        form = IncomeForm(user=request.user)
    return render(request, 'add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            custom_category = form.cleaned_data['custom_category']
            category = process_category(
                category_name, custom_category, request.user)
            form.instance.user = request.user
            form.instance.category = category
            form.instance.custom_category = custom_category
            form.save()
            return redirect('expense_list')

    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'add_expense.html', {'form': form})
