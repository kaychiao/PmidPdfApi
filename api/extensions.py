from spectree import SpecTree, SecurityScheme
from config import Config

# Initialize SpecTree for API validation and documentation
spec = SpecTree(
    "flask", 
    title=Config.API_TITLE, 
    version=Config.API_VERSION,
    ui='swagger',
    security_schemes=[
        SecurityScheme(
            name="UserAuth",
            data={"type": "apiKey", "name": "X-API-Key", "in": "header"},
        ),
    ],
    security={"UserAuth": []},
    )
