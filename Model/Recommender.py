"""

This class parses the movie rating file and creates a huge array containing the pearson correlation of each user.

"""
import csv
import math


# noinspection PyPep8Naming
class Parse:

    def __init__(self, path: str):

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

        top = 30
        for user_a_id, user_a in self.users.items():         # Creating the actual pearson table
            top_neighbors = []  # A list of tuples containing the 30 closest neighbors < userId , correlation >
            for user_w in user_a.neighbors:
                score = self.__calculate_score(user_a, self.users[user_w])
                if score < 0:
                    continue
                if len(top_neighbors) < top:  # If there aren't X movies yet in the list, append it anyway
                    user_correlation = (user_w, score)
                    top_neighbors.append(user_correlation)
                    top_neighbors.sort(key=lambda userTuple: userTuple[1], reverse=True)
                elif score > top_neighbors[-1][0]:  # the score is greater than at least the last user in the list.
                    user_correlation = (user_w, score)
                    top_neighbors.append(user_correlation)
                    top_neighbors.sort(key=lambda userTuple: userTuple[1], reverse=True)
                    del top_neighbors[-1]

            close_neighbors = set()
            for entry in top_neighbors:
                self.PearsonScoreDictionary[user_a_id][entry[0]] = entry[1]
                close_neighbors.add(entry[0])

            user_a.neighbors = user_a.neighbors.intersection(close_neighbors)

    def get_pearson_table(self):
        return self.PearsonScoreDictionary

    def get_movie_id(self, movie_title):
        return self.movieNames[movie_title]

    def get_movie_name(self, movieID):
        return self.movies[movieID].title

    # receives a user ID and a movie name and returns the predicted rating of the given user for the movie.
    # the movie name can be upper/lower case.
    def compute_prediction_for_movie(self, userId: int, movieName: str):
        user = self.users[userId]
        title = movieName.lower()
        if title not in self.movieNames:
            print("The movie is not in the database")
            return

        movieID = self.movieNames[movieName.lower()]
        r_a = user.averageUserRating
        numerator = 0
        denominator = 0

        for neighbor in user.neighbors:  # iterate over neighbors and their ratings for movie i
            neighbor = self.users[neighbor]
            if movieID in neighbor.movies:
                try:
                    neighbor_score = neighbor.movies[movieID] - neighbor.averageUserRating
                    pearson_score = self.PearsonScoreDictionary[user.ID][neighbor.ID]
                    product = neighbor_score * pearson_score
                    numerator += product
                    denominator += pearson_score
                except KeyError:
                    print("here")

        if denominator == 0:  # in case the denominator happens to be 0, return the average rating.
            return r_a
        else:
            return r_a + (numerator / denominator)

    # Returns a DESCENDING sorted list of tuples containing the predicted score and the corresponding Movie objects.
    def get_top_x_movies_for_user(self, userId: int, top_x: int):
        top_x_list = []  # A sorted list of tuples - < predicted score, movie object >
        for movieId, movie in self.movies.items():
            if userId in movie.ratings:
                continue
            title = movie.title
            if '"' in title:
                continue
            else:
                title = title.split('(')[0].strip().lower()
            score = self.compute_prediction_for_movie(userId, title)
            try:
                if score is not None:
                    if len(top_x_list) < top_x:  # If there aren't X movies yet in the list, append it anyway
                        entry = (score, movie)
                        top_x_list.append(entry)
                        top_x_list.sort(key=lambda x: x[0], reverse=True)
                    elif score > top_x_list[-1][0]:  # the score is greater than at least the last element in the list.
                        entry = (score, movie)
                        top_x_list.append(entry)
                        top_x_list.sort(key=lambda x: x[0], reverse=True)
                        del top_x_list[-1]
            except TypeError:
                print(movie.title)

        return top_x_list

    @staticmethod
    def get_rating(pair):
        return pair[0]

    # Retrieves titles and ratings of top X movies
    def get_top_rated_movies(self, top_x):
        pass

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

        for movieId, movie in self.movies.items():
            movie.calculate_average_rating()

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
        with open(moviesPath, encoding="utf8") as csvFile:
            movie_reader = csv.DictReader(csvFile)
            for row in movie_reader:
                title = row['title']
                movieID = int(row['movieId'])
                if (movieID not in self.movies):
                    self.movies[movieID] = Movie(movieID)
                self.movies[movieID].title = title  # Keep original name
                title = title.split('(')[0].strip().lower()
                self.movieNames[title] = movieID  # make it lower-case for search purposes

class User:

    def __init__(self, Id):
        self.ID = Id
        self.movies = {}  # A dictionary of movies seen by the user and their ratings.
        self.neighbors = set()  # A dictionary containing a user and a set of neighbours (BY ID!!!)
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
        self.title = ''
        self.ratings = {}  # A dictionary mapping user to rating (for this movie) < userID : Rating >
        self.averageRating = -1
        self.genres = []

    def calculate_average_rating(self):
        rating_sum = 0
        num = 0
        for user, rating in self.ratings.items():
            rating_sum += rating
            num += 1
        if num != 0:
            self.averageRating = rating_sum / num
