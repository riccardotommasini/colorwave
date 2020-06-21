FROM node:10.20.1-alpine3.11

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
COPY package*.json ./

RUN npm ci --only=production

# Bundle app source
COPY colorstream.js colorstream.js
COPY colors.json colors.json

EXPOSE 8080

CMD [ "npm", "start" ]