from ninja_jwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def generate_tokens_for_user(user) -> dict:
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserService:
    pass
