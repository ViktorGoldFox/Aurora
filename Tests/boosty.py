import boosty
# import boosty.api

api = boosty.api.API()

response = api.get_post("boosty", post_id="c9fb8a19-c45e-4602-9942-087c3af28c1b")

print(response.title)