const { gql } = require('apollo-server');

const typeDefs = gql`
  type Movie {
    id: ID!
    title: String!
    director: String!
    releaseYear: Int!
    reviews: [Review!]!
  }

  type Review {
    id: ID!
    movieId: ID!
    rating: Float!
    reviewer: String!
    movie: Movie!  # This is the new field to connect Review to Movie
  }

  type Query {
    movies: [Movie!]!
    movie(id: ID!): Movie
    reviews: [Review!]!
    review(id: ID!): Review
  }
`;

module.exports = typeDefs;