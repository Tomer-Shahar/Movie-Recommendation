"""

This class parses the movie rating file and creates a huge array containing the pearson correlation of each user.

"""
import csv
import math


# noinspection PyPep8Naming
class Parse:

    def __init__(self, path=''):
        self.filePath = path
        self.PearsonScoreDictionary = {}  # A dictionary mapping pearson correlation between users.
        self.movies = {}  # A dictionary containing each movie and the ratings it Receives per user
        self.users = {}  # A dictionary mapping user IDs to their average/ratings
        self.movieNames = {}  # A dictionary that maps movie titles to their numbers

    def parse_movieDB_files(self):

        self.__create_dictionaries()
        self.__mapMovieNames()
        self.__calculateAverages()
        self.__populateNeighbors()

        for user_a_id, user_a in self.users.items():
            for user_w in user_a.neighbors:
                score = self.__calculate_score(user_a, self.users[user_w])
                self.PearsonScoreDictionary[user_a_id][user_w] = score
                self.PearsonScoreDictionary[user_w][user_a_id] = score

    def get_pearson_table(self):
        return self.PearsonScoreDictionary

    def get_movie_id(self, movie_title):
        return self.movieNames[movie_title]

    def get_movie_name(self, movieID):
        return self.movies[movieID].name

    # receives a user ID and a movie Id and returns the predicted rating of the given user for the movie.
    def compute_prediction_for_movie(self, userId, movieName):
        user = self.users[userId]
        if movieName.lower() not in self.movieNames:
            print("The movie is not in the database")
            return
        
        movieID = self.movieNames[movieName.lower()]
        r_a = user.averageUserRating
        numerator = 0
        denominator = 0

        for neighbor in user.neighbors:  # iterate over neighbors and their ratings for movie i
            neighbor = self.users[neighbor]
            if movieID in neighbor.movies:
                neighbor_score = neighbor.movies[movieID] - neighbor.averageUserRating
                pearson_score = self.PearsonScoreDictionary[user][neighbor.ID]
                product = neighbor_score * pearson_score
                numerator += product
                denominator += pearson_score

        if denominator == 0:  # in case the denominator happens to be 0, return the average rating.
            return r_a
        else:
            return r_a + (numerator / denominator)

    # A method that populates the movieRatingsPerUser and users dictionary
    def __create_dictionaries(self):
        ratingsPath = self.filePath + '\\ratings2.csv'
        with open(ratingsPath, newline='') as csvFile:
            reader = csv.DictReader(csvFile)

            for row in reader:  # First of all, we'll calculate the average rating of each user
                curr_id = int(row['userId'])
                rating = float(row['rating'])
                movie = int(row['movieId'])

                if curr_id not in self.users:  # Create a new user and adds it to the set
                    newUser = User(int(curr_id))
                    self.users[curr_id] = newUser
                    self.PearsonScoreDictionary[curr_id] = {}

                self.users[curr_id].movies[movie] = rating  # add the movie and rating to the User object

                if movie not in self.movies:
                    self.movies[movie] = Movie(movie)

                self.movies[movie].ratings[curr_id] = rating  # update the user rating

    def __calculateAverages(self):

        for userEntry in self.users:
            self.users[userEntry].calculate_average()

    def __populateNeighbors(self):

        for movieID, movie in self.movies.items():  # iterate over all the movies

            for user1 in movie.ratings:  # Add neighbors based on which users rated the same movie.
                for user2 in movie.ratings:
                    if user1 == user2:
                        pass
                    else:
                        self.users[user1].neighbors.add(user2)

    """
        ---- Helpful classes ----
    """

    def __calculate_score(self, user_a, user_w):

        commonMovies = user_a.movies.keys() & user_w.movies.keys()
        sum_of_normal_product = 0
        sum_of_user_a_square_ratings = 0
        sum_of_user_w_square_ratings = 0

        for movie in commonMovies:
            # numerator
            a_normalized_score = user_a.movies[movie] - user_a.averageUserRating
            w_normalized_score = user_w.movies[movie] - user_w.averageUserRating
            product = a_normalized_score * w_normalized_score
            sum_of_normal_product += product

            # denominator
            sum_of_user_a_square_ratings += a_normalized_score * a_normalized_score
            sum_of_user_w_square_ratings += w_normalized_score * w_normalized_score

        product_of_square_ratings = sum_of_user_a_square_ratings * sum_of_user_w_square_ratings
        denominator = math.sqrt(product_of_square_ratings)

        if product_of_square_ratings == 0 or denominator == 0:
            return 0

        score = sum_of_normal_product / denominator

        return score

    # create a dictionary mapping movie IDs to their names
    def __mapMovieNames(self):
        moviesPath = self.filePath + '\\movies.csv'
        with open(moviesPath, newline='') as csvFile:
            movie_reader = csv.DictReader(csvFile)
            for row in movie_reader:
                title = row['title'].split('(')[0].strip()
                movieId = int(row['movieId'])
                self.movies[movieId].name = title # Keep original name
                title = title.lower()
                self.movieNames[title] = movieId # make it lower-case for search purposes


class User:

    def __init__(self, Id):
        self.ID = Id
        self.movies = {}  # A dictionary of movies seen by the user and their ratings.
        self.neighbors = set()  # A dictionary containing a user and a set of neighbours
        self.averageUserRating = -1  # The users average rating.

    def calculate_average(self):
        i = 0
        rating_sum = 0
        for movie, rating in self.movies.items():
            rating_sum += rating
            i += 1

        self.averageUserRating = rating_sum / i


class Movie:

    def __init__(self, number):
        self.serialNum = number  # movie's serial number
        self.name = ''
        self.ratings = {}  # A dictionary mapping user to rating (for this movie)
        self.averageRating = -1
        self.genres = []

    def calculate_average_rating(self):
        rating_sum = 0
        num = 0
        for user, rating in self.ratings.items():
            rating_sum += rating
            num += 1

        self.averageRating = rating_sum / num
