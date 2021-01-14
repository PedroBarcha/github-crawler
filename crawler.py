from lib import stats

repos_jsons_path = "repos/json/"
repos_urls_output_file = "repos/urls.txt"

# get repos' URLs (BRADA)
#reposurls.getUrls(repos_jsons_path,repos_urls_output_file)

#Popular tabela de usuarios
# with open('repos/urls_limpas.txt') as f:
#      repos_urls = f.read().splitlines()
# for url in repos_urls:
#     try:
# #Preenche tabela de ususarios
#         featuresextract.popularLista(url)
#         database.session.commit()
#     except Exception as e:
#         print(e)
#         database.session.rollback()
#get all repos information (TK)
#featuresextract.extract_all()




#stats (GUS)
# ...
stats.plot_repos_by_license()
