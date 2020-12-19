# get features from certain github repo
import datetime
import time
# Cliente para api GraphQL
import lib.graphql_classses as ql
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

# Parser de url
from giturlparse import parse

from lib.database import session
from lib.classe_repositorio import Repository as Repo
from lib.database import UrlList

# Carrega as Env variables, do arquivo .env
import os
from dotenv import load_dotenv

load_dotenv()
# Colocar seu token em .env
token = os.environ.get('GITHUB_TOKEN')


def parser(url):
    p = parse(url)
    if p.valid and p.github:
        if p.data.get('repo') is None or p.data.get('owner') is None:
            raise Exception('Informação faltante')
        return p.data
    else:
        raise Exception('URL inválida!')


def populate_list(url):
    try:
        erro = False
        visitado = False
        github_url = parser(url)
        repo = github_url.get('repo')
        owner = github_url.get('owner')
        print(owner, repo)
        id_count = session.query(Repo.id).filter(Repo.name == repo, Repo.owner == owner).scalar()
        if id_count is not None:
            visitado = True
    except Exception as e:
        erro = True
        print(e)

    if erro:
        url_entry = UrlList(url=url, erro=erro)
    elif visitado:
        url_entry = UrlList(url=url, visitado=visitado, repo_id=id_count)
    else:
        url_entry = UrlList(url=url)
    if session.query(UrlList.id).filter(UrlList.url == url).scalar() is None:
        session.add(url_entry)


def check_api_limit(limite):
    print('Queries realizadas na última hora: ' + str(limite.used))
    if limite.used >= 5000:
        reset = limite.resetAt
        now = datetime.datetime.now(datetime.timezone.utc)
        time.sleep((reset - now).total_seconds() + 5)


def check_errors(result):
    error_elements = []
    if 'errors' in result.keys():
        for e in result['errors']:
            print(e)
            if e['type'] == "NOT_FOUND":
                error_elements.append(e['path'][0])
    return error_elements


def check_exists(repo_id):
    return session.query(Repo.id).filter(Repo.id == repo_id).scalar() is not None


def session_commit():
    try:
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()


def add_repo(query_result, repo_entry, alias):
    if not check_exists(query_result[alias].databaseId):
        session.add(repo_entry)
        session_commit()
        return True
    else:
        return False


# create query using operation module from sgqlc and classes defined in graphql_classes
def create_query(url):
    query = Operation(ql.Query)
    # F
    for i in range(0, len(url)):
        github_url = parser(url[i]['url'])
        alias = ('alias_' + str(i))
        repos = query.repository(name=github_url.get('repo'), owner=github_url.get('owner'), __alias__=alias)
        repos.issues(states=ql.IssueState.__to_graphql_input__(ql.IssueState.OPEN))
        repos.issues.totalCount()
        repos.watchers.totalCount()
        repos.commitComments.totalCount()
        repos.licenseInfo.name()
        repos.__fields__('name', 'forkCount', 'stargazerCount', 'databaseId', 'updatedAt', 'pushedAt')
    rate_limit = query.rateLimit()
    rate_limit.__fields__('cost', 'limit', 'nodeCount', 'remaining', 'resetAt', 'used')
    return query


def create_repo_object(repo, result, alias, owner):
    return Repo(name=repo.name, owner=owner,
                license=None if result['data'][alias]['licenseInfo'] is None else repo.licenseInfo.name,
                id=repo.databaseId, forkCount=repo.forkCount, watchersCount=repo.watchers.totalCount,
                stargazerCount=repo.stargazerCount, openIssues=repo.issues.totalCount,
                updatedAt=repo.updatedAt, pushedAt=repo.pushedAt,
                commits=repo.commitComments.totalCount, )


def process_result(url, query, result, avoid):
    if "data" in result.keys():
        query_result = (query + result)
        for i in range(0, len(url)):
            db_url = session.query(UrlList).filter_by(url=url[i]['url']).first()
            alias = ('alias_' + str(i))
            if alias not in avoid:
                db_url.visitado = True
                repo_entry = create_repo_object(query_result[alias], result, alias, parser(url[i]['url']).get('owner'))
                if add_repo(query_result, repo_entry, alias):
                    db_url.repo_id = query_result[alias].databaseId
                else:
                    db_url.visitado = True
                    db_url.erro = True
                session_commit()
        return query_result
    else:
        raise Exception('Erro na query: ' + result.get('errors')[0]['message'])


def batch_url(url):
    query = create_query(url)
    endpoint = HTTPEndpoint('https://api.github.com/graphql',
                            {'Authorization': 'Bearer {0}'.format(token)})
    # realiza a query e retorna o resultado(json)
    result = endpoint(query=query)
    avoid = check_errors(result)
    return process_result(url, query, result, avoid)


# call all other extraction methods below

def extract_all():
    used = 0
    print("Quantidade de repos à ser vasculhado: " + str(
        session.query(UrlList.url).filter_by(visitado=False).count()))
    while session.query(UrlList.url).filter_by(visitado=False).first() is not None:
        repos_urls = session.query(UrlList.url).filter_by(visitado=False, erro=False).with_entities(UrlList.url).limit(120).all()
        try:
            retorno = batch_url(repos_urls)
            check_api_limit(retorno.rateLimit)
        # TODO:implement proper exceptions,name resolution errors should be treated separately
        except Exception as msg:
            used += 1
            print(msg)
