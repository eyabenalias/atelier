const app = require('./app');
const eurekaClient = require('./config/eureka.client');

const PORT = parseInt(process.env.PORT || '8083', 10);

const server = app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  eurekaClient.start((error) => {
    if (error) {
      console.error('Error registering with Eureka:', error);
    } else {
      console.log(`Successfully registered with Eureka as MEETING on port ${PORT}`);
    }
  });
});

const gracefulShutdown = () => {
  console.log('Stopping Eureka client...');
  eurekaClient.stop((error) => {
    if (error) {
      console.error('Error stopping Eureka client:', error);
    } else {
      console.log('Eureka client stopped');
    }
    server.close(() => {
      process.exit(0);
    });
  });
};

process.on('SIGINT', gracefulShutdown);
process.on('SIGTERM', gracefulShutdown);
