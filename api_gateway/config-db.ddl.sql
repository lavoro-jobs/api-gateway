CREATE TABLE IF NOT EXISTS position_catalog (
    id SERIAL PRIMARY KEY,
    position_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS education_catalog (
    id SERIAL PRIMARY KEY,
    education_level VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS contract_type_catalog (
    id SERIAL PRIMARY KEY,
    contract_type VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS work_type_catalog (
    id SERIAL PRIMARY KEY,
    work_type VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS skills_catalog (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL
);



INSERT INTO position_catalog (position_name) VALUES ('Software Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Frontend Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Backend Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Fullstack Engineer');
INSERT INTO position_catalog (position_name) VALUES ('QA Engineer');
INSERT INTO position_catalog (position_name) VALUES ('System Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Site Reliability Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Security Engineer');
INSERT INTO education_catalog (education_level) VALUES ('High School - Complete');
INSERT INTO education_catalog (education_level) VALUES ('Bachelor - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('Bachelor - Complete');
INSERT INTO education_catalog (education_level) VALUES ('Master - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('Master - Complete');
INSERT INTO education_catalog (education_level) VALUES ('PhD - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('PhD - Complete');
INSERT INTO position_catalog (position_name) VALUES ('DevOps Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Business Analyst');
INSERT INTO position_catalog (position_name) VALUES ('Project Manager');
INSERT INTO position_catalog (position_name) VALUES ('Product Owner');
INSERT INTO position_catalog (position_name) VALUES ('Scrum Master');
INSERT INTO position_catalog (position_name) VALUES ('UX Designer');
INSERT INTO position_catalog (position_name) VALUES ('UI Designer');
INSERT INTO position_catalog (position_name) VALUES ('Data Scientist');
INSERT INTO position_catalog (position_name) VALUES ('Data Analyst');
INSERT INTO position_catalog (position_name) VALUES ('Data Engineer');
INSERT INTO position_catalog (position_name) VALUES ('Data Architect');

INSERT INTO education_catalog (education_level) VALUES ('High School - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('High School - Complete');
INSERT INTO education_catalog (education_level) VALUES ('Bachelor - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('Bachelor - Complete');
INSERT INTO education_catalog (education_level) VALUES ('Master - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('Master - Complete');
INSERT INTO education_catalog (education_level) VALUES ('PhD - Incomplete');
INSERT INTO education_catalog (education_level) VALUES ('PhD - Complete');

INSERT INTO contract_type_catalog (contract_type) VALUES ('Part Time');
INSERT INTO contract_type_catalog (contract_type) VALUES ('Freelance');
INSERT INTO contract_type_catalog (contract_type) VALUES ('Internship');
INSERT INTO contract_type_catalog (contract_type) VALUES ('Full Time');


INSERT INTO work_type_catalog (work_type) VALUES ('Remote');
INSERT INTO work_type_catalog (work_type) VALUES ('Hybrid');
INSERT INTO work_type_catalog (work_type) VALUES ('On Site');

INSERT INTO skills_catalog (skill_name) VALUES ('Python');
INSERT INTO skills_catalog (skill_name) VALUES ('Java');
INSERT INTO skills_catalog (skill_name) VALUES ('C#');
INSERT INTO skills_catalog (skill_name) VALUES ('C++');
INSERT INTO skills_catalog (skill_name) VALUES ('PHP');
INSERT INTO skills_catalog (skill_name) VALUES ('Ruby');
INSERT INTO skills_catalog (skill_name) VALUES ('Swift');
INSERT INTO skills_catalog (skill_name) VALUES ('Kotlin');
INSERT INTO skills_catalog (skill_name) VALUES ('TypeScript');
INSERT INTO skills_catalog (skill_name) VALUES ('Go');
INSERT INTO skills_catalog (skill_name) VALUES ('Scala');
INSERT INTO skills_catalog (skill_name) VALUES ('Rust');
INSERT INTO skills_catalog (skill_name) VALUES ('Perl');
INSERT INTO skills_catalog (skill_name) VALUES ('R');
INSERT INTO skills_catalog (skill_name) VALUES ('Dart');
INSERT INTO skills_catalog (skill_name) VALUES ('Haskell');
INSERT INTO skills_catalog (skill_name) VALUES ('Julia');
INSERT INTO skills_catalog (skill_name) VALUES ('Lua');
INSERT INTO skills_catalog (skill_name) VALUES ('Matlab');
INSERT INTO skills_catalog (skill_name) VALUES ('Objective-C');
INSERT INTO skills_catalog (skill_name) VALUES ('Visual Basic');
INSERT INTO skills_catalog (skill_name) VALUES ('Assembly');
INSERT INTO skills_catalog (skill_name) VALUES ('Delphi');
INSERT INTO skills_catalog (skill_name) VALUES ('Groovy');
INSERT INTO skills_catalog (skill_name) VALUES ('Clojure');
INSERT INTO skills_catalog (skill_name) VALUES ('Elixir');
INSERT INTO skills_catalog (skill_name) VALUES ('Erlang');
INSERT INTO skills_catalog (skill_name) VALUES ('F#');
INSERT INTO skills_catalog (skill_name) VALUES ('React');
INSERT INTO skills_catalog (skill_name) VALUES ('Angular');
INSERT INTO skills_catalog (skill_name) VALUES ('Vue');
INSERT INTO skills_catalog (skill_name) VALUES ('Ember');
INSERT INTO skills_catalog (skill_name) VALUES ('Svelte');
INSERT INTO skills_catalog (skill_name) VALUES ('Node');
INSERT INTO skills_catalog (skill_name) VALUES ('Express');
INSERT INTO skills_catalog (skill_name) VALUES ('Spring');
INSERT INTO skills_catalog (skill_name) VALUES ('Django');
INSERT INTO skills_catalog (skill_name) VALUES ('Flask');
INSERT INTO skills_catalog (skill_name) VALUES ('Laravel');
INSERT INTO skills_catalog (skill_name) VALUES ('Ruby on Rails');
INSERT INTO skills_catalog (skill_name) VALUES ('ASP.NET');
INSERT INTO skills_catalog (skill_name) VALUES ('jQuery');
INSERT INTO skills_catalog (skill_name) VALUES ('Bootstrap');
INSERT INTO skills_catalog (skill_name) VALUES ('Tailwind');
INSERT INTO skills_catalog (skill_name) VALUES ('Material UI');
INSERT INTO skills_catalog (skill_name) VALUES ('Ant Design');
INSERT INTO skills_catalog (skill_name) VALUES ('Chakra UI');
INSERT INTO skills_catalog (skill_name) VALUES ('Vuetify');
INSERT INTO skills_catalog (skill_name) VALUES ('Bulma');
INSERT INTO skills_catalog (skill_name) VALUES ('Sass');
INSERT INTO skills_catalog (skill_name) VALUES ('Less');
INSERT INTO skills_catalog (skill_name) VALUES ('Stylus');
INSERT INTO skills_catalog (skill_name) VALUES ('Jest');
INSERT INTO skills_catalog (skill_name) VALUES ('Mocha');
INSERT INTO skills_catalog (skill_name) VALUES ('Cypress');
INSERT INTO skills_catalog (skill_name) VALUES ('Enzyme');
INSERT INTO skills_catalog (skill_name) VALUES ('React Testing Library');
INSERT INTO skills_catalog (skill_name) VALUES ('Jasmine');
INSERT INTO skills_catalog (skill_name) VALUES ('Karma');
INSERT INTO skills_catalog (skill_name) VALUES ('Puppeteer');
INSERT INTO skills_catalog (skill_name) VALUES ('Playwright');
INSERT INTO skills_catalog (skill_name) VALUES ('Selenium');
INSERT INTO skills_catalog (skill_name) VALUES ('Cucumber');
INSERT INTO skills_catalog (skill_name) VALUES ('Appium');
INSERT INTO skills_catalog (skill_name) VALUES ('Docker');
INSERT INTO skills_catalog (skill_name) VALUES ('Kubernetes');
INSERT INTO skills_catalog (skill_name) VALUES ('AWS');
INSERT INTO skills_catalog (skill_name) VALUES ('Azure');
INSERT INTO skills_catalog (skill_name) VALUES ('GCP');
INSERT INTO skills_catalog (skill_name) VALUES ('Heroku');
INSERT INTO skills_catalog (skill_name) VALUES ('Netlify');
INSERT INTO skills_catalog (skill_name) VALUES ('Vercel');
INSERT INTO skills_catalog (skill_name) VALUES ('Firebase');
INSERT INTO skills_catalog (skill_name) VALUES ('Digital Ocean');
INSERT INTO skills_catalog (skill_name) VALUES ('Linode');
INSERT INTO skills_catalog (skill_name) VALUES ('Vagrant');
INSERT INTO skills_catalog (skill_name) VALUES ('Terraform');
INSERT INTO skills_catalog (skill_name) VALUES ('Ansible');
INSERT INTO skills_catalog (skill_name) VALUES ('Puppet');
INSERT INTO skills_catalog (skill_name) VALUES ('Prometheus');
INSERT INTO skills_catalog (skill_name) VALUES ('Grafana');
INSERT INTO skills_catalog (skill_name) VALUES ('ELK Stack');
INSERT INTO skills_catalog (skill_name) VALUES ('Graylog');
INSERT INTO skills_catalog (skill_name) VALUES ('Splunk');
INSERT INTO skills_catalog (skill_name) VALUES ('Logstash');
INSERT INTO skills_catalog (skill_name) VALUES ('Kibana');
INSERT INTO skills_catalog (skill_name) VALUES ('Nagios');
INSERT INTO skills_catalog (skill_name) VALUES ('Sentry');
INSERT INTO skills_catalog (skill_name) VALUES ('RabbitMQ');
INSERT INTO skills_catalog (skill_name) VALUES ('Kafka');
INSERT INTO skills_catalog (skill_name) VALUES ('Redis');
INSERT INTO skills_catalog (skill_name) VALUES ('Memcached');
INSERT INTO skills_catalog (skill_name) VALUES ('PostgreSQL');
INSERT INTO skills_catalog (skill_name) VALUES ('MySQL');
INSERT INTO skills_catalog (skill_name) VALUES ('MariaDB');
INSERT INTO skills_catalog (skill_name) VALUES ('MongoDB');
INSERT INTO skills_catalog (skill_name) VALUES ('Cassandra');
INSERT INTO skills_catalog (skill_name) VALUES ('Elasticsearch');
INSERT INTO skills_catalog (skill_name) VALUES ('Neo4j');
INSERT INTO skills_catalog (skill_name) VALUES ('CouchDB');
INSERT INTO skills_catalog (skill_name) VALUES ('SQLite');
INSERT INTO skills_catalog (skill_name) VALUES ('Oracle');
INSERT INTO skills_catalog (skill_name) VALUES ('SQL Server');
INSERT INTO skills_catalog (skill_name) VALUES ('DynamoDB');
INSERT INTO skills_catalog (skill_name) VALUES ('CockroachDB');

