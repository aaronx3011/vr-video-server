#!/bin/bash
 
# Configuración
RED_LOCAL="192.168.88.0/24"
GATEWAY="192.168.88.1"
IP_ETH1="192.168.88.72"  # IP de tu enp129s0
 
# Limpiar configuraciones previas
sudo ip rule del from $IP_ETH1 table 101 2>/dev/null
sudo ip rule del to $RED_LOCAL table 100 2>/dev/null
sudo ip route flush table 100 2>/dev/null
sudo ip route flush table 101 2>/dev/null
 
# TABLA 100: Para tráfico LOCAL (enxf8e43b816deb)
sudo ip route add $RED_LOCAL dev enxf8e43b816deb table 100
sudo ip route add default via $GATEWAY dev enxf8e43b816deb table 100
 
# TABLA 101: Para tráfico GENERAL (enp129s0)  
sudo ip route add default via $GATEWAY dev enp129s0 table 101
 
# REGLAS DE ENRUTAMIENTO
 
# Regla 1: Todo el tráfico DESTINADO a la red local usa tabla 100 (enxf8e43b816deb)
sudo ip rule add to $RED_LOCAL table 100 priority 100
 
# Regla 2: Todo el tráfico ORIGINADO desde enp129s0 usa tabla 101 (eth1)
sudo ip rule add from $IP_ETH1 table 101 priority 200
 
# Regla 3: Todo el tráfico restante usa tabla main (por defecto enp129s0)
# Esto se hace automáticamente
 
# Asegurar que las rutas locales están correctas
sudo ip route add $RED_LOCAL dev enxf8e43b816deb
sudo ip route add default via $GATEWAY dev enp129s0
 
echo "Configuración completada:"
echo "- Tráfico a $RED_LOCAL → enxf8e43b816deb"
echo "- Tráfico desde $IP_ETH1 → enp129s0" 
echo "- Tráfico restante → enp129s0 (internet)"

