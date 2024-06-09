CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fio VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    login VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role_id INTEGER REFERENCES Roles(id)
);

CREATE TABLE Students (
    user_id UUID PRIMARY KEY REFERENCES Users(id),
    groups VARCHAR(100) NOT NULL,
    institution VARCHAR(100) NOT NULL
);

CREATE TABLE Partners (
    user_id UUID PRIMARY KEY REFERENCES Users(id),
    organization VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL
);

CREATE TABLE Events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    max_participants INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    place VARCHAR(150) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    created_time TIMESTAMP NOT NULL,
    image_url VARCHAR(255),
    creator_id UUID REFERENCES Users(id)
);


CREATE TABLE EventRegistrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES Events(id),
    user_id UUID REFERENCES Users(id)
);

CREATE TABLE Tags (
    id SERIAL PRIMARY KEY,
    partners_items TEXT[] NOT NULL,
    education_items TEXT[] NOT NULL,
    organization_items TEXT[] NOT NULL
);

INSERT INTO Roles (name) VALUES ('Студент'), ('Партнёр'), ('Админ');

INSERT INTO Tags (partners_items, education_items, organization_items) VALUES (
    ARRAY['Все', 'Банковское дело', 'IT', 'Право и юриспруденция', 'Гостеприимство и сервис', 'Коммерция', 'Практики и стажировки', 'Наставники', 'Вакансии и трудоустройство'],
    ARRAY['Все', 'Спорт', 'Творчество', 'СМИ/Медиа', 'Доп образование', 'Языковая подготовка', 'Soft Skills', 'Наука'],
    ARRAY['Все', 'СГЭУ', 'Сбербанк', 'ВТБ', 'Россельхоз Банк']
);
