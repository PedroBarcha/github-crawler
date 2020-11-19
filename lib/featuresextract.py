# get features from certain github repo

#Parser de url
import giturlparse

#Carrega as Env variables, do arquivo .env
from dotenv import load_dotenv
import os
load_dotenv()

#Colocar seu token em .env
token=os.environ.get('GITHUB_TOKEN')

#Cliente para api GraphQL
from sgqlc.operation import Operation
from sgqlc.types import Int, Enum, Field, Type, list_of, String, ID
from sgqlc.types.relay import Node, Connection, connection_args
from sgqlc.endpoint.http import HTTPEndpoint

#Classes representando a estrutura da query,mover deste arquivo
class IssueState(Enum):
    __choices__ = ('CLOSED', 'OPEN')


class IssueNode(Node):
    states = IssueState


class IssueEdge(Type):
    node = IssueNode
    cursor = String


class IssueConnection(Connection):
    nodes = list_of(IssueNode)
    edges = list_of(IssueEdge)
    totalCount = Int


class WatchersConnection(Connection):
    totalCount = Int


class licenseNode(Node):
    name = String

#Declarado somente os campos de interesse,mais camops podem ser adicionados
class RepoNode(Node):
    owner = String
    name = String
    databaseId = Int
    licenseInfo = Field(licenseNode)
    forkCount = Int
    stargazerCount = Int
    watchers = Field(WatchersConnection, args={**connection_args()})
    issues = Field(IssueConnection, args={'states': IssueState, **connection_args()})


class RepoEdges(Type):
    node = RepoNode
    cursor = String


class RepoConnection(Connection):
    edges = list_of(RepoEdges)
    nodes = list_of(RepoNode)

#Representa a query,mais de uma busca pode ser feita ao mesmo tempo com um request só, checar documentação (alias) sgqlc
class Query(Type):
    repository = Field(RepoNode, args={'name': String, 'owner': String, **connection_args()})

#cria uma query através das classes
def extractRepo(dono, nome):
    query = Operation(Query)
    query.repository(name=nome, owner=dono)
    query.repository.issues(states=IssueState.__to_graphql_input__(IssueState.OPEN))
    query.repository.issues.totalCount()
    query.repository.watchers.totalCount()
    query.repository.forkCount()
    query.repository.stargazerCount()
    query.repository.licenseInfo.name()
    print(query)

    #Formata o endpoint e header com o token
    endpoint = HTTPEndpoint('https://api.github.com/graphql',
                            {'Authorization': 'Bearer {0}'.format(token)})
    #realiza a query e retorna o resultado(json)
    result = endpoint(query=query)
    #mapeia json para o objeto,segue a estrutura das classes utilizadas para gerar a query
    repo = (query + result).repository
    print(repo)
    return repo

# call all other extraction methods below
def extractAll(url):
    # Parser de url simples, mover deste arquivo
    p = giturlparse.parse(url)
    if (p.resource != "github.com"):
        print("Host invalido")
        print(p)
    elif (p.name is "none" or p.owner is "none"):
        print("url incompleta")
    else:
        return extractRepo(p.owner, p.name)



