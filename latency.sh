#!/bin/bash

# Loop to run the generation and curl command 100 times
for i in {1..100}
do
    # Generate a random number between 0 and 100
    user_id=$(( RANDOM % 101 ))

    # Print the generated API key (optional)
    echo
    echo
    echo "Run #$i - Generated API key: $user_id"

    # Make a curl call to localhost, passing the API key as a header
    curl "http://127.0.0.1/user/$user_id" -i -w "\nTime to Connect: %{time_connect}s\nTime to First Byte: %{time_starttransfer}s\nTotal Time: %{time_total}s\n"
done