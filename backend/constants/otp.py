OTP_LENGTH: int = 6
OTP_EXPIRY_SECONDS: int = 5 * 60
OTP_MAX_ATTEMPTS: int = 5

# rate limit: how many OTP requests per mobile in a rolling window
OTP_RATE_LIMIT_COUNT: int = 3
OTP_RATE_LIMIT_WINDOW_SECONDS: int = 10 * 60
