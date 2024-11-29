const { gql } = require('apollo-server');

const typeDefs = gql`
    type User {
        id: ID!
        name: String!
        email: String!
    }

    type Movie {
        id: ID!
        title: String!
        director: String!
        releaseYear: Int!
        reviews: [Review!]!
    }

    type Review {
        id: ID!
        rating: Float!
        reviewer: String!
        movie: Movie!
    }

    type Query {
        user(id: ID!): User
        movie(id: ID!): Movie
        movies: [Movie!]!
        reviews(movieId: ID!): [Review!]!
        allReviews: [Review!]!
    }
`;

module.exports = typeDefs;
