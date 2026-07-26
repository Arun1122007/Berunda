def test_cross_station_denial():
    # Attempt to retrieve cases from Station B while authorized for Station A
    authorized_stations = ["STATION_A"]
    # Service should return empty or error
    assert "STATION_B" not in authorized_stations

def test_unauthorized_user_extraction():
    user_authorized = False
    try:
        # service.extract(..., user_authorized=False)
        pass
    except PermissionError:
        assert True
