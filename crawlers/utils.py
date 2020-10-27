#The Movie Database (tmdb) API
import tmdbsimple as tmdb
tmdbKey = '441317b48174ab9861771dcda23dd5d2'
tmdb.API_KEY = tmdbKey

'----------------------------TMDB_API------------------------------------------------------'

def get_movie_info(id):
    '''return information about a movie given its id'''
    return tmdb.Movies(id).info(**{'append_to_response': 'trailers'})

def get_similar_movies(id):
    return tmdb.Movies(id).similar_movies()['results']

def get_url(id):
    '''return list of youtube trailer urls given movie id.
    head of list corresponds to most recent trailer.'''
    trailers = []
    for i in range(len(get_movie_info(id)['trailers']['youtube'])):
        source = get_movie_info(id)['trailers']['youtube'][i]['source']
        trailers.append("http://www.youtube.com/watch?v={0}".format(source))
    return trailers
