#!/bin/bash
# Script to calculate Simple Interest

# Formula: (P * R * T) / 100

echo "Enter Principal amount:"
read p

echo "Enter Rate of Interest:"
read r

echo "Enter Time (in years):"
read t

# Calculate simple interest
si=$(echo "scale=2; ($p * $r * $t) / 100" | bc)

echo "-----------------------------------"
echo "Simple Interest = $si"
echo "Total Amount = $(echo "scale=2; $p + $si" | bc)"
echo "-----------------------------------"
