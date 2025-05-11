import random
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def generate_code():
    return random.randint(100000, 999999)

def send_verification_code(user_id):
    code = generate_code()
    r.setex(f"verify:{user_id}", 300, code)
    return code

def verify_code(user_id, input_code):
    stored_code = r.get(f"verify:{user_id}")
    if stored_code and stored_code.decode() == str(input_code):
        r.delete(f"verify:{user_id}")
        return True
    return False