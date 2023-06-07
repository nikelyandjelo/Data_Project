import matplotlib.pyplot as plt
import seaborn as sns


def plot_histogram(data, field):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.hist(data[field], bins=10)
    ax.set_xlabel(field.capitalize())
    ax.set_ylabel('Frequency')
    ax.set_title(f'{field.capitalize()} Histogram')

    return fig


def line_graph(data, x_field, y_field):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data[x_field], data[y_field])
    ax.set_xlabel(x_field.capitalize())
    ax.set_ylabel(y_field.capitalize())
    ax.set_title(f'{y_field.capitalize()} vs {x_field.capitalize()}')

    return fig


def pie_chart(data, labels):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.axis("equal")

    return fig


def chart_bar(data):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.bar(data.index, data.values)
    ax.set_xlabel(data.name.capitalize())
    ax.set_ylabel('Count')
    ax.set_title(f'{data.name.capitalize()} Bar Chart')

    return fig


def compare(data, x, y):
    fig, ax = plt.subplots(figsize=(6, 6))

    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set_xlabel(x.capitalize())
    ax.set_ylabel(y.capitalize())
    ax.set_title(f'{y.capitalize()} vs {x.capitalize()}')

    return fig


def heatmap(data, x, y):
    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(data=data, x=x, y=y, ax=ax)
    ax.set_xlabel(x.capitalize())
    ax.set_ylabel(y.capitalize())
    ax.set_title(f'{y.capitalize()} vs {x.capitalize()}')

    return fig
