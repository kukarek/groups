import vk_api

# Ваш токен доступа для авторизации в ВКонтакте
VK_ACCESS_TOKEN = "vk1.a.jxR6pEkaRj7j9WNJ1DBtNvolxfLtUCAZvzxSb3-WJrLUnRemjz85aI86IAUPZEiYrjRTCoUDhLYv56F41eashHp6Dq-onnhDotpXBDrlyELDI3h_qIwu4iUKvTjuC1GSSZ_MWvHZrIl32fRIKGWLZYxBvCMF5BJqaQ9uBg6KsJfaarJBV1jx9ym6aOn2us8wBZundpknFnq3kAafJk4Fog"
VK_GROUP_ID = "-220670949"  # ID вашего сообщества


def delete_wall_post(post_id):
    try:
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        vk.wall.delete(owner_id=int(VK_GROUP_ID), post_id=int(post_id))
        print("Post successfully deleted!")
    except vk_api.exceptions.ApiError as e:
        print(f"Error deleting post: {e}")

if __name__ == "__main__":
    delete_wall_post(345)
