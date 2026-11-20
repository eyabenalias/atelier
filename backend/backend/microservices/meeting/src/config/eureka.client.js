const Eureka = require('eureka-js-client').Eureka;

const PORT = parseInt(process.env.PORT || '8083', 10);
const HOST = process.env.HOST || 'localhost';
const EUREKA_HOST = process.env.EUREKA_HOST || 'localhost';
const EUREKA_PORT = parseInt(process.env.EUREKA_PORT || '8761', 10);

const client = new Eureka({
  instance: {
    app: 'MEETING',
    instanceId: `${HOST}:meeting:${PORT}`,
    hostName: HOST,
    ipAddr: '127.0.0.1',
    statusPageUrl: `http://${HOST}:${PORT}/swagger-ui`,
    healthCheckUrl: `http://${HOST}:${PORT}/api/meetings/hello`,
    port: {
      '$': PORT,
      '@enabled': 'true',
    },
    vipAddress: 'MEETING',
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn',
    },
  },
  eureka: {
    host: EUREKA_HOST,
    port: EUREKA_PORT,
    servicePath: '/eureka/apps/',
    maxRetries: 10,
    requestRetryDelay: 2000,
  },
});

module.exports = client;
