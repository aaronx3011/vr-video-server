#!/bin/bash

# Recorrer el directorio actual
for file in ./videos/low/*; do
  # Eliminar archivos .ts y .m3u8
  if [[ "$file" =~ \.(ts|m3u8)$ ]]; then
    rm "$file"
  fi
done

for file in ./videos/high/*; do
  # Eliminar archivos .ts y .m3u8
  if [[ "$file" =~ \.(ts|m3u8)$ ]]; then
    rm "$file"
  fi
done