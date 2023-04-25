rs.status();
use db_kafka_news;
db.createCollection('col_articles');
db.createUser({user: 'kafka', pwd: '123456', roles: [ { role: 'readWrite', db: 'db_kafka_news' } ]});
db.getLastError();
db.getUsers();