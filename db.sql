CREATE DATABASE whatsapp_bot;

CREATE TABLE users (
    phone_number VARCHAR(15) PRIMARY KEY,
    user_name VARCHAR(25) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE banned_users (
    phone_number VARCHAR(15) PRIMARY KEY,
    ban_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users (phone_number)
);

CREATE TABLE roles (
    role_name VARCHAR(255) PRIMARY KEY,
    holders INTEGER DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    phone_number VARCHAR(15) NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    grant_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (phone_number, role_name),
    FOREIGN KEY (phone_number) REFERENCES users (phone_number),
    FOREIGN KEY (role_name) REFERENCES roles (role_name)
);

CREATE TABLE commands (
    command_name VARCHAR(15) PRIMARY KEY,
    command_description VARCHAR(255) NOT NULL,
    times_executed INTEGER DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE executed_commands (
    id serial PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL,
    command_name VARCHAR(15) NOT NULL,
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users (phone_number),
    FOREIGN KEY (command_name) REFERENCES commands (command_name)
);

CREATE OR REPLACE FUNCTION add_user_role_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_roles (phone_number, role_name) VALUES (NEW.phone_number, 'USER');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_holder_count_function()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE roles SET holders = holders + 1 WHERE role_name = NEW.role_name;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_holder_count_on_update_function()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE roles SET holders = holders - 1 WHERE role_name = OLD.role_name;
    UPDATE roles SET holders = holders + 1 WHERE role_name = NEW.role_name;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_executed_command()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE commands
    SET times_executed = times_executed + 1
    WHERE command_name = NEW.command_name;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_user_role
AFTER INSERT ON users
FOR EACH ROW
EXECUTE PROCEDURE add_user_role_function();

CREATE TRIGGER update_holder_count
AFTER INSERT ON user_roles
FOR EACH ROW
EXECUTE PROCEDURE update_holder_count_function();

CREATE TRIGGER update_holder_count_on_update
AFTER UPDATE ON user_roles
FOR EACH ROW
EXECUTE PROCEDURE update_holder_count_on_update_function();

CREATE TRIGGER add_executed_command
AFTER INSERT ON executed_commands
FOR EACH ROW
EXECUTE PROCEDURE add_executed_command();

----------------------------------------

INSERT INTO roles (role_name)
VALUES ('USER'), ('MODERATOR'), ('ADMIN');

INSERT INTO commands (command_name, command_description)
VALUES ('menu', 'Returns a list of all the available commands.'),
('whoami', 'Tells you who you are.'),
('sticker', 'Creates a sticker with an image that you provide.'),
('say', 'Replies with the message you sent.'),
('send', 'Sends a message to a specified phone number, clarifying that it is your message.');
