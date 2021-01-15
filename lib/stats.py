#get statistics of a list of github repos' features
#from lib.database import engine

from lib import static

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

REPOS_BY_LICENSE_QUERY = """
        SELECT r.license,
           SUM(r.commits),
           SUM(r.forkCount),
           SUM(r.Issues),
           SUM(r.stargazerCount),
           SUM(r.Watchers)
    FROM repositorios r
    GROUP BY r.license;
"""

strong_copyleft = ["GNU General Public License v2.0", "GNU General Public License v3.0",
 "GNU Affero General Public License v3.0"]

weak_copyleft = ['Eclipse Public License 1.0',
 'Eclipse Public License 2.0', 'GNU Lesser General Public License v2.1',
 'GNU Lesser General Public License v3.0', 'Microsoft Reciprocal License',
 'Mozilla Public License 2.0', 'Open Software License 3.0']

permissive = ['Apache License 2.0', 'BSD 2-Clause "Simplified" License',
 'BSD 3-Clause "New" or "Revised" License', 'BSD 3-Clause Clear License',
 'BSD Zero Clause License', 'Boost Software License 1.0', 'ISC License',
 'MIT License', 'Universal Permissive License v1.0']

def execute_query(query):
    return engine.execute(query)

# def get_repos_by_licence():
#     return execute_query(REPOS_BY_LICENSE_QUERY)

def map_license_to_group(license):
    if license in strong_copyleft:
        return 'Strong Copyleft'
    elif license in weak_copyleft:
        return 'Weak Copyleft'
    elif license in permissive:
        return 'Permissive'
    else:
        return 'Non-Free'

def group_licenses(data):
    data['license'] = data['license'].apply(lambda x: map_license_to_group(x))
    print(data)

def plot_repos_by_license():
    data = static.read_file('static_data/get_by_license.csv')
    group_licenses(data)

    plot_commits_per_license(data)
    plot_forks_per_license(data)
    plot_issues_per_license(data)
    plot_stars_per_license(data)
    plot_watchers_per_license(data)
    plot_repos_per_license(data)

def plot_commits_per_license(data):
    plot_graph(data, 'license', 'commits', 'Número de commits por licença')

def plot_forks_per_license(data):
    plot_graph(data, 'license', 'forkCounts', 'Número de forks por licença')

def plot_issues_per_license(data):
    plot_graph(data, 'license', 'issues', 'Número de issues por licença')

def plot_stars_per_license(data):
    plot_graph(data, 'license', 'stargazerCounts', 'Número de stars por licença')

def plot_watchers_per_license(data):
    plot_graph(data, 'license', 'watchers', 'Número de watchers por licença')

def plot_repos_per_license(data):
    plot_graph(data, 'license', 'numberOfRepos', 'Número de repositórios por licença')

def plot_graph(data, x, y, title):

    dataset = data.groupby(by=[x])[y].sum().reset_index(name=y)

    print(dataset)

    ax = sns.barplot(x=x, y=y, palette='deep', data = dataset)

    # for index, row in dataset.iterrows():
    #     print(row.array)
    #     ax.text(row.name, row.array[0], round(row.array[1], 2), color='black', ha="center")
    show_values_on_bars(ax)
    ax.set_title(title, color='black')
    ax.set_xlabel('')
    ax.figure.set_size_inches(15,7)
    ax.figure.savefig(title + '.png')
    ax.figure.clf()

def show_values_on_bars(axs):
    def _show_on_single_plot(ax):
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height())
            ax.text(_x, _y, value, ha="center")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)
