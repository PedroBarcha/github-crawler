curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/OWNER/REPO/

#Numeros diversos
https://docs.github.com/en/free-pro-team@latest/rest/reference/repos
- # open issues
- # forks
- # watchers
- # stars
- # contribuidores: /collaborators
Só usar a api sem nenhum path adicional

#Licenses
https://docs.github.com/en/free-pro-team@latest/rest/reference/licenses

#Stats
https://developer.github.com/v3/repos/statistics/

##Get all contributor commit activity
- numero de contribuidores
- numero de commits total
stats/contributors

##Get the last year of commit activity
stats/commit_activity

##Get the weekly commit activity
stats/code_frequency

##Get the weekly commit count
stats/participation

##Get the hourly commit count for each day
stats/punch_card