#!/bin/bash
echo "=== Serpent Task Runner Installation ==="
echo "Please run as root!"

echo -e "\n1. Setting up executable permissions..."
chmod +x ./cli.py


echo -e "\n2. Creating installation directories..."
mkdir -p /usr/serpent/
mkdir -p /var/serpent/

echo -e "\n3. Installing CLI tool..."
cp ./cli.py /bin/serpent


echo -e "\n4. Installing runner script..."
cp ./runner.py /usr/serpent/runner.py

echo -e "\n5. Creating database..."
sqlite3 jobs.db <<EOF
CREATE TABLE jobs(
	name	TEXT PRIMARY KEY,
	delay	INTEGER NOT NULL,
	path	TEXT NOT NULL,
	status	INTEGER NOT NULL,
	type	TEXT NOT NULL,
	dependencies	TEXT,
	last_run	TIMESTAMP,
	last_status	TEXT,
	last_error	TEXT
);
EOF

echo -e "\n6. Setting up database and log files..."
cp ./jobs.db /var/serpent/
chmod 777 /var/serpent/jobs.db
touch /var/serpent/serpent.log
chmod 777 /var/serpent/serpent.log

echo -e "\n7. Installing systemd service..."
cp ./serpent.service /etc/systemd/system/

echo -e "\n8. Reloading systemd and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable serpent.service
sudo systemctl restart serpent.service

echo -e "\n=== Installation Complete! ==="
echo "Serpent Task Runner has been installed successfully."
echo "You can now use the 'serpent' command to manage your tasks."
echo "Check the log file at /var/serpent/serpent.log for detailed information."
