from ninja_jwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def attach_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserService:
    pass
