# Stage 1: Build React App
FROM node:20-alpine AS build

RUN apk add --no-cache unzip curl

# Install yarn
# RUN npm install -g yarn

WORKDIR /app

# Download and unzip the Snowplow example repo
RUN curl -L https://github.com/snowplow-incubator/snowplow-javascript-tracker-examples/archive/refs/heads/master.zip -o master.zip \
    && unzip master.zip \
    && rm master.zip

# Move to the React app directory
WORKDIR /app/snowplow-javascript-tracker-examples-master/react

# Install dependencies and build the app
RUN yarn install && yarn build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built app to Nginx web folder
COPY --from=build /app/snowplow-javascript-tracker-examples-master/react/build /usr/share/nginx/html
