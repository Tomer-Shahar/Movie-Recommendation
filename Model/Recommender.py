"""

This class parses the movie rating file and creates a huge array containing the pearson correlation of each user.

"""
import csv
import math
import random
import copy
from random import randint


# noinspection PyPep8Naming
class Parse:

    def __init__(self, path: str):

        self.filePath = path
        self.PearsonScoreDictionary = {}  # A dictionary mapping pearson correlation between users.
        self.movies = {}  # A dictionary containing each movie and the ratings it Receives per user
        self.users = {}  # A dictionary mapping user IDs to their average/ratings
        self.movieNames = {}  # A dictionary that maps movie titles to their numbers
        self.sequentialID = 700

    def parse_movieDB_files(self):

        self.__create_dictionaries()
        self.__mapMovieNames()
        self.__calculateAverages()
        self.__populateNeighbors()
        self.__calculateSimilarities()
        print("Done parsing")

    # Receives a list of tuples containing the movie NAMES and their ratings for a new user
    # Adds the user to the system: create user, update neighbors, update average movie score
    def add_new_user(self, newRatings: list, ID=-1):
        if ID == -1:
            newUser = User(self.sequentialID)
        else:
            newUser = User(ID)
        self.PearsonScoreDictionary[newUser.ID] = {}  # create new entry in the pearson table
        for rating in newRatings:  # < movie name (year) : rating >
            score = float(rating[1])
            movieID = self.get_movie_id(rating[0])
            movieName = rating[0].lower().split('(')[0].strip()
            newUser.movies[movieID] = score
            self.movies[movieID].ratings[newUser.ID] = score  # add the user to the list of users that have seen the movie
            self.movies[movieID].calculate_average_rating()

        for movie_id in newUser.movies:  # iterate over movies the new user has seen
            for user in self.movies[movie_id].ratings:  # iterate over the users that have seen the movie
                if user == newUser.ID:
                    continue
                self.users[user].neighbors.add(newUser.ID)
                newUser.neighbors.add(user)

        newUser.calculate_average()
        self.users[newUser.ID] = newUser
        self.__calculateSimilarities()
        self.sequentialID += 1
        self.users[newUser.ID] = newUser
        return newUser.ID

    def __calculateSimilarities(self):
        top = 30
        for user_a_id, user_a in self.users.items():  # Creating the actual pearson table
            top_neighbors = []  # A list of tuples that will contain the 30 closest neighbors < userId , correlation >
            if len(user_a.neighbors) == top:
                continue
            for user_w in user_a.neighbors:
             #   try:
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
              #  except KeyError:
                  #  print("here")

            close_neighbors = set()
            for entry in top_neighbors:
                self.PearsonScoreDictionary[user_a_id][entry[0]] = entry[1]
                close_neighbors.add(entry[0])

            user_a.neighbors = user_a.neighbors.intersection(close_neighbors)

    def get_pearson_table(self):
        return self.PearsonScoreDictionary

    def get_movie_id(self, movie_title):
        movie_title = movie_title.lower().split('(')[0].strip()
        return self.movieNames[movie_title]

    def get_movie_name(self, movieID):
        return self.movies[movieID].title

    # receives a user ID and a movie name and returns the predicted rating of the given user for the movie.
    # the movie name can be upper/lower case.
    def compute_prediction_for_movie(self, userId: int, movieName: str="", movieID: int=-1):
        user = self.users[userId]
        if movieName != "":
            title = movieName.lower()
            if '(' in title:
                title = title.split('(')[0].strip()
            if title not in self.movieNames:
                print("The movie is not in the database")
                return

            movieID = self.movieNames[title]

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
                    pass

        if denominator == 0:  # in case the denominator happens to be 0, return the average rating.
            return r_a
        else:
            return self.rounded_score(r_a + (numerator / denominator))

    # Returns a DESCENDING sorted list of tuples containing the predicted score and the corresponding Movie objects.
    def get_top_x_movies_for_user(self, userId: int, top_x: int):
        top_x_list = []  # A sorted list of tuples - < predicted score, movie object >
        for movieId, movie in self.movies.items():
            if userId in movie.ratings:  # Don't recommend movies that the user has already seen
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
    def get_top_rated_movies_global(self, top_x):
        top_x_list = []  # A sorted list of tuples - < Movie Name, Movie Score >
        min_num_of_ratings = 25
        for movieId, movie in self.movies.items():
            if len(movie.ratings.keys()) < min_num_of_ratings:
                continue
            if len(top_x_list) < top_x:  # If there aren't X movies yet in the list, append it anyway
                entry = (movie.title, movie.averageRating)
                top_x_list.append(entry)
                top_x_list.sort(key=lambda x: x[1], reverse=True)
            else:
                entry = (movie.title, movie.averageRating)
                top_x_list.append(entry)
                top_x_list.sort(key=lambda x: x[1], reverse=True)
                del top_x_list[-1]

        for i in range(0, len(top_x_list)):
            title = top_x_list[i][0]
            score = round(top_x_list[i][1], 2)
            top_x_list[i] = (title, score)

        return top_x_list

    def get_top_movies_for_genre(self, genre: str, top_x: int):
        top_x_list = []  # A sorted list of tuples - < Movie Name, Movie Score >
        min_num_of_ratings = 20
        for movieId, movie in self.movies.items():
            if len(movie.ratings.keys()) < min_num_of_ratings or \
                    genre not in movie.genres:
                continue
            if len(top_x_list) < top_x:  # If there aren't X movies yet in the list, append it anyway
                entry = (movie.title, movie.averageRating)
                top_x_list.append(entry)
                top_x_list.sort(key=lambda x: x[1], reverse=True)
            else:
                entry = (movie.title, movie.averageRating)
                top_x_list.append(entry)
                top_x_list.sort(key=lambda x: x[1], reverse=True)
                del top_x_list[-1]

        for i in range(0, len(top_x_list)):
            title = top_x_list[i][0]
            score = round(top_x_list[i][1], 2)
            top_x_list[i] = (title, score)
        return top_x_list

    # A method that populates the movieRatingsPerUser and users dictionary
    def __create_dictionaries(self):
        ratingsPath = self.filePath + '\\ratings2.csv'
        with open(ratingsPath, newline='') as csvFile:
            reader = csv.DictReader(csvFile)

            for row in reader:  # First of all, we'll calculate the average rating of each user
                curr_id = int(row['userId'])
                rating = float(row['rating'])
                movie_id = int(row['movieId'])

                if curr_id not in self.users:  # Create a new user and adds it to the set
                    newUser = User(int(curr_id))
                    self.users[curr_id] = newUser
                    self.PearsonScoreDictionary[curr_id] = {}
                    self.sequentialID = curr_id

                self.users[curr_id].movies[movie_id] = rating  # add the movie and rating to the User object

                if movie_id not in self.movies:
                    self.movies[movie_id] = Movie(movie_id)

                self.movies[movie_id].ratings[curr_id] = rating  # update the user rating
            self.sequentialID += 1

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

    # Returns similarity between two users (W_a,u)
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
                genres = set(row['genres'].split('|'))
                if movieID not in self.movies:
                    self.movies[movieID] = Movie(movieID)
                self.movies[movieID].title = title  # Keep original name
                title = title.split('(')[0].strip().lower()
                self.movieNames[title] = movieID  # make it lower-case for search purposes
                self.movies[movieID].genres = genres

    def checkUserInput(self, ranks: list):
        user_ratings = []
        popularMovies = self.get_top_rated_movies_global(20)
        number_of_rated_movies = 0
        success = False
        for i in range(0, 20):
            rank_score = ranks[i]
            movie_to_rank = popularMovies[i][0]
            try:
                rank_number = float(rank_score)
                if rank_number < 0 or rank_number > 5:
                    return False, user_ratings
                else:
                    ranked_movie = (movie_to_rank, rank_number)
                    user_ratings.append(ranked_movie)
                    number_of_rated_movies += 1
                    if number_of_rated_movies >= 5:
                        success = True
            except ValueError:
                if i == 19:
                    if number_of_rated_movies < 5:
                        return False, user_ratings
        return True, user_ratings

    # Performs an accuracy test with n-cross-validation
    # Note that we need to add a NEW user that has only seen the test set, and later remove him.
    def run_accuracy_test(self, n: int):
        tens_system_wins, average_rmse, strawman_average_rmse = 0, 0, 0
        users_tested = set()  # Keep track of which users were chosen to not form duplicated
        for i in range(0, n):
            userCopy = self.get_new_user(users_tested)

            trainSet, testSet = self.splitSets(userCopy.movies, 0.8)  # randomly split the set of movies
            new_user_ID = self.add_new_user(trainSet)

            rmse = self.calc_rmse(testSet, new_user_ID)
            strawman_rmse = self.calc_strawman_rmse(testSet)
            average_rmse += rmse
            strawman_average_rmse += strawman_rmse

            if rmse < strawman_rmse:
                tens_system_wins += 1
            self.remove_user(new_user_ID)
            self.add_old_user(userCopy)
        self.print_results(average_rmse/n, n, strawman_average_rmse/n, tens_system_wins)

        return average_rmse

    def calc_rmse(self, testSet, new_user_ID):
        numerator = 0
        for movie, real_rating in testSet:
            prediction = self.compute_prediction_for_movie(new_user_ID, movieID=movie)
            error = (prediction-real_rating) ** 2
            numerator += error
        fraction = numerator / len(testSet)
        return math.sqrt(fraction)

    @staticmethod
    def print_results(average_rmse, n, strawman_rmse, wins):
        print("---- ACCURACY TEST PARAMETERS ----")
        print("Number of Users Tested: " + str(n))
        print("Minimum Threshold of Movies Seen: 30")
        print("----- ACCURACY TEST RESULTS -----")
        print("Strawman Average RMSE: ", strawman_rmse)
        print("TENS Average RMSE: ", average_rmse)
        print("----------- Conclusion -----------")
        print("TENS system was more accurate for " + str(wins) + " out of " + str(n) + " users")
        print("----------------------------------")


    def get_new_user(self, users_tested):
        userCopy = self.get_random_user(minMoviesSeen=30)  # Get a user that has seen at least 30 movies.
        while userCopy.ID in users_tested:
            userCopy = self.get_random_user(minMoviesSeen=30)  # Get a user that has seen at least 30 movies.

        users_tested.add(userCopy.ID)
        self.remove_user(userCopy.ID)  # Remove from system since the user has been chosen.
        return userCopy

    def calc_strawman_rmse(self, userRatings):
        numerator = 0
        sum = 0
        for movie, real_rating in userRatings:
            sum += real_rating
        for movie, real_rating in userRatings:
            prediction = self.movies[movie].averageRating
            error = (prediction-real_rating) ** 2
            numerator += error
        fraction = numerator / len(userRatings)
        return math.sqrt(fraction)

    def get_random_user(self, minMoviesSeen):
        numOfUsers = len(self.users)
        moviesSeen = 0
        userID = -1
        while moviesSeen < minMoviesSeen:
            userID = randint(0, numOfUsers)  # Choose random user (?)
            try:
                moviesSeen = len(self.users[userID].movies)
            except KeyError:
                pass
        userForTest = User(userID, self.users[userID])  # copy the user
        return userForTest

    def splitSets(self, userMovies, ratio):
        trainSize = int(len(userMovies) * ratio)
        keys = random.sample(userMovies.items(), trainSize)
        trainSet = {}
        testSet = copy.deepcopy(userMovies)
        for k in keys:
            trainSet[k[0]] = k[1]
            testSet.pop(k[0])
        # values = [userMovies[k] for k in keys]
        trainList = [(self.get_movie_name(movie), rating) for movie, rating in trainSet.items()]
        testList = [(movie, rating) for movie, rating in testSet.items()]
        return trainList, testList

    # Adds a user to the DB (note that this func receives an actual user OBJECT and not just ID)
    def add_old_user(self, user):
        ratings = [(self.get_movie_name(ID), rating) for ID, rating in user.movies.items()]
        self.add_new_user(ratings, ID=user.ID)

    # Receives a user ID and removes from DB
    def remove_user(self, userID):
        user = self.users[userID]
        self.PearsonScoreDictionary[userID] = None  # remove from pearson score dictionary
        for movie, rating in user.movies.items():
            self.movies[movie].ratings.pop(userID)  # Remove this user from the users that have seen each movie
        for user in self.users:
            if userID in self.users[user].neighbors:
                self.users[user].neighbors.remove(userID)
        self.users.pop(userID)

    def calc_average_rmse(self, n, originalSet, userCopy):
        sum_rmse = 0
        trainSet, testSet = self.splitSets(originalSet, 0.8)  # randomly split the set of movies
        newID = self.add_new_user(trainSet)
        sum_rmse += self.calc_rmse(originalSet, testSet, newID)
        self.remove_user(newID)
        average_rmse = sum_rmse
        return average_rmse

    """
        ---- Helpful classes ----
    """

    def rounded_score(self, score: float):
        if score > 5:
            return 5
        remainder = score % 1
        score = int(score)
        if 0.33 < remainder < 0.66:
            score += 0.5
        elif remainder >= 0.66:
            score += 1

        return score


class User:

    def __init__(self, Id: int, orig=None):
        if orig is None:
            self.ID = Id
            self.movies = {}  # A dictionary of movies seen by the user and their ratings.
            self.neighbors = set()  # A dictionary containing a user and a set of neighbours (BY ID!!!)
            self.averageUserRating = -1  # The users average rating.
        else:  # copy constructor
            self.ID = orig.ID
            self.movies = copy.deepcopy(orig.movies)
            self.neighbors = copy.deepcopy(orig.neighbors)
            self.averageUserRating = orig.averageUserRating

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
        self.genres = set()

    def calculate_average_rating(self):
        rating_sum = 0
        num = 0
        for user, rating in self.ratings.items():
            rating_sum += rating
            num += 1
        if num != 0:
            self.averageRating = rating_sum / num
