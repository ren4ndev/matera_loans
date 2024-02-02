def test_get_authentication_token_using_wrong_credentials(client):
    response = client.post(
        "/login/",
        {"username": "admin", "password": "wrong"})
    print(response)
    assert response.status_code == 400


def test_get_authentication_token(client):
    response = client.post(
        "/login/",
        {"username": "testuser1", "password": "matera123"})
    assert response.status_code == 200
    assert "token" in response.json()


# def test_post_new_loan_without_token(client):
#     response = client.post(
#         "/loans/",
#         {
#             "nominal_value": "1000.00",
#             "interest_rate": "1.00",
#             "ip_address": "163.198.0.1",
#             "request_date": "2024-02-01",
#             "bank": "Itau"
#         })
#     assert response.status_code == 401


# def test_post_new_loan_using_generated_token(client):
#     response = client.post(
#         "/login/",
#         {"username": "testuser1", "password": "matera123"})
#     client.credentials(HTTP_AUTHORIZATION="Token " + response.json()["token"])
#     response = client.post(
#         "/loans/",
#         {
#             "nominal_value": "1000.00",
#             "interest_rate": "1.00",
#             "ip_address": "163.198.0.1",
#             "request_date": "2024-02-01",
#             "bank": "Itau"
#         })
#     assert response.status_code == 201
#     assert response.json()["bank"] == "Itau"
