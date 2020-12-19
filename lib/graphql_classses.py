from sgqlc.types import Int, Enum, Field, Type, list_of, String, ID, datetime
from sgqlc.types.relay import Node, Connection, connection_args

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


class CollaboratorConnection(Connection):
    totalCount = Int

class CommitCommentsConnection(Connection):
    totalCount = Int

# declaring only fields of interest,
# but more can be added following github api V4.0 Object documentation
class RepoNode(Node):
    pushedAt =datetime.DateTime
    owner = String
    name = String
    databaseId = Int
    licenseInfo = Field(licenseNode)
    forkCount = Int
    stargazerCount = Int
    watchers = Field(WatchersConnection, args={**connection_args()})
    issues = Field(IssueConnection, args={'states': IssueState, **connection_args()})
    commitComments = Field(CommitCommentsConnection,args={**connection_args()})
    collaborators = Field(CollaboratorConnection,args={**connection_args()})
    updatedAt = datetime.DateTime


class RepoEdges(Type):
    node = RepoNode
    cursor = String


class RepoConnection(Connection):
    edges = list_of(RepoEdges)
    nodes = list_of(RepoNode)

class RateLimit(Node):
    cost=Int
    limit=Int
    nodeCount=Int
    remaining=Int
    resetAt=datetime.DateTime
    used=Int

# Represent a query, multiple repositories can be queried at a time, see Alias in sgqlc documentation
class Query(Type):
    repository = Field(RepoNode, args={'name': String, 'owner': String, **connection_args()})
    rateLimit = Field(RateLimit)

