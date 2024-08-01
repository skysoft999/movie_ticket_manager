# movie_ticket_manager
Movie Ticket Booking Service Using Flask


> Write a REST API for a theater ticket booking system. The system should provide functionality for checking available seats.booking a seat, and temporarily reserving a seat with an expiry time.
The challenge includes implementing caching for seat availability and ensuring idempotent seat booking operations.


### Requirements:

#### API Endpoints:

1. GET /theaters/{theaterId}/seats: Retrieves the current availability of seats for a specified theater.

2. POST /theaters/{theaterId}/book: Books a seat for a specified theater. This operation should be idempotent.

3. POST /theaters/{theaterId}/reserve: Temporarily reserves a seat for a specified theater with an expiry time.


#### Caching:

Implement caching for the GET /theaters/{theaterId}/seats endpoint to improve performance. The cache should be updated accordingly when a seat is booked or reserved.


#### Idempotency:

Ensure that booking a seat is an idempotent operation. This means if the booking request is repeated (e.g., due to network issues), it won't result in multiple bookings.


#### Temporary Reservation:

Allow seats to be temporarily reserved. If the reservation is not converted to a booking within a certain time frame, the reservation expires and the seat becomes available again.


#### API Business logic Design Process:

1. Each Booking is associated with a unique booking_id (uuid)
2. before processing a booking server checksif the booking_id already exists in bookings for the theater using redis SISMEMBER
3. Handling Repeated Requests: 
    * if the booking_id is found in bookings, it means this bookings already been processed.
    * In this case server returns a 200 response with a message indicating already exist.
    * this prevent creation of duplicate booking.


### Dependencies Used:

1. Python Language
2. Flask Framework
3. flast-restful library
4. py-redis as cache client
5. loaddotenv for seperating creds from codebase

### How to run?

0. initialize a virtual-env in python
1. install dependencies -> use make file -> make install
3. change configuration if you want to
4. redis configuration port and host can be configured in .env file inside *config/.env*
5. use make file -> "make run" from root directory


### Sample Curls:

```
curl --location 'http://127.0.0.1:8000/v1/theaters/1/seats'


curl --location 'http://127.0.0.1:8000/v1/theaters/1/reserve' \
--header 'Content-Type: application/json' \
--data '{
    "seat": "A1"
}'



curl --location 'http://127.0.0.1:8000/v1/theaters/1/book' \
--header 'Content-Type: application/json' \
--data '{
    "seat": "A1"
}'

```


### TODO: Improvements:

1. Unittesting
2. ratelimiting
3. authorization
4. route , resource blueprint based structural improvements.
5. using design patterns
6. containerizing.

---

