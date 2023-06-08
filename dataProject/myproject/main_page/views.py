from io import StringIO
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, ExpenseForm
from .graph import plot_histogram, line_graph, pie_chart, chart_bar, compare
from .utils import convert_set_to_csv, convert_to_csv, process_category
from .models import Income, Expense, Category


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

    #heatmap
    df['date'] = pd.to_datetime(df['date']) 
    df['month'] = df['date'].dt.month 
    df['year'] = df['date'].dt.year  
    df_grouped = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    df_pivot = df_grouped.pivot('month', 'year', 'amount')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data=df_pivot, annot=True, fmt=".1f", cmap='viridis', ax=ax)

    ax.set_xlabel('Year')
    ax.set_ylabel('Month')
    ax.set_title('Income Heatmap')
    ax.invert_yaxis()

    graph_filename4 = 'static/heatmap.png'
    plt.savefig(graph_filename4)
    plt.close(fig)

    context = {
        'csv_filename': csv_filename,
        'graph_filename': graph_filename,
        'graph_filename2': graph_filename2,
        'graph_filename3': graph_filename3,
        'graph_filename4': graph_filename4
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

    #heatmap
    df['date'] = pd.to_datetime(df['date']) 
    df['month'] = df['date'].dt.month 
    df['year'] = df['date'].dt.year  
    df_grouped = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    df_pivot = df_grouped.pivot('month', 'year', 'amount')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data=df_pivot, annot=True, fmt=".1f", cmap='viridis', ax=ax)

    ax.set_xlabel('Year')
    ax.set_ylabel('Month')
    ax.set_title('Expense Heatmap')
    ax.invert_yaxis()
    
    graph_filename4 = 'static/heatmap_expense.png'
    plt.savefig(graph_filename4)
    plt.close(fig)

    context = {
        'csv_filename': csv_filename,
        'graph_filename': graph_filename,
        'graph_filename1': graph_filename1,
        'graph_filename2': graph_filename2,
        'graph_filename3': graph_filename3,
        'graph_filename4': graph_filename4
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
        category_id = income.category_id
        income.delete()

        if category_id:
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
        category_id = expense.category_id
        expense.delete()

        if category_id:
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
            return redirect('add_income')

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
            return redirect('add_expense')

    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'add_expense.html', {'form': form})