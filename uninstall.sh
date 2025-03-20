#!/bin/bash
echo "=== Serpent Task Runner Uninstallation ==="
echo "Please run as root!"

echo -e "\n1. Stopping Serpent service..."
systemctl stop serpent.service

echo -e "\n2. Disabling Serpent service..."
systemctl disable serpent.service

echo -e "\n3. Removing systemd service file..."
rm /etc/systemd/system/serpent.service

echo -e "\n4. Reloading systemd..."
systemctl daemon-reload

echo -e "\n5. Resetting failed service status..."
systemctl reset-failed

echo -e "\n6. Removing Serpent files..."
echo "  - Removing CLI tool..."
rm -f /bin/serpent

echo "  - Removing installation directory..."
rm -rf /usr/serpent

echo "  - Removing data directory..."
rm -rf /var/serpent

echo -e "\n=== Uninstallation Complete! ==="
echo "Serpent Task Runner has been completely removed from your system."
echo "All associated files and configurations have been cleaned up."