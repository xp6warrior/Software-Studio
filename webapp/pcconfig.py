import pynecone as pc

class WebappConfig(pc.Config):
    pass

config = WebappConfig(
    app_name="webapp",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)