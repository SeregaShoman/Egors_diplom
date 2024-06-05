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
    role_id INTEGER REFERENCES Roles(id),
    groups TEXT,
    institution TEXT,
    organization TEXT,
    position TEXT
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