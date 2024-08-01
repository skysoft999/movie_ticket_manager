import uuid
import redis
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from config import settings

app = Flask(__name__)
api = Api(app)

# Initialize Redis client
redis_client = redis.Redis(
    host=settings.redis_config.get("host", ""),
    port=int(settings.redis_config.get("port", "")), 
    db=0,
    decode_responses=True
)

# Mock data for theaters and seats
theaters = settings.theaters

RESERVATION_EXPIRY = 600  # 10 minutes

class TheaterSeats(Resource):
    def get(self, theater_id):
        if theater_id not in theaters:
            return {"error": "Theater not found"}, 404
        breakpoint()
        # Check cache first
        cached_seats = redis_client.get(f"theater:{theater_id}:seats")
        if cached_seats:
            return jsonify({"seats": eval(cached_seats)})

        # If not in cache, get from "database" and update cache
        available_seats = self._get_available_seats(theater_id)
        redis_client.setex(f"theater:{theater_id}:seats", 60, str(available_seats))  # Cache for 1 minute
        return jsonify({"seats": available_seats})

    def _get_available_seats(self, theater_id):
        all_seats = theaters[theater_id]["seats"]
        booked_seats = redis_client.smembers(f"theater:{theater_id}:booked")
        reserved_seats = redis_client.smembers(f"theater:{theater_id}:reserved")
        return list(set(all_seats) - set(booked_seats) - set(reserved_seats))

class BookSeat(Resource):
    def post(self, theater_id):
        if theater_id not in theaters:
            return {"error": "Theater not found"}, 404

        seat = request.json.get('seat')
        if not seat:
            return {"error": "Seat not specified"}, 400

        booking_id = request.json.get('booking_id', str(uuid.uuid4()))

        # Check if booking already exists (idempotency check)
        if redis_client.sismember(f"theater:{theater_id}:bookings", booking_id):
            return {"message": "Booking already exists", "booking_id": booking_id}, 200

        # Check if seat is available
        if redis_client.sismember(f"theater:{theater_id}:booked", seat) or \
           redis_client.sismember(f"theater:{theater_id}:reserved", seat):
            return {"error": "Seat is not available"}, 400

        # Book the seat
        redis_client.sadd(f"theater:{theater_id}:booked", seat)
        redis_client.sadd(f"theater:{theater_id}:bookings", booking_id)
        
        # Invalidate cache
        redis_client.delete(f"theater:{theater_id}:seats")

        return {"message": "Seat booked successfully", "booking_id": booking_id}, 201

class ReserveSeat(Resource):
    def post(self, theater_id):
        if theater_id not in theaters:
            return {"error": "Theater not found"}, 404

        seat = request.json.get('seat')
        if not seat:
            return {"error": "Seat not specified"}, 400

        # Check if seat is available
        if redis_client.sismember(f"theater:{theater_id}:booked", seat) or \
           redis_client.sismember(f"theater:{theater_id}:reserved", seat):
            return {"error": "Seat is not available"}, 400

        # Reserve the seat
        reservation_id = str(uuid.uuid4())
        redis_client.sadd(f"theater:{theater_id}:reserved", seat)
        redis_client.setex(f"theater:{theater_id}:reservation:{reservation_id}", RESERVATION_EXPIRY, seat)

        # Invalidate cache
        redis_client.delete(f"theater:{theater_id}:seats")

        return {
            "message": "Seat reserved successfully",
            "reservation_id": reservation_id,
            "expires_in": RESERVATION_EXPIRY
        }, 201

api.add_resource(TheaterSeats, '/v1/theaters/<int:theater_id>/seats')
api.add_resource(BookSeat, '/v1/theaters/<int:theater_id>/book')
api.add_resource(ReserveSeat, '/v1/theaters/<int:theater_id>/reserve')
