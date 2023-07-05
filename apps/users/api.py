from ninja import Router

router = Router(tags=["Users"])


@router.get("")
def users(request):
    return "users router"
