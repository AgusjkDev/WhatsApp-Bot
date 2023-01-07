CREATE DATABASE whatsapp_bot;

CREATE TABLE users (
    number VARCHAR(15) PRIMARY KEY,
    user_name VARCHAR(25) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE banned_users (
    number VARCHAR(15) PRIMARY KEY,
    reason VARCHAR(255) NOT NULL,
    ban_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (number) REFERENCES users (number)
);

CREATE TABLE roles (
    role_name VARCHAR(255) PRIMARY KEY,
    holders INTEGER DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    number VARCHAR(15) NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    grant_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (number, role_name),
    FOREIGN KEY (number) REFERENCES users (number),
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
    number VARCHAR(15) NOT NULL,
    command_name VARCHAR(15) NOT NULL,
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (number) REFERENCES users (number),
    FOREIGN KEY (command_name) REFERENCES commands (command_name)
);

CREATE OR REPLACE FUNCTION add_user_role_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_roles (number, role_name) VALUES (NEW.number, 'USER');
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

CREATE OR REPLACE FUNCTION update_grant_date_on_update_function()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.role_name != NEW.role_name THEN
        UPDATE user_roles SET grant_date = CURRENT_TIMESTAMP WHERE number = NEW.number AND role_name = NEW.role_name;
    END IF;
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

CREATE TRIGGER update_grant_date_on_update
AFTER UPDATE ON user_roles
FOR EACH ROW
EXECUTE PROCEDURE update_grant_date_on_update_function();

----------------------------------------

INSERT INTO roles (role_name)
VALUES ('USER'), ('MODERATOR'), ('ADMIN'), ('OWNER');

INSERT INTO commands (command_name, command_description)
VALUES ('menu', 'Returns a list of all the available commands.'),
('whoami', 'Tells you who you are.'),
('sticker', 'Creates a sticker with an image that you provide.'),
('say', 'Replies with the message you sent.'),
('send', 'Sends a message to a specified phone number, clarifying that it is your message.'),
('resources', 'Returns details about CPU and RAM usage.'),
('history', 'Returns the command history of an user, with an optional limit.'),
('executions', 'Returns the number of times a command has been executed.'),
('ban', 'Bans the given phone number due to a reason.'),
('unban', 'Unbans the given phone number.'),
('role', 'Sets a role for a given phone number.');
