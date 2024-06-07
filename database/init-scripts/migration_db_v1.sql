CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fio TEXT NOT NULL,
    avatar_url TEXT,
    login TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER REFERENCES Roles(id)
);

CREATE TABLE Students (
    user_id UUID PRIMARY KEY REFERENCES Users(id),
    groups TEXT NOT NULL,
    institution TEXT NOT NULL
);

CREATE TABLE Partners (
    user_id UUID PRIMARY KEY REFERENCES Users(id),
    organization TEXT NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE Events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    max_participants INTEGER NOT NULL,
    status TEXT NOT NULL,
    type TEXT NOT NULL,
    start_time TEXT NOT NULL,
    image_url TEXT,
    creator_id UUID REFERENCES Users(id)
);

CREATE TABLE EventRegistrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES Events(id),
    user_id UUID REFERENCES Users(id)
);

INSERT INTO Roles (name) VALUES ('Студент'), ('Партнёр'), ('Админ');
