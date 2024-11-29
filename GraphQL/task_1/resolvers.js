const mockMovies = [
    { id: 1, title: "Inception", director: "Christopher Nolan", releaseYear: 2010 },
    { id: 2, title: "The Dark Knight", director: "Christopher Nolan", releaseYear: 2008 },
    { id: 3, title: "Interstellar", director: "Christopher Nolan", releaseYear: 2014 },
    { id: 4, title: "Titanic", director: "James Cameron", releaseYear: 1997 },
    { id: 5, title: "Avatar", director: "James Cameron", releaseYear: 2009 }
  ];
  
  const mockReviews = [
    { id: 1, movieId: 1, rating: 4.8, reviewer: "Alice" },
    { id: 2, movieId: 2, rating: 4.9, reviewer: "Bob" },
    { id: 3, movieId: 3, rating: 4.7, reviewer: "Charlie" },
    { id: 4, movieId: 4, rating: 4.5, reviewer: "Alice" },
    { id: 5, movieId: 5, rating: 4.6, reviewer: "Bob" }
  ];
  
  const resolvers = {
    Query: {
      movie: (_, { id }) => mockMovies.find(movie => movie.id === Number(id)),
        movies: () => mockMovies,
  
      reviews: (_, { movieId }) =>
        mockReviews.filter(review => review.movieId === Number(movieId)),
        allReviews: () => mockReviews
    },
  
  };
  
  module.exports = resolvers;
  